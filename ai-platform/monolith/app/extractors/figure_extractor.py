"""
FigureExtractor - High-Level Pedagogical Figure Interpretation

Menginterpretasi gambar dalam konteks pendidikan Kurikulum Merdeka.
Beda dengan ImageExtractor yang hanya ekstrak data teknis.
"""

import logging
from enum import Enum
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field
import re
import fitz  # PyMuPDF

from app.extractors.image_extractor import (
    RawImageMetadata, 
    ImageType, 
    ImageColorspace
)
from app.models.document_models import Region, BoundingBox

logger = logging.getLogger(__name__)


class FigureType(str, Enum):
    """
    Klasifikasi HIGH-LEVEL berdasarkan makna pedagogis.
    Ini beda dengan ImageType yang hanya teknis (raster/vector).
    """
    # Illustrasi pembelajaran
    ILLUSTRATION = "illustration"           # Ilustrasi umum pembelajaran
    DIAGRAM = "diagram"                     # Diagram konsep/proses
    CHART = "chart"                         # Grafik/statistik
    MAP = "map"                             # Peta/geografi
    TIMELINE = "timeline"                  # Timeline/kronologi
    
    # Gambar dokumentasi
    PHOTO = "photo"                         # Foto dokumentasi kegiatan
    PORTRAIT = "portrait"                   # Potret tokoh/figur
    
    # Visual aids matematika/sains
    GEOMETRIC_SHAPE = "geometric_shape"    # Bangun geometri
    SCIENTIFIC_MODEL = "scientific_model"  # Model ilmiah (atom, dll)
    MATHEMATICAL = "mathematical"          # Visual matematika (graph, dll)
    
    # Infographics
    INFOGRAPHIC = "infographic"             # Infographic
    FLOWCHART = "flowchart"                # Flowchart/alur
    
    # Spesifik Kurikulum Merdeka
    P5_PROJECT = "p5_project"              # Visual dari projek P5
    ASESMEN_VISUAL = "asesmen_visual"       # Visual asesmen/portofolio
    LEARNING_RESOURCE = "learning_resource" # Sumber belajar visual
    
    # Unknown/other
    UNKNOWN = "unknown"


class FigureRole(str, Enum):
    """
    Peran figure dalam konteks pembelajaran.
    """
    PRIMARY = "primary"       # Gambar utama (focus of attention)
    SECONDARY = "secondary"   # Gambar pendukung
    BACKGROUND = "background" # Background/decorative
    NAVIGATION = "navigation" # Visual untuk navigasi
    ASSESSMENT = "assessment" # Gambar untuk asesmen/portofolio


class FigureSubject(str, Enum):
    """
    Klasifikasi berdasarkan mata pelajaran.
    """
    IPA = "ipa"           # Ilmu Pengetahuan Alam
    IPS = "ips"           # Ilmu Pengetahuan Sosial
    MATEMATIKA = "matematika"
    BAHASA_INDONESIA = "bahasa_indonesia"
    BAHASA_INGGRIS = "bahasa_inggris"
    PJOK = "pjok"         # Pendidikan Jasmani
    SENI_BUDAYA = "seni_budaya"
    PPKN = "ppkn"
    AGAMA = "agama"
    IPAS = "ipas"         # Integrated (SD)
    SBDP = "sbdp"         # Seni Budaya & Prakarya Kreatif (SD)
    P5 = "p5"             # Projek Penguatan Profil Pelajar Pancasila
    UNKNOWN = "unknown"


@dataclass
class FigureMetadata:
    """
    High-level figure metadata dengan interpretasi pedagogis.
    Dibangun di atas RawImageMetadata.
    """
    # Inherit dari RawImageMetadata
    image_id: str
    page_number: int
    bbox: List[float]
    width_px: int
    height_px: int
    minio_key: Optional[str]
    
    # High-level classification
    figure_type: FigureType
    figure_role: FigureRole
    figure_subject: FigureSubject
    
    # Caption & text context
    caption: Optional[str] = None
    caption_confidence: float = 0.0  # 0-1, confidence ini caption yang benar
    caption_position: Optional[str] = None  # "above", "below", "inside"
    
    # Description dari Vision API (akan diisi oleh Vision Service)
    ai_description: Optional[str] = None
    ai_confidence: float = 0.0
    
    # Contextual understanding
    contextual_relevance: float = 0.0  # Relevance dengan konteks halaman
    learning_objective_alignment: float = 0.0  # Alignment dengan tujuan pembelajaran
    
    # Pedagogical significance
    is_essential: bool = False  # Essential untuk pemahaman materi
    is_supplementary: bool = False  # Suplementary (opsional)
    is_assessment_related: bool = False  # Terkait asesmen/portofolio
    is_p5_related: bool = False  # Terkait projek P5
    
    # Additional metadata
    detected_elements: List[str] = field(default_factory=list)  # Elemen yang terdeteksi
    educational_keywords: List[str] = field(default_factory=list)  # Keywords pendidikan
    difficulty_level: Optional[str] = None  # mudah/sedang/sulit
    
    # Source & attribution
    source: Optional[str] = None  # Sumber gambar (credit)
    is_original: bool = True  # Original atau dari sumber lain


@dataclass
class FigureExtractionResult:
    """Hasil keseluruhan figure extraction dari satu dokumen"""
    doc_id: Optional[str]
    file_path: str
    total_images: int
    total_figures: int
    figures: List[FigureMetadata] = field(default_factory=list)
    by_type: Dict[FigureType, int] = field(default_factory=dict)
    by_role: Dict[FigureRole, int] = field(default_factory=dict)
    by_subject: Dict[FigureSubject, int] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


