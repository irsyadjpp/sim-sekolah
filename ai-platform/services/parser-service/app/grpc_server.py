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
    import parser_service_pb2 as pb2
    import parser_service_pb2_grpc as pb2_grpc
except ImportError:
    print("Error: gRPC stub files not found. Please compile proto files first.")
    sys.exit(1)

# Import parser components
from app.extractors.text_extractor import TextExtractor
from app.extractors.table_extractor import TableExtractor
from app.extractors.image_extractor import ImageExtractor
from app.extractors.ocr_extractor import OCRExtractor
from app.extractors.layout_detector import LayoutDetector
from app.pipelines.document_pipeline import DocumentPipeline
from app.normalizers.content_normalizer import ContentNormalizer

logger = logging.getLogger(__name__)

# Temporary storage for processing documents
TEMP_DIR = Path(tempfile.gettempdir()) / "parser-service"
TEMP_DIR.mkdir(exist_ok=True)


class ParserServicer(pb2_grpc.ParserServiceServicer):
    """gRPC Servicer for Parser Service"""
    
    def __init__(self):
        # Initialize parser components
        self.text_extractor = TextExtractor()
        self.table_extractor = TableExtractor()
        self.image_extractor = ImageExtractor()
        self.ocr_extractor = OCRExtractor()
        self.layout_detector = LayoutDetector()
        self.content_normalizer = ContentNormalizer()
        self.document_pipeline = DocumentPipeline(
            text_extractor=self.text_extractor,
            table_extractor=self.table_extractor,
            image_extractor=self.image_extractor,
            ocr_extractor=self.ocr_extractor,
            layout_detector=self.layout_detector,
            content_normalizer=self.content_normalizer
        )
        logger.info("ParserServicer initialized")
    
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
        Parse document and extract structured content
        """
        try:
            document_id = request.document_id
            document_data = request.document_data
            document_type = request.document_type
            metadata = dict(request.metadata)
            
            logger.info(f"ParseDocument called for: {document_id}")
            
            # Create temporary file from document data
            file_extension = self._get_file_extension(document_type)
            temp_file_path = TEMP_DIR / f"{document_id}{file_extension}"
            
            # Write document data to file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(document_data)
            
            # Process document
            result = self.document_pipeline.process(
                file_path=str(temp_file_path),
                options=metadata
            )
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Convert result to protobuf format
            text_chunks = []
            for i, chunk in enumerate(result.get("text_chunks", [])):
                text_chunk = pb2.TextChunk(
                    chunk_id=f"{document_id}_text_{i}",
                    content=chunk.get("content", ""),
                    page_number=chunk.get("page_number", 0),
                    metadata=self._dict_to_map(chunk.get("metadata", {}))
                )
                text_chunks.append(text_chunk)
            
            table_chunks = []
            for i, chunk in enumerate(result.get("table_chunks", [])):
                table_chunk = pb2.TableChunk(
                    chunk_id=f"{document_id}_table_{i}",
                    headers=chunk.get("headers", []),
                    rows=[pb2.TableRow(cells=row) for row in chunk.get("rows", [])],
                    page_number=chunk.get("page_number", 0),
                    metadata=self._dict_to_map(chunk.get("metadata", {}))
                )
                table_chunks.append(table_chunk)
            
            image_chunks = []
            for i, chunk in enumerate(result.get("image_chunks", [])):
                image_chunk = pb2.ImageChunk(
                    chunk_id=f"{document_id}_image_{i}",
                    image_data=chunk.get("image_data", b""),
                    image_type=chunk.get("image_type", "png"),
                    page_number=chunk.get("page_number", 0),
                    metadata=self._dict_to_map(chunk.get("metadata", {}))
                )
                image_chunks.append(image_chunk)
            
            parse_result = pb2.ParseResult(
                text_chunks=text_chunks,
                table_chunks=table_chunks,
                image_chunks=image_chunks,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
            
            response = pb2.ParseDocumentResponse(
                success=True,
                message="Document parsed successfully",
                result=parse_result,
                metadata={"timestamp": str(Path(__file__).stat().st_mtime)}
            )
            
            logger.info(f"ParseDocument completed for: {document_id}")
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
    logger.info("Available methods: 6 (ParseDocument, ParseText, ExtractTables, ExtractImages, ExtractOCR, DetectLayout)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


if __name__ == "__main__":
    import os
    port = int(os.getenv("GRPC_PORT", "50051"))
    serve(port)
