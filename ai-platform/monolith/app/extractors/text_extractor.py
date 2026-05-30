import fitz  # PyMuPDF
import hashlib
import base64
import logging
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class ImageType(str, Enum):
    """
    Klasifikasi LOW-LEVEL image.
    Beda dengan FigureType yang high-level & pedagogis.
    
    ImageExtractor → tahu BENTUK & SUMBER
    FigureExtractor → tahu MAKNA & KONTEKS PENDIDIKAN
    """
    RASTER_EMBEDDED  = "raster_embedded"   # gambar embed dalam PDF
    VECTOR_RENDERED  = "vector_rendered"   # vector di-render jadi raster
    SCANNED_PAGE     = "scanned_page"      # halaman scan (seluruh halaman)
    SCANNED_REGION   = "scanned_region"    # region scan dalam halaman
    DECORATIVE       = "decorative"        # border, ornamen, background
    UNKNOWN          = "unknown"


class ImageColorspace(str, Enum):
    RGB      = "rgb"
    GRAY     = "gray"
    CMYK     = "cmyk"
    INDEXED  = "indexed"
    UNKNOWN  = "unknown"


@dataclass
class RawImageMetadata:
    """
    Output dari ImageExtractor.
    Berisi informasi TEKNIS gambar — belum ada makna pedagogis.
    Figure extractor yang akan menambah makna di atasnya.
    """
    # Identifikasi
    image_id: str                    # hash unik berdasarkan content
    xref: int                        # PDF internal reference
    
    # Lokasi dalam dokumen
    page_number: int                 # 1-indexed
    page_width: float                # lebar halaman (points)
    page_height: float               # tinggi halaman (points)
    bbox: List[float]                # [x0, y0, x1, y1] dalam page coordinates
    bbox_normalized: List[float]     # [0-1, 0-1, 0-1, 0-1] relatif terhadap halaman
    
    # Properti teknis
    format: str                      # png, jpeg, webp, dll
    width_px: int                    # lebar dalam pixel
    height_px: int                   # tinggi dalam pixel
    color_space: ImageColorspace
    bits_per_component: int
    file_size_bytes: int
    aspect_ratio: float
    
    # Klasifikasi awal (low-level)
    image_type: ImageType
    is_likely_noise: bool            # True jika kemungkinan besar dekoratif/noise
    noise_reason: Optional[str]      # alasan dianggap noise
    
    # Data mentah (untuk downstream)
    image_bytes: Optional[bytes]     # raw bytes (bisa None jika tidak diminta)
    image_base64: Optional[str]      # base64 (bisa None jika tidak diminta)
    
    # Context clues untuk figure_extractor
    surrounding_text_above: str = ""  # teks 3 baris di atas gambar
    surrounding_text_below: str = ""  # teks 3 baris di bawah gambar
    has_caption_candidate: bool = False  # ada kandidat caption di sekitar?
    
    # Deduplication
    content_hash: str = ""          # MD5 dari image bytes
    is_duplicate: bool = False      # sudah muncul di halaman lain?