class FigureExtractor:
    """
    HIGH-LEVEL figure extractor dengan interpretasi pedagogis.
    
    NEW: Region-aware extraction for modern pipeline.
    
    Tanggung jawab:
    - Interpretasi makna gambar dalam konteks pendidikan
    - Klasifikasi figure type (diagram, illustration, dll)
    - Extract dan validate captions
    - Determine relevance dengan konteks pembelajaran
    - P5 detection untuk Kurikulum Merdeka
    
    BUKAN tanggung jawab:
    - Ekstrak gambar teknis (→ image_extractor.py)
    - Vision AI processing (→ vision-service)
    - Upload ke MinIO (→ image_extractor.py sudah handle)
    """

    # Caption detection keywords
    CAPTION_PREFIXES = [
        "gambar", "foto", "ilustrasi", "diagram", "grafik", 
        "tabel", "bagel", "bagan", "figure", "fig.", "gb."
    ]
    
    # Kurikulum Merdeka specific patterns
    P5_KEYWORDS = [
        "p5", "projek", "profil pelajar pancasila", "penguatan profil",
        "projek penguatan profil pelajar pancasila"
    ]
    
    # Subject classification keywords
    SUBJECT_KEYWORDS = {
        FigureSubject.IPA: [
            "sains", "ipa", "biologi", "fisika", "kimia", "alam",
            "hewan", "tumbuhan", "ekosistem", "organisme"
        ],
        FigureSubject.IPS: [
            "sejarah", "ips", "geografi", "sosiologi", "ekonomi",
            "masyarakat", "budaya", "wilayah", "daerah"
        ],
        FigureSubject.MATEMATIKA: [
            "matematika", "angka", "hitung", "geometri", "aljabar",
            "kalkulasi", "operasi", "rasio", "persentase"
        ],
        FigureSubject.BAHASA_INDONESIA: [
            "bahasa", "teks", "puisi", "cerpen", "novel", "drama"
        ],
        FigureSubject.BAHASA_INGGRIS: [
            "english", "inggris", "language", "english text"
        ],
        FigureSubject.PJOK: [
            "olahraga", "pjok", "gerak", "aktivitas fisik", "sport"
        ],
        FigureSubject.SENI_BUDAYA: [
            "seni", "budaya", "musik", "lukis", "tari", "karya"
        ],
        FigureSubject.PPKN: [
            "ppkn", "pkn", "civics", "kewarganegaraan", "pancasila", "bhinneka"
        ],
        FigureSubject.AGAMA: [
            "agama", "islam", "kristen", "katolik", "hindu", "buddha", "konghucu"
        ],
    }

    def __init__(
        self,
        detect_captions: bool = True,
        classify_subject: bool = True,
        detect_p5: bool = True,
    ):
        self.detect_captions = detect_captions
        self.classify_subject = classify_subject
        self.detect_p5 = detect_p5
    
    def extract_from_region(
        self, 
        region: Region, 
        page: fitz.Page,
        options: Optional[Dict[str, Any]] = None
    ) -> Optional[FigureMetadata]:
        """
        Extract figure content from a specific region (region-aware).
        
        This is the NEW method for the modern pipeline.
        
        Args:
            region: Region object with bounding box
            page: PyMuPDF page object
            options: Extraction options
            
        Returns:
            Figure metadata for this specific region
        """
        try:
            options = options or {}
            
            # Check if region is actually a figure
            if region.region_type.value not in ['figure', 'image']:
                return None
            
            # Create basic figure metadata from region
            figure = FigureMetadata(
                image_id=f"{region.region_id}_figure",
                page_number=region.page_number,
                bbox=region.bbox.to_list(),
                width_px=int(region.bbox.width),
                height_px=int(region.bbox.height),
                minio_key=None,  # Would be set by image extractor
                figure_type=FigureType.ILLUSTRATION,  # Default
                figure_role=FigureRole.SECONDARY,  # Default
                figure_subject=FigureSubject.UNKNOWN,  # Default
            )
            
            # Classify figure type based on context
            figure.figure_type = self._classify_figure_type_from_region(region)
            
            # Classify figure role
            figure.figure_role = self._classify_figure_role_from_region(region)
            
            # Classify subject if enabled
            if self.classify_subject:
                figure.figure_subject = self._classify_figure_subject_from_region(region)
            
            # Extract caption if enabled
            if self.detect_captions:
                figure.caption = self._extract_caption_from_region(region)
                figure.caption_confidence = 0.7 if figure.caption else 0.0
                figure.caption_position = "below"  # Default assumption
            
            # Detect P5 relevance if enabled
            if self.detect_p5:
                figure.is_p5_related = self._detect_p5_from_region(region)
            
            # Determine educational significance
            self._determine_significance_from_region(figure, region)
            
            logger.info(f"Extracted figure from region {region.region_id}: {figure.figure_type.value}")
            
            return figure
            
        except Exception as e:
            logger.error(f"Error extracting figure from region {region.region_id}: {e}")
            return None
    
    def _classify_figure_type_from_region(self, region: Region) -> FigureType:
        """Classify figure type based on region content"""
        text = region.text_content.lower() if region.text_content else ""
        
        # Check for diagram keywords
        if any(kw in text for kw in ['diagram', 'bagel', 'bagan', 'skema']):
            return FigureType.DIAGRAM
        
        # Check for chart keywords
        if any(kw in text for kw in ['grafik', 'chart', 'statistik', 'data']):
            return FigureType.CHART
        
        # Check for map keywords
        if any(kw in text for kw in ['peta', 'map', 'wilayah', 'daerah']):
            return FigureType.MAP
        
        # Check for timeline keywords
        if any(kw in text for kw in ['timeline', 'kronologi', 'garis waktu']):
            return FigureType.TIMELINE
        
        # Check for geometric keywords
        if any(kw in text for kw in ['geometri', 'bangun', 'segi', 'lingkaran']):
            return FigureType.GEOMETRIC_SHAPE
        
        # Default to illustration
        return FigureType.ILLUSTRATION
    
    def _classify_figure_role_from_region(self, region: Region) -> FigureRole:
        """Classify figure role based on region position and context"""
        # Check if figure is large (likely primary)
        if region.bbox.width > 300 and region.bbox.height > 300:
            return FigureRole.PRIMARY
        
        # Check if figure is small (likely secondary)
        if region.bbox.width < 100 or region.bbox.height < 100:
            return FigureRole.BACKGROUND
        
        # Default to secondary
        return FigureRole.SECONDARY
    
    def _classify_figure_subject_from_region(self, region: Region) -> FigureSubject:
        """Classify figure subject based on region content"""
        text = region.text_content.lower() if region.text_content else ""
        
        for subject, keywords in self.SUBJECT_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return subject
        
        return FigureSubject.UNKNOWN
    
    def _extract_caption_from_region(self, region: Region) -> Optional[str]:
        """Extract caption from region metadata or surrounding text"""
        # Check if caption is in metadata
        if region.metadata and 'caption' in region.metadata:
            return region.metadata['caption']
        
        # Check surrounding text for caption patterns
        text = region.text_content or ""
        for prefix in self.CAPTION_PREFIXES:
            if prefix in text.lower():
                # Extract text after prefix
                idx = text.lower().find(prefix)
                caption = text[idx + len(prefix):].strip()
                if len(caption) > 5:  # Minimum caption length
                    return caption
        
        return None
    
    def _detect_p5_from_region(self, region: Region) -> bool:
        """Detect if figure is related to P5 project"""
        text = region.text_content.lower() if region.text_content else ""
        return any(kw in text for kw in self.P5_KEYWORDS)
    
    def _determine_significance_from_region(self, figure: FigureMetadata, region: Region):
        """Determine educational significance of figure"""
        # Large figures are more likely essential
        if region.bbox.width > 300 and region.bbox.height > 300:
            figure.is_essential = True
        
        # Figures with captions are more significant
        if figure.caption:
            figure.is_supplementary = True
    
    # ─────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────

    def extract_figures(
        self,
        raw_images: List[RawImageMetadata],
        doc_context: Optional[Dict[str, Any]] = None,
    ) -> FigureExtractionResult:
        """
        Convert raw images ke figures dengan interpretasi pedagogis.
        
        Args:
            raw_images: List dari ImageExtractor output
            doc_context: Context dokumen (title, subject, grade, dll)
            
        Returns:
            FigureExtractionResult dengan figure metadata
        """
        result = FigureExtractionResult(
            doc_id=doc_context.get("doc_id") if doc_context else None,
            file_path=doc_context.get("file_path", "") if doc_context else "",
            total_images=len(raw_images),
            total_figures=0,
        )
        
        doc_context = doc_context or {}
        
        for raw_img in raw_images:
            try:
                # Skip jika noise
                if raw_img.is_likely_noise:
                    continue
                
                # Convert ke FigureMetadata
                figure = self._convert_to_figure(raw_img, doc_context)
                
                # Classify
                figure.figure_type = self._classify_figure_type(raw_img, doc_context)
                figure.figure_role = self._classify_figure_role(raw_img, doc_context)
                
                if self.classify_subject:
                    figure.figure_subject = self._classify_figure_subject(raw_img, doc_context)
                
                # Extract caption
                if self.detect_captions:
                    figure.caption = self._extract_caption(raw_img)
                    figure.caption_confidence = self._calculate_caption_confidence(raw_img, figure.caption)
                    figure.caption_position = self._detect_caption_position(raw_img, figure.caption)
                
                # Detect P5 relevance
                if self.detect_p5:
                    figure.is_p5_related = self._detect_p5_relevance(raw_img, doc_context)
                
                # Determine educational significance
                self._determine_significance(figure, doc_context)
                
                result.figures.append(figure)
                result.total_figures += 1
                
                # Update counts
                result.by_type[figure.figure_type] = result.by_type.get(figure.figure_type, 0) + 1
                result.by_role[figure.figure_role] = result.by_role.get(figure.figure_role, 0) + 1
                result.by_subject[figure.figure_subject] = result.by_subject.get(figure.figure_subject, 0) + 1
                
                logger.debug(
                    f"Figure {figure.image_id}: {figure.figure_type.value} "
                    f"({figure.figure_subject.value}, role={figure.figure_role.value})"
                )
                
            except Exception as e:
                logger.warning(f"Error processing figure {raw_img.image_id}: {e}")
                result.errors.append(f"{raw_img.image_id}: {str(e)}")
                continue
        
        logger.info(
            f"Figure extraction selesai: {result.total_figures} figures "
            f"dari {result.total_images} images"
        )
        
        return result
    
    # ─────────────────────────────────────────────
    # PRIVATE: Conversion & Classification
    # ─────────────────────────────────────────────

    def _convert_to_figure(
        self,
        raw_img: RawImageMetadata,
        doc_context: Dict[str, Any]
    ) -> FigureMetadata:
        """Convert RawImageMetadata ke FigureMetadata"""
        return FigureMetadata(
            image_id=raw_img.image_id,
            page_number=raw_img.page_number,
            bbox=raw_img.bbox,
            width_px=raw_img.width_px,
            height_px=raw_img.height_px,
            minio_key=raw_img.minio_key,
            figure_type=FigureType.UNKNOWN,
            figure_role=FigureRole.SECONDARY,
            figure_subject=FigureSubject.UNKNOWN,
        )
    
    def _classify_figure_type(
        self,
        raw_img: RawImageMetadata,
        doc_context: Dict[str, Any]
    ) -> FigureType:
        """
        Classify figure type berdasarkan teknis + context.
        Ini simplifikasi - versi production akan pakai Vision AI.
        """
        # Heuristics based on aspect ratio dan context
        aspect = raw_img.aspect_ratio
        
        # Wide images → charts/infographics/diagrams
        if aspect > 3.0:
            return FigureType.INFOGRAPHIC
        elif aspect > 2.0:
            return FigureType.CHART
        
        # Tall images → timelines/flowcharts
        if aspect < 0.4:
            return FigureType.FLOWCHART
        
        # Square-ish → illustrations/photos
        if 0.8 <= aspect <= 1.2:
            if raw_img.color_space == ImageColorspace.GRAY:
                return FigureType.DIAGRAM
            else:
                return FigureType.ILLUSTRATION
        
        # Color images → photos/illustrations
        if raw_img.color_space == ImageColorspace.RGB:
            if raw_img.width_px > 1000 or raw_img.height_px > 1000:
                return FigureType.PHOTO
            return FigureType.ILLUSTRATION
        
        # Default
        return FigureType.ILLUSTRATION
    
    def _classify_figure_role(
        self,
        raw_img: RawImageMetadata,
        doc_context: Dict[str, Any]
    ) -> FigureRole:
        """Classify figure role dalam konteks pembelajaran"""
        # Large images → primary
        if raw_img.width_px > 800 and raw_img.height_px > 600:
            return FigureRole.PRIMARY
        
        # Small images → secondary
        if raw_img.width_px < 200 or raw_img.height_px < 200:
            return FigureRole.SECONDARY
        
        # Has caption candidate → likely primary
        if raw_img.has_caption_candidate:
            return FigureRole.PRIMARY
        
        # Default
        return FigureRole.SECONDARY
    
    def _classify_figure_subject(
        self,
        raw_img: RawImageMetadata,
        doc_context: Dict[str, Any]
    ) -> FigureSubject:
        """
        Classify figure subject berdasarkan context text + caption.
        """
        # Check doc context subject
        if doc_context:
            subject_str = doc_context.get("subject", "").lower()
            for subject, keywords in self.SUBJECT_KEYWORDS.items():
                if any(kw in subject_str for kw in keywords):
                    return subject
        
        # Check surrounding text
        combined_text = (
            raw_img.surrounding_text_above.lower() + " " +
            raw_img.surrounding_text_below.lower()
        )
        
        for subject, keywords in self.SUBJECT_KEYWORDS.items():
            if any(kw in combined_text for kw in keywords):
                return subject
        
        # Default
        return FigureSubject.UNKNOWN
    
    # ─────────────────────────────────────────────
    # PRIVATE: Caption Extraction
    # ─────────────────────────────────────────────

    def _extract_caption(self, raw_img: RawImageMetadata) -> Optional[str]:
        """Extract caption dari surrounding text"""
        text_above = raw_img.surrounding_text_above.strip()
        text_below = raw_img.surrounding_text_below.strip()
        
        # Caption biasanya di bawah
        if text_below:
            # Cek apakah ada caption prefix
            for prefix in self.CAPTION_PREFIXES:
                if text_below.lower().startswith(prefix):
                    # Remove prefix dan number (e.g., "Gambar 1: ")
                    caption = re.sub(
                        rf'^{re.escape(prefix)}\s*\d+[:\.-]?\s*', 
                        '', 
                        text_below, 
                        flags=re.IGNORECASE
                    )
                    return caption.strip()
            
            # Jika tidak ada prefix tapi ada caption candidate
            if raw_img.has_caption_candidate:
                return text_below
        
        # Cek teks di atas sebagai fallback
        if text_above:
            for prefix in self.CAPTION_PREFIXES:
                if text_above.lower().startswith(prefix):
                    caption = re.sub(
                        rf'^{re.escape(prefix)}\s*\d+[:\.-]?\s*', 
                        '', 
                        text_above, 
                        flags=re.IGNORECASE
                    )
                    return caption.strip()
        
        return None
    
    def _calculate_caption_confidence(
        self,
        raw_img: RawImageMetadata,
        caption: Optional[str]
    ) -> float:
        """Calculate confidence bahwa ini caption yang benar"""
        if not caption:
            return 0.0
        
        confidence = 0.0
        
        # Ada caption prefix → higher confidence
        for prefix in self.CAPTION_PREFIXES:
            if caption.lower().startswith(prefix):
                confidence += 0.5
                break
        
        # Caption reasonable length (10-200 chars)
        if 10 <= len(caption) <= 200:
            confidence += 0.3
        
        # Caption di bawah gambar → higher confidence
        if raw_img.surrounding_text_below and caption in raw_img.surrounding_text_below:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _detect_caption_position(
        self,
        raw_img: RawImageMetadata,
        caption: Optional[str]
    ) -> Optional[str]:
        """Detect posisi caption relatif terhadap gambar"""
        if not caption:
            return None
        
        if caption in raw_img.surrounding_text_below:
            return "below"
        elif caption in raw_img.surrounding_text_above:
            return "above"
        else:
            return "unknown"
    
    # ─────────────────────────────────────────────
    # PRIVATE: P5 Detection & Significance
    # ─────────────────────────────────────────────

    def _detect_p5_relevance(
        self,
        raw_img: RawImageMetadata,
        doc_context: Dict[str, Any]
    ) -> bool:
        """Detect apakah figure terkait Projek P5"""
        # Check doc context
        if doc_context:
            context_str = str(doc_context).lower()
            if any(kw in context_str for kw in self.P5_KEYWORDS):
                return True
        
        # Check surrounding text
        combined_text = (
            raw_img.surrounding_text_above.lower() + " " +
            raw_img.surrounding_text_below.lower()
        )
        
        return any(kw in combined_text for kw in self.P5_KEYWORDS)
    
    def _determine_significance(
        self,
        figure: FigureMetadata,
        doc_context: Dict[str, Any]
    ) -> None:
        """
        Determine educational significance dari figure.
        """
        # Primary role → essential
        if figure.figure_role == FigureRole.PRIMARY:
            figure.is_essential = True
        
        # P5 related → assessment related
        if figure.is_p5_related:
            figure.is_assessment_related = True
        
        # Has caption → likely important
        if figure.caption and figure.caption_confidence > 0.5:
            figure.is_essential = True
        
        # Large image → likely essential
        if figure.width_px > 600 and figure.height_px > 400:
            figure.is_essential = True
        
        # Small image → supplementary
        if figure.width_px < 200 or figure.height_px < 200:
            figure.is_supplementary = True