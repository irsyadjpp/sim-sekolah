"""
gRPC Server for Parser Service
Handles synchronous document parsing requests via gRPC
"""
import sys
import os
sys.path.append('/app')

import grpc
from concurrent import futures
import logging
from typing import Dict, Any
import tempfile
from pathlib import Path

# Import protobuf classes
try:
    import proto.parser_service_pb2 as pb2
    import proto.parser_service_pb2_grpc as pb2_grpc
except ImportError:
    print("Error: gRPC stub files not found. Please compile proto files first.")
    sys.exit(1)

# Import parser components
from app.extractors.text_extractor import TextExtractor
from app.extractors.table_extractor import TableExtractor
from app.extractors.image_extractor import ImageExtractor
from app.extractors.ocr_extractor import OCRExtractor
from app.extractors.layout_detector import LayoutDetector
from app.extractors.enhanced_layout_detector import EnhancedLayoutDetector
from app.extractors.formula_extractor import FormulaExtractor
from app.extractors.figure_extractor import FigureExtractor
from app.pipelines.document_pipeline import DocumentPipeline
from app.pipelines.modern_document_pipeline import ModernDocumentPipeline
from app.pipelines.reading_order_resolver import ReadingOrderResolver
from app.pipelines.semantic_chunker import SemanticChunker
from app.pipelines.region_classifier import RegionClassifier
from app.pipelines.semantic_services_integration import SemanticServicesIntegration
from app.normalizers.content_normalizer import ContentNormalizer
from app.services.vision_integration_service import get_vision_integration_service

logger = logging.getLogger(__name__)

# Temporary storage for processing documents
TEMP_DIR = Path(tempfile.gettempdir()) / "parser-service"
TEMP_DIR.mkdir(exist_ok=True)


class ParserServicer(pb2_grpc.ParserServiceServicer):
    """gRPC Servicer for Parser Service"""
    
    def __init__(self):
        # Initialize modern pipeline components
        self.layout_detector = EnhancedLayoutDetector()
        self.reading_order_resolver = ReadingOrderResolver()
        self.semantic_chunker = SemanticChunker(
            max_chunk_size=500,
            chunk_overlap=50
        )
        self.region_classifier = RegionClassifier()
        self.semantic_services_integration = SemanticServicesIntegration()
        
        # Initialize extractors (region-aware)
        self.ocr_extractor = OCRExtractor()
        self.table_extractor = TableExtractor()
        self.formula_extractor = FormulaExtractor()
        self.figure_extractor = FigureExtractor(
            detect_captions=True,
            classify_subject=True,
            detect_p5=True
        )
        self.vision_integration_service = get_vision_integration_service()
        
        # Initialize modern pipeline
        self.modern_document_pipeline = ModernDocumentPipeline(
            layout_detector=self.layout_detector,
            reading_order_resolver=self.reading_order_resolver,
            semantic_chunker=self.semantic_chunker,
            semantic_services_integration=self.semantic_services_integration,
            region_classifier=self.region_classifier,
            ocr_extractor=self.ocr_extractor,
            table_extractor=self.table_extractor,
            formula_extractor=self.formula_extractor,
            figure_extractor=self.figure_extractor
        )
        
        # Keep old pipeline for backward compatibility
        self.text_extractor = TextExtractor()
        self.image_extractor = ImageExtractor(upload_to_minio=True)
        self.layout_detector_old = LayoutDetector()
        self.content_normalizer = ContentNormalizer()
        
        self.document_pipeline = DocumentPipeline(
            text_extractor=self.text_extractor,
            table_extractor=self.table_extractor,
            image_extractor=self.image_extractor,
            ocr_extractor=self.ocr_extractor,
            layout_detector=self.layout_detector_old,
            content_normalizer=self.content_normalizer
        )
        
        logger.info("ParserServicer initialized with Modern Pipeline and FigureExtractor")
    
    def _get_file_extension(self, document_type: str) -> str:
        """Get file extension from document type"""
        extensions = {
            'pdf': '.pdf',
            'docx': '.docx',
            'doc': '.doc',
            'png': '.png',
            'jpg': '.jpg',
            'jpeg': '.jpeg',
            'tiff': '.tiff'
        }
        return extensions.get(document_type.lower(), '.pdf')
    
    def _dict_to_map(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Convert dictionary to protobuf map"""
        return {str(k): str(v) for k, v in data.items()}
    
    def ParseDocument(self, request, context):
        """
        Parse document and extract structured content using modern pipeline
        """
        try:
            document_id = request.document_id
            document_data = request.document_data
            document_type = request.document_type
            metadata = dict(request.metadata)
            
            logger.info(f"ParseDocument called for: {document_id} with modern pipeline")
            
            # Create temporary file from document data
            file_extension = self._get_file_extension(document_type)
            temp_file_path = TEMP_DIR / f"{document_id}{file_extension}"
            
            # Write document data to file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(document_data)
            
            # Process document with modern pipeline
            result = self.modern_document_pipeline.process(
                file_path=str(temp_file_path),
                document_id=document_id,
                options=metadata
            )
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Convert result to protobuf format
            # Use semantic chunks from modern pipeline
            text_chunks = []
            for i, chunk in enumerate(result.semantic_chunks):
                text_chunk = pb2.TextChunk(
                    chunk_id=chunk.get("chunk_id", f"{document_id}_text_{i}"),
                    content=chunk.get("content", ""),
                    page_number=chunk.get("page_number", 0),
                    metadata=self._dict_to_map({
                        "heading": chunk.get("heading", ""),
                        "heading_level": chunk.get("heading_level", 0),
                        "section_path": chunk.get("section_path", []),
                        "importance_score": chunk.get("importance_score", 0.0)
                    })
                )
                text_chunks.append(text_chunk)
            
            # Extract tables from regions
            table_chunks = []
            for page in result.pages:
                for region in page.regions:
                    if region.region_type.value == "table" and region.metadata:
                        table_data = region.metadata.get("table_data", {})
                        if table_data:
                            table_chunk = pb2.TableChunk(
                                chunk_id=region.region_id,
                                headers=table_data.get("headers", []),
                                rows=[pb2.TableRow(cells=row) for row in table_data.get("rows", [])],
                                page_number=region.page_number,
                                metadata=self._dict_to_map(region.metadata)
                            )
                            table_chunks.append(table_chunk)
            
            # Extract figures from regions
            image_chunks = []
            for page in result.pages:
                for region in page.regions:
                    if region.region_type.value == "figure" and region.metadata:
                        image_data = region.metadata.get("image_data", b"")
                        if image_data:
                            image_chunk = pb2.ImageChunk(
                                chunk_id=region.region_id,
                                image_data=image_data,
                                image_type=region.metadata.get("image_type", "png"),
                                page_number=region.page_number,
                                metadata=self._dict_to_map(region.metadata)
                            )
                            image_chunks.append(image_chunk)
            
            parse_result = pb2.ParseResult(
                text_chunks=text_chunks,
                table_chunks=table_chunks,
                image_chunks=image_chunks,
                metadata=self._dict_to_map({
                    "total_pages": len(result.pages),
                    "total_regions": sum(len(p.regions) for p in result.pages),
                    "total_chunks": len(result.semantic_chunks),
                    "processing_time": result.processing_time
                })
            )
            
            response = pb2.ParseDocumentResponse(
                success=True,
                message="Document parsed successfully with modern pipeline",
                result=parse_result,
                metadata={"timestamp": str(Path(__file__).stat().st_mtime)}
            )
            
            logger.info(f"ParseDocument completed for: {document_id} with modern pipeline")
            return response
            
        except Exception as e:
            logger.error(f"Error in ParseDocument: {str(e)}")
            return pb2.ParseDocumentResponse(
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.ParseResult(),
                metadata={}
            )
    
    def ParseText(self, request, context):
        """Parse text content"""
        try:
            text_id = request.text_id
            text_content = request.text_content
            metadata = dict(request.metadata)
            
            logger.info(f"ParseText called for: {text_id}")
            
            # Extract text content
            result = self.text_extractor.extract_text(text_content)
            
            text_parse_result = pb2.TextParseResult(
                chunk_id=text_id,
                content=result,
                metadata=self._dict_to_map(metadata)
            )
            
            response = pb2.ParseTextResponse(
                success=True,
                message="Text parsed successfully",
                result=text_parse_result,
                metadata={"timestamp": str(Path(__file__).stat().st_mtime)}
            )
            
            logger.info(f"ParseText completed for: {text_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ParseText: {str(e)}")
            return pb2.ParseTextResponse(
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.TextParseResult(),
                metadata={}
            )
    
    def ExtractTables(self, request, context):
        """Extract tables from document"""
        try:
            document_id = request.document_id
            document_data = request.document_data
            options = dict(request.options)
            
            logger.info(f"ExtractTables called for: {document_id}")
            
            # Create temporary file
            temp_file_path = TEMP_DIR / f"{document_id}.pdf"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(document_data)
            
            # Extract tables
            tables_data = self.table_extractor.extract(str(temp_file_path))
            
            # Clean up
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Convert to protobuf format
            tables = []
            for i, table in enumerate(tables_data.get("tables", [])):
                table_chunk = pb2.TableChunk(
                    chunk_id=f"{document_id}_table_{i}",
                    headers=table.get("headers", []),
                    rows=[pb2.TableRow(cells=row) for row in table.get("rows", [])],
                    page_number=table.get("page_number", 0),
                    metadata=self._dict_to_map(table.get("metadata", {}))
                )
                tables.append(table_chunk)
            
            response = pb2.ExtractTablesResponse(
                success=True,
                message="Tables extracted successfully",
                tables=tables,
                metadata={"timestamp": str(Path(__file__).stat().st_mtime)}
            )
            
            logger.info(f"ExtractTables completed for: {document_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ExtractTables: {str(e)}")
            return pb2.ExtractTablesResponse(
                success=False,
                message=f"Error: {str(e)}",
                tables=[],
                metadata={}
            )
    
    def ExtractImages(self, request, context):
        """Extract images from document"""
        try:
            document_id = request.document_id
            document_data = request.document_data
            options = dict(request.options)
            
            logger.info(f"ExtractImages called for: {document_id}")
            
            # Create temporary file
            temp_file_path = TEMP_DIR / f"{document_id}.pdf"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(document_data)
            
            # Extract images
            images_data = self.image_extractor.extract(str(temp_file_path))
            
            # Clean up
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Convert to protobuf format
            images = []
            for i, img in enumerate(images_data.get("images", [])):
                image_chunk = pb2.ImageChunk(
                    chunk_id=f"{document_id}_image_{i}",
                    image_data=img.get("image_data", b""),
                    image_type=img.get("image_type", "png"),
                    page_number=img.get("page_number", 0),
                    metadata=self._dict_to_map(img.get("metadata", {}))
                )
                images.append(image_chunk)
            
            response = pb2.ExtractImagesResponse(
                success=True,
                message="Images extracted successfully",
                images=images,
                metadata={"timestamp": str(Path(__file__).stat().st_mtime)}
            )
            
            logger.info(f"ExtractImages completed for: {document_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ExtractImages: {str(e)}")
            return pb2.ExtractImagesResponse(
                success=False,
                message=f"Error: {str(e)}",
                images=[],
                metadata={}
            )
    
    def ExtractOCR(self, request, context):
        """OCR processing"""
        try:
            image_id = request.image_id
            image_data = request.image_data
            language = request.language
            options = dict(request.options)
            
            logger.info(f"ExtractOCR called for: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(image_data)
            
            # Process OCR
            ocr_result = self.ocr_extractor.extract(str(temp_file_path), language=language)
            
            # Clean up
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Convert to protobuf format
            words = []
            for word in ocr_result.get("words", []):
                word_box = pb2.BoundingBox(
                    x=word.get("x", 0),
                    y=word.get("y", 0),
                    width=word.get("width", 0),
                    height=word.get("height", 0),
                    text=word.get("text", "")
                )
                ocr_word = pb2.OcrWord(
                    text=word.get("text", ""),
                    confidence=word.get("confidence", 0.0),
                    bbox=word_box
                )
                words.append(ocr_word)
            
            lines = []
            for line in ocr_result.get("lines", []):
                line_box = pb2.BoundingBox(
                    x=line.get("x", 0),
                    y=line.get("y", 0),
                    width=line.get("width", 0),
                    height=line.get("height", 0)
                )
                ocr_line = pb2.OcrLine(
                    text=line.get("text", ""),
                    words=words,  # Simplified - would need proper mapping
                    bbox=line_box
                )
                lines.append(ocr_line)
            
            ocr_result_proto = pb2.OCRResult(
                text=ocr_result.get("text", ""),
                confidence=ocr_result.get("confidence", 0.0),
                words=words,
                lines=lines
            )
            
            response = pb2.ExtractOCRResponse(
                success=True,
                message="OCR processing completed",
                result=ocr_result_proto,
                metadata={"timestamp": str(Path(__file__).stat().st_mtime)}
            )
            
            logger.info(f"ExtractOCR completed for: {image_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ExtractOCR: {str(e)}")
            return pb2.ExtractOCRResponse(
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.OCRResult(),
                metadata={}
            )
    
    def DetectLayout(self, request, context):
        """Layout detection"""
        try:
            document_id = request.document_id
            document_data = request.document_data
            options = dict(request.options)
            
            logger.info(f"DetectLayout called for: {document_id}")
            
            # Create temporary file
            temp_file_path = TEMP_DIR / f"{document_id}.pdf"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(document_data)
            
            # Detect layout
            layout_result = self.layout_detector.detect(str(temp_file_path))
            
            # Clean up
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Convert to protobuf format
            nodes = []
            for i, node in enumerate(layout_result.get("nodes", [])):
                hierarchy_node = pb2.HierarchyNode(
                    node_id=f"{document_id}_node_{i}",
                    node_type=node.get("type", "unknown"),
                    content=node.get("content", ""),
                    level=node.get("level", 0),
                    children=node.get("children", [])
                )
                nodes.append(hierarchy_node)
            
            edges = []
            for i, edge in enumerate(layout_result.get("edges", [])):
                hierarchy_edge = pb2.HierarchyEdge(
                    parent_id=edge.get("parent_id", ""),
                    child_id=edge.get("child_id", ""),
                    relationship_type=edge.get("type", "")
                )
                edges.append(hierarchy_edge)
            
            layout_result_proto = pb2.LayoutResult(
                elements=[pb2.LayoutElement(
                    element_type=elem.get("type", ""),
                    bbox=[pb2.BoundingBox(
                        x=bbox.get("x", 0),
                        y=bbox.get("y", 0),
                        width=bbox.get("width", 0),
                        height=bbox.get("height", 0)
                    ) for bbox in elem.get("bboxes", [])],
                    properties=self._dict_to_map(elem.get("properties", {}))
                ) for elem in layout_result.get("elements", [])],
                document_type=layout_result.get("document_type", "unknown")
            )
            
            response = pb2.DetectLayoutResponse(
                success=True,
                message="Layout detection completed",
                result=layout_result_proto,
                metadata={"timestamp": str(Path(__file__).stat().st_mtime)}
            )
            
            logger.info(f"DetectLayout completed for: {document_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in DetectLayout: {str(e)}")
            return pb2.DetectLayoutResponse(
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.LayoutResult(),
                metadata={}
            )
    
    def ExtractFigures(self, request, context):
        """
        Extract figures with high-level pedagogical interpretation
        """
        try:
            document_id = request.document_id
            document_data = request.document_data
            context_data = dict(request.context)
            options = dict(request.options)
            
            logger.info(f"ExtractFigures called for: {document_id}")
            
            # Create temporary file
            temp_file_path = TEMP_DIR / f"{document_id}.pdf"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(document_data)
            
            # Step 1: Extract images menggunakan ImageExtractor
            image_result = self.image_extractor.extract(
                file_path=str(temp_file_path),
                doc_id=document_id
            )
            
            # Step 2: Convert to figures menggunakan FigureExtractor
            figure_result = self.figure_extractor.extract_figures(
                raw_images=image_result.images,
                doc_context=context_data
            )
            
            # Clean up
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Convert FigureMetadata to protobuf format
            figure_metadata_list = []
            for figure in figure_result.figures:
                # Convert ImageMetadata
                image_metadata_proto = pb2.ImageMetadata(
                    image_id=figure.image_metadata.image_id,
                    xref=figure.image_metadata.xref,
                    page_number=figure.image_metadata.page_number,
                    page_width=figure.image_metadata.page_width,
                    page_height=figure.image_metadata.page_height,
                    bbox=figure.image_metadata.bbox,
                    bbox_normalized=figure.image_metadata.bbox_normalized,
                    format=figure.image_metadata.format,
                    width_px=figure.image_metadata.width_px,
                    height_px=figure.image_metadata.height_px,
                    color_space=figure.image_metadata.color_space,
                    bits_per_component=figure.image_metadata.bits_per_component,
                    file_size_bytes=figure.image_metadata.file_size_bytes,
                    aspect_ratio=figure.image_metadata.aspect_ratio,
                    is_likely_noise=figure.image_metadata.is_likely_noise,
                    noise_reason=figure.image_metadata.noise_reason,
                    content_hash=figure.image_metadata.content_hash,
                    is_duplicate=figure.image_metadata.is_duplicate,
                    surrounding_text_above=figure.image_metadata.surrounding_text_above,
                    surrounding_text_below=figure.image_metadata.surrounding_text_below,
                    has_caption_candidate=figure.image_metadata.has_caption_candidate
                )
                
                # Map enum values
                figure_type_map = {
                    "ILLUSTRATION": pb2.FIGURE_TYPE_ILLUSTRATION,
                    "DIAGRAM": pb2.FIGURE_TYPE_DIAGRAM,
                    "CHART": pb2.FIGURE_TYPE_CHART,
                    "MAP": pb2.FIGURE_TYPE_MAP,
                    "TIMELINE": pb2.FIGURE_TYPE_TIMELINE,
                    "PHOTO": pb2.FIGURE_TYPE_PHOTO,
                    "PORTRAIT": pb2.FIGURE_TYPE_PORTRAIT,
                    "GEOMETRIC_SHAPE": pb2.FIGURE_TYPE_GEOMETRIC_SHAPE,
                    "SCIENTIFIC_MODEL": pb2.FIGURE_TYPE_SCIENTIFIC_MODEL,
                    "MATHEMATICAL": pb2.FIGURE_TYPE_MATHEMATICAL,
                    "INFOGRAPHIC": pb2.FIGURE_TYPE_INFOGRAPHIC,
                    "FLOWCHART": pb2.FIGURE_TYPE_FLOWCHART,
                    "P5_PROJECT": pb2.FIGURE_TYPE_P5_PROJECT,
                    "ASESMEN_VISUAL": pb2.FIGURE_TYPE_ASESMEN_VISUAL,
                    "LEARNING_RESOURCE": pb2.FIGURE_TYPE_LEARNING_RESOURCE,
                    "UNKNOWN": pb2.FIGURE_TYPE_UNKNOWN
                }
                
                figure_role_map = {
                    "PRIMARY": pb2.FIGURE_ROLE_PRIMARY,
                    "SECONDARY": pb2.FIGURE_ROLE_SECONDARY,
                    "BACKGROUND": pb2.FIGURE_ROLE_BACKGROUND,
                    "NAVIGATION": pb2.FIGURE_ROLE_NAVIGATION,
                    "ASSESSMENT": pb2.FIGURE_ROLE_ASSESSMENT
                }
                
                figure_subject_map = {
                    "IPA": pb2.FIGURE_SUBJECT_IPA,
                    "IPS": pb2.FIGURE_SUBJECT_IPS,
                    "MATEMATIKA": pb2.FIGURE_SUBJECT_MATEMATIKA,
                    "BAHASA_INDONESIA": pb2.FIGURE_SUBJECT_BAHASA_INDONESIA,
                    "BAHASA_INGGRIS": pb2.FIGURE_SUBJECT_BAHASA_INGGRIS,
                    "PJOK": pb2.FIGURE_SUBJECT_PJOK,
                    "SENI_BUDAYA": pb2.FIGURE_SUBJECT_SENI_BUDAYA,
                    "PPKN": pb2.FIGURE_SUBJECT_PPKN,
                    "AGAMA": pb2.FIGURE_SUBJECT_AGAMA,
                    "IPAS": pb2.FIGURE_SUBJECT_IPAS,
                    "SBDP": pb2.FIGURE_SUBJECT_SBDP,
                    "P5": pb2.FIGURE_SUBJECT_P5,
                    "UNKNOWN": pb2.FIGURE_SUBJECT_UNKNOWN
                }
                
                image_type_map = {
                    "RASTER_EMBEDDED": pb2.IMAGE_TYPE_RASTER_EMBEDDED,
                    "VECTOR_RENDERED": pb2.IMAGE_TYPE_VECTOR_RENDERED,
                    "SCANNED_PAGE": pb2.IMAGE_TYPE_SCANNED_PAGE,
                    "SCANNED_REGION": pb2.IMAGE_TYPE_SCANNED_REGION,
                    "DECORATIVE": pb2.IMAGE_TYPE_DECORATIVE,
                    "UNKNOWN": pb2.IMAGE_TYPE_UNKNOWN
                }
                
                figure_metadata_proto = pb2.FigureMetadata(
                    image_id=figure.image_id,
                    page_number=figure.page_number,
                    bbox=figure.bbox,
                    width_px=figure.width_px,
                    height_px=figure.height_px,
                    minio_key=figure.minio_key,
                    figure_type=figure_type_map.get(figure.figure_type, pb2.FIGURE_TYPE_UNKNOWN),
                    figure_role=figure_role_map.get(figure.figure_role, pb2.FIGURE_ROLE_PRIMARY),
                    figure_subject=figure_subject_map.get(figure.figure_subject, pb2.FIGURE_SUBJECT_UNKNOWN),
                    caption=figure.caption,
                    caption_confidence=figure.caption_confidence,
                    caption_position=figure.caption_position,
                    ai_description=figure.ai_description,
                    ai_confidence=figure.ai_confidence,
                    is_essential=figure.is_essential,
                    is_supplementary=figure.is_supplementary,
                    is_assessment_related=figure.is_assessment_related,
                    is_p5_related=figure.is_p5_related,
                    detected_elements=figure.detected_elements,
                    educational_keywords=figure.educational_keywords,
                    difficulty_level=figure.difficulty_level,
                    source=figure.source,
                    is_original=figure.is_original,
                    image_metadata=image_metadata_proto
                )
                figure_metadata_list.append(figure_metadata_proto)
            
            # Create extraction result
            figure_extraction_result_proto = pb2.FigureExtractionResult(
                doc_id=figure_result.doc_id,
                file_path=figure_result.file_path,
                total_images=figure_result.total_images,
                total_figures=figure_result.total_figures,
                figures=figure_metadata_list,
                by_type=self._dict_to_map(figure_result.by_type),
                by_role=self._dict_to_map(figure_result.by_role),
                by_subject=self._dict_to_map(figure_result.by_subject)
            )
            
            response = pb2.ExtractFiguresResponse(
                success=True,
                message="Figure extraction completed successfully",
                result=figure_extraction_result_proto,
                metadata={"timestamp": str(Path(__file__).stat().st_mtime)}
            )
            
            logger.info(f"ExtractFigures completed for: {document_id} - {figure_result.total_figures} figures extracted")
            return response
            
        except Exception as e:
            logger.error(f"Error in ExtractFigures: {str(e)}")
            return pb2.ExtractFiguresResponse(
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.FigureExtractionResult(),
                metadata={}
            )
    
    def AnalyzeFiguresWithVision(self, request, context):
        """
        Analyze figures menggunakan Vision Service untuk AI-powered image analysis
        """
        try:
            document_id = request.document_id
            minio_keys = list(request.minio_keys)
            context_data = dict(request.context)
            options = dict(request.options)
            
            logger.info(f"AnalyzeFiguresWithVision called for: {document_id} with {len(minio_keys)} figures")
            
            # Gunakan Vision Integration Service
            analysis_results = self.vision_integration_service.batch_analyze_figures(
                minio_keys=minio_keys,
                context=context_data,
                classification_only=options.get("classification_only", "false").lower() == "true",
                batch_size=options.get("batch_size", 10)
            )
            
            # Convert results to protobuf format
            figure_analysis_results_proto = []
            for result in analysis_results:
                detected_elements_proto = []
                for elem in result.get("detected_elements", []):
                    detected_element_proto = pb2.DetectedElement(
                        element_type=elem.get("element_type", ""),
                        label=elem.get("label", ""),
                        confidence=elem.get("confidence", 0.0),
                        bbox=pb2.BoundingBox(
                            x=elem.get("bbox", {}).get("x", 0),
                            y=elem.get("bbox", {}).get("y", 0),
                            width=elem.get("bbox", {}).get("width", 0),
                            height=elem.get("bbox", {}).get("height", 0)
                        )
                    )
                    detected_elements_proto.append(detected_element_proto)
                
                detected_text_proto = []
                for dt in result.get("detected_text", []):
                    detected_text_element_proto = pb2.DetectedText(
                        text=dt.get("text", ""),
                        confidence=dt.get("confidence", 0.0),
                        bbox=pb2.BoundingBox(
                            x=dt.get("bbox", {}).get("x", 0),
                            y=dt.get("bbox", {}).get("y", 0),
                            width=dt.get("bbox", {}).get("width", 0),
                            height=dt.get("bbox", {}).get("height", 0)
                        ),
                        language=dt.get("language", "")
                    )
                    detected_text_proto.append(detected_text_element_proto)
                
                figure_analysis_result_proto = pb2.FigureAnalysisResult(
                    image_id=result.get("image_id", ""),
                    minio_key=result.get("minio_key", ""),
                    analysis_success=result.get("analysis_success", True),
                    analysis_error=result.get("analysis_error", ""),
                    description=result.get("description", ""),
                    confidence=result.get("confidence", 0.0),
                    detected_elements=detected_elements_proto,
                    detected_text=detected_text_proto,
                    metadata=self._dict_to_map(result.get("metadata", {}))
                )
                figure_analysis_results_proto.append(figure_analysis_result_proto)
            
            response = pb2.AnalyzeFiguresWithVisionResponse(
                success=True,
                message=f"Vision analysis completed for {len(minio_keys)} figures",
                results=figure_analysis_results_proto,
                metadata={"timestamp": str(Path(__file__).stat().st_mtime)}
            )
            
            logger.info(f"AnalyzeFiguresWithVision completed for: {document_id} - {len(analysis_results)} results")
            return response
            
        except Exception as e:
            logger.error(f"Error in AnalyzeFiguresWithVision: {str(e)}")
            return pb2.AnalyzeFiguresWithVisionResponse(
                success=False,
                message=f"Error: {str(e)}",
                results=[],
                metadata={}
            )


def serve(port: int = 50051):
    """Start the gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Parser Service gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = ParserServicer()
    pb2_grpc.add_ParserServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Parser Service gRPC Server started successfully on port {port}")
    logger.info("Available methods: 8 (ParseDocument, ParseText, ExtractTables, ExtractImages, ExtractOCR, DetectLayout, ExtractFigures, AnalyzeFiguresWithVision)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


if __name__ == "__main__":
    import os
    port = int(os.getenv("GRPC_PORT", "50051"))
    serve(port)