@dataclass 
class ImageExtractionResult:
    """Hasil keseluruhan ekstraksi dari satu dokumen"""
    file_path: str
    total_pages: int
    total_images_found: int
    total_images_extracted: int
    total_skipped_small: int
    total_skipped_noise: int
    total_duplicates: int
    images: List[RawImageMetadata] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class ImageExtractor:
    """
    LOW-LEVEL image extractor dari PDF.
    
    Tanggung jawab:
    - Temukan semua gambar dalam PDF
    - Ekstrak bytes & metadata teknis
    - Dapatkan posisi AKURAT di halaman
    - Ambil surrounding text untuk konteks
    - Klasifikasi awal (raster/vector/scanned/decorative)
    - Deduplication berdasarkan content hash
    
    BUKAN tanggung jawab:
    - Interpretasi makna gambar (→ figure_extractor.py)
    - Caption understanding (→ figure_extractor.py)
    - Pedagogical classification (→ figure_extractor.py)
    - Upload ke MinIO (→ storage_service.py)
    """

    # Threshold konfigurasi
    DEFAULT_MIN_SIZE_PX    = 100      # pixel minimum width/height
    DEFAULT_MIN_SIZE_RATIO = 0.02     # min 2% dari dimensi halaman
    CAPTION_SEARCH_RADIUS  = 60       # points di atas/bawah untuk cari caption
    SURROUNDING_TEXT_LINES = 3        # jumlah baris konteks
    
    # Noise detection thresholds
    NOISE_MAX_SIZE_PX      = 50       # gambar < 50px hampir pasti icon/bullet
    NOISE_COVERAGE_RATIO   = 0.85     # gambar yang cover > 85% halaman = background

    def __init__(
        self,
        min_size_px: int = DEFAULT_MIN_SIZE_PX,
        min_size_ratio: float = DEFAULT_MIN_SIZE_RATIO,
        extract_bytes: bool = True,
        extract_base64: bool = False,
        extract_surrounding_text: bool = True,
        skip_noise: bool = True,
        deduplicate: bool = True,
    ):
        self.min_size_px = min_size_px
        self.min_size_ratio = min_size_ratio
        self.extract_bytes = extract_bytes
        self.extract_base64 = extract_base64
        self.extract_surrounding_text = extract_surrounding_text
        self.skip_noise = skip_noise
        self.deduplicate = deduplicate
        
        self._seen_hashes: Dict[str, str] = {}  # hash → image_id pertama kali ditemukan

    # ─────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────

    def extract(
        self,
        file_path: str,
        page_range: Optional[Tuple[int, int]] = None,
    ) -> ImageExtractionResult:
        """
        Ekstrak semua gambar dari PDF.
        
        Args:
            file_path: Path ke file PDF
            page_range: Opsional (start, end) 1-indexed, inclusive
            
        Returns:
            ImageExtractionResult dengan semua metadata
        """
        result = ImageExtractionResult(
            file_path=file_path,
            total_pages=0,
            total_images_found=0,
            total_images_extracted=0,
            total_skipped_small=0,
            total_skipped_noise=0,
            total_duplicates=0,
        )

        if not Path(file_path).exists():
            result.errors.append(f"File tidak ditemukan: {file_path}")
            return result

        if Path(file_path).suffix.lower() != '.pdf':
            result.errors.append(f"Hanya PDF yang didukung, got: {file_path}")
            return result

        try:
            doc = fitz.open(file_path)
            result.total_pages = doc.page_count

            start_page = (page_range[0] - 1) if page_range else 0
            end_page   = page_range[1] if page_range else doc.page_count

            for page_num in range(start_page, min(end_page, doc.page_count)):
                page = doc[page_num]
                page_images = self._extract_from_page(doc, page, page_num + 1)
                
                for img_meta in page_images:
                    result.total_images_found += 1

                    if img_meta.is_likely_noise and self.skip_noise:
                        result.total_skipped_noise += 1
                        logger.debug(
                            f"Skip noise image hal.{page_num+1}: {img_meta.noise_reason}"
                        )
                        continue

                    if img_meta.is_duplicate and self.deduplicate:
                        result.total_duplicates += 1
                        logger.debug(
                            f"Skip duplicate image hal.{page_num+1} "
                            f"(pertama kali di: {self._seen_hashes.get(img_meta.content_hash)})"
                        )
                        continue

                    result.images.append(img_meta)
                    result.total_images_extracted += 1

            doc.close()
            logger.info(
                f"Ekstraksi selesai: {result.total_images_extracted} gambar "
                f"dari {result.total_pages} halaman "
                f"({result.total_skipped_noise} noise, "
                f"{result.total_duplicates} duplikat dilewati)"
            )

        except Exception as e:
            msg = f"Error membuka PDF {file_path}: {str(e)}"
            logger.error(msg)
            result.errors.append(msg)

        return result

    # ─────────────────────────────────────────────
    # PRIVATE: Per-page extraction
    # ─────────────────────────────────────────────

    def _extract_from_page(
        self,
        doc: fitz.Document,
        page: fitz.Page,
        page_num: int,
    ) -> List[RawImageMetadata]:
        """Ekstrak semua gambar dari satu halaman"""
        results = []
        page_rect = page.rect
        page_w = page_rect.width
        page_h = page_rect.height

        for img_info in page.get_images(full=True):
            xref = img_info[0]
            
            try:
                # Ambil data mentah
                base_image = doc.extract_image(xref)
                img_bytes  = base_image["image"]
                img_w      = base_image["width"]
                img_h      = base_image["height"]
                img_fmt    = base_image["ext"]
                img_cs     = base_image.get("colorspace", 0)
                img_bpc    = base_image.get("bpc", 8)

                # ── Size filter ──────────────────────────
                if img_w < self.min_size_px or img_h < self.min_size_px:
                    result = self._make_skipped(
                        xref, page_num, img_w, img_h,
                        "terlalu kecil (pixel)"
                    )
                    results.append(result)
                    continue

                # ── Dapatkan posisi AKURAT di halaman ──
                bbox, bbox_norm = self._get_accurate_bbox(page, xref, page_w, page_h)

                # ── Content hash untuk dedup ─────────────
                content_hash = hashlib.md5(img_bytes).hexdigest()
                is_duplicate = content_hash in self._seen_hashes
                if not is_duplicate:
                    image_id = f"img_p{page_num}_{xref}_{content_hash[:8]}"
                    self._seen_hashes[content_hash] = image_id
                else:
                    image_id = f"img_p{page_num}_{xref}_dup_{content_hash[:8]}"

                # ── Klasifikasi low-level ─────────────────
                image_type = self._classify_image_type(
                    img_w, img_h, img_cs, img_bpc, bbox_norm, page_w, page_h
                )

                # ── Noise detection ───────────────────────
                is_noise, noise_reason = self._detect_noise(
                    img_w, img_h, bbox_norm, image_type, img_bytes
                )

                # ── Surrounding text ──────────────────────
                text_above = ""
                text_below = ""
                has_caption = False
                if self.extract_surrounding_text and bbox:
                    text_above, text_below, has_caption = \
                        self._get_surrounding_text(page, bbox)

                # ── Bangun metadata ───────────────────────
                metadata = RawImageMetadata(
                    image_id        = image_id,
                    xref            = xref,
                    page_number     = page_num,
                    page_width      = page_w,
                    page_height     = page_h,
                    bbox            = bbox or [0.0, 0.0, page_w, page_h],
                    bbox_normalized = bbox_norm or [0.0, 0.0, 1.0, 1.0],
                    format          = img_fmt,
                    width_px        = img_w,
                    height_px       = img_h,
                    color_space     = self._map_colorspace(img_cs),
                    bits_per_component = img_bpc,
                    file_size_bytes = len(img_bytes),
                    aspect_ratio    = img_w / img_h if img_h > 0 else 0,
                    image_type      = image_type,
                    is_likely_noise = is_noise,
                    noise_reason    = noise_reason,
                    image_bytes     = img_bytes if self.extract_bytes else None,
                    image_base64    = (
                        base64.b64encode(img_bytes).decode() 
                        if self.extract_base64 else None
                    ),
                    surrounding_text_above  = text_above,
                    surrounding_text_below  = text_below,
                    has_caption_candidate   = has_caption,
                    content_hash    = content_hash,
                    is_duplicate    = is_duplicate,
                )

                results.append(metadata)
                logger.debug(
                    f"  Gambar hal.{page_num}: {img_w}x{img_h} "
                    f"{image_type.value} noise={is_noise}"
                )

            except Exception as e:
                logger.warning(
                    f"Error ekstraksi gambar xref={xref} hal.{page_num}: {e}"
                )
                continue

        return results

    # ─────────────────────────────────────────────
    # PRIVATE: Bbox yang akurat
    # ─────────────────────────────────────────────

    def _get_accurate_bbox(
        self,
        page: fitz.Page,
        xref: int,
        page_w: float,
        page_h: float,
    ) -> Tuple[Optional[List[float]], Optional[List[float]]]:
        """
        Dapatkan bounding box AKURAT dari gambar di halaman.
        
        Menggunakan get_image_rects() yang lebih akurat dari
        pendekatan manual sebelumnya.
        """
        try:
            # Cara terbaik — PyMuPDF menyediakan ini sejak v1.18
            rects = page.get_image_rects(xref)
            if rects:
                rect = rects[0]  # ambil occurrence pertama
                bbox = [rect.x0, rect.y0, rect.x1, rect.y1]
                bbox_norm = [
                    rect.x0 / page_w,
                    rect.y0 / page_h,
                    rect.x1 / page_w,
                    rect.y1 / page_h,
                ]
                return bbox, bbox_norm

        except AttributeError:
            # Fallback untuk PyMuPDF versi lama
            pass

        try:
            # Fallback: cari via get_images(full=True) dan matrix
            for img in page.get_images(full=True):
                if img[0] == xref:
                    # img[7] = transform matrix jika tersedia
                    # Ini estimasi, tidak seakurat get_image_rects
                    clip = img[10] if len(img) > 10 else None
                    if clip and hasattr(clip, 'x0'):
                        bbox = [clip.x0, clip.y0, clip.x1, clip.y1]
                        bbox_norm = [
                            clip.x0 / page_w,
                            clip.y0 / page_h,
                            clip.x1 / page_w,
                            clip.y1 / page_h,
                        ]
                        return bbox, bbox_norm
        except Exception:
            pass

        logger.debug(f"Tidak bisa dapatkan bbox akurat untuk xref={xref}")
        return None, None

    # ─────────────────────────────────────────────
    # PRIVATE: Surrounding text untuk konteks caption
    # ─────────────────────────────────────────────

    def _get_surrounding_text(
        self,
        page: fitz.Page,
        bbox: List[float],
    ) -> Tuple[str, str, bool]:
        """
        Ambil teks di atas dan di bawah gambar.
        Berguna untuk figure_extractor mencari caption.
        
        Returns:
            (text_above, text_below, has_caption_candidate)
        """
        try:
            x0, y0, x1, y1 = bbox
            
            # Area di atas gambar
            above_rect = fitz.Rect(
                x0 - 20,                        # sedikit lebih lebar
                max(0, y0 - self.CAPTION_SEARCH_RADIUS),
                x1 + 20,
                y0
            )
            
            # Area di bawah gambar
            below_rect = fitz.Rect(
                x0 - 20,
                y1,
                x1 + 20,
                min(page.rect.height, y1 + self.CAPTION_SEARCH_RADIUS)
            )

            text_above = page.get_text("text", clip=above_rect).strip()
            text_below = page.get_text("text", clip=below_rect).strip()

            # Deteksi kandidat caption
            # Caption biasanya diawali "Gambar X", "Foto X", "Grafik X", dll
            caption_keywords = [
                "gambar", "foto", "grafik", "tabel", "bagan",
                "diagram", "ilustrasi", "figure", "fig.", "gb."
            ]
            combined = (text_above + " " + text_below).lower()
            has_caption = any(kw in combined for kw in caption_keywords)

            return text_above, text_below, has_caption

        except Exception as e:
            logger.debug(f"Error ambil surrounding text: {e}")
            return "", "", False

    # ─────────────────────────────────────────────
    # PRIVATE: Klasifikasi dan noise detection
    # ─────────────────────────────────────────────

    def _classify_image_type(
        self,
        width: int,
        height: int,
        colorspace: int,
        bpc: int,
        bbox_norm: Optional[List[float]],
        page_w: float,
        page_h: float,
    ) -> ImageType:
        """
        Klasifikasi LOW-LEVEL berdasarkan properti teknis.
        Bukan klasifikasi pedagogis — itu tugas figure_extractor.
        """
        # Gambar grayscale 1-bit biasanya hasil scan
        if colorspace == 1 and bpc == 1:
            if bbox_norm:
                coverage = (bbox_norm[2] - bbox_norm[0]) * (bbox_norm[3] - bbox_norm[1])
                if coverage > 0.7:
                    return ImageType.SCANNED_PAGE
                else:
                    return ImageType.SCANNED_REGION
            return ImageType.SCANNED_PAGE

        # Gambar yang hampir cover seluruh halaman
        if bbox_norm:
            coverage = (bbox_norm[2] - bbox_norm[0]) * (bbox_norm[3] - bbox_norm[1])
            if coverage > 0.8:
                return ImageType.SCANNED_PAGE

        # Default: embedded raster
        return ImageType.RASTER_EMBEDDED

    def _detect_noise(
        self,
        width: int,
        height: int,
        bbox_norm: Optional[List[float]],
        image_type: ImageType,
        image_bytes: bytes,
    ) -> Tuple[bool, Optional[str]]:
        """
        Deteksi apakah gambar kemungkinan besar noise/dekoratif.
        Gambar noise tidak akan diteruskan ke figure_extractor.
        """
        # Gambar sangat kecil → ikon, bullet, ornamen kecil
        if width < self.NOISE_MAX_SIZE_PX and height < self.NOISE_MAX_SIZE_PX:
            return True, f"ukuran terlalu kecil ({width}x{height}px)"

        # Gambar sangat tipis → garis dekoratif, divider
        aspect = width / height if height > 0 else 0
        if aspect > 20 or (aspect < 0.05 and aspect > 0):
            return True, f"rasio sangat ekstrem (kemungkinan garis/divider): {aspect:.1f}"

        # File size sangat kecil → kemungkinan solid color / ornamen
        if len(image_bytes) < 500:
            return True, f"file size sangat kecil ({len(image_bytes)} bytes)"

        return False, None

    def _map_colorspace(self, cs_code: int) -> ImageColorspace:
        mapping = {
            1: ImageColorspace.GRAY,
            2: ImageColorspace.RGB,       # sebenarnya bisa beda-beda
            3: ImageColorspace.RGB,
            4: ImageColorspace.CMYK,
        }
        return mapping.get(cs_code, ImageColorspace.UNKNOWN)

    def _make_skipped(
        self,
        xref: int,
        page_num: int,
        w: int,
        h: int,
        reason: str,
    ) -> RawImageMetadata:
        """Buat metadata untuk gambar yang di-skip"""
        return RawImageMetadata(
            image_id    = f"img_skip_p{page_num}_{xref}",
            xref        = xref,
            page_number = page_num,
            page_width  = 0, page_height = 0,
            bbox        = [], bbox_normalized = [],
            format      = "unknown",
            width_px    = w, height_px = h,
            color_space = ImageColorspace.UNKNOWN,
            bits_per_component = 0,
            file_size_bytes    = 0,
            aspect_ratio       = w / h if h > 0 else 0,
            image_type    = ImageType.UNKNOWN,
            is_likely_noise = True,
            noise_reason    = reason,
            image_bytes   = None,
            image_base64  = None,
            content_hash  = "",
            is_duplicate  = False,
        )