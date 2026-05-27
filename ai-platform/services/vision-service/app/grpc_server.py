"""
gRPC Server for Vision Service
Handles synchronous vision processing requests via gRPC
"""
import sys
import os
sys.path.append('/app')

import grpc
from concurrent import futures
import logging
import tempfile
from pathlib import Path
import base64

# Import proto files
import app.vision_service_pb2 as vision_service_pb2
import app.vision_service_pb2_grpc as vision_service_pb2_grpc

# Import vision components
from app.OCR.ocr_processor import OCRProcessor
from app.VLM.image_classifier import ImageClassifier
from app.captioning.image_captioning import ImageCaptioning
from app.diagram_analysis.diagram_analyzer import DiagramAnalyzer
from app.embeddings.image_embeddings import ImageEmbeddings

logger = logging.getLogger(__name__)

# Temporary storage for processing images
TEMP_DIR = Path(tempfile.gettempdir()) / "vision-service"
TEMP_DIR.mkdir(exist_ok=True)


class VisionServicer(vision_service_pb2_grpc.VisionServiceServicer):
    """gRPC Servicer for Vision Service"""
    
    def __init__(self):
        # Initialize vision components
        self.ocr_processor = OCRProcessor()
        self.image_classifier = ImageClassifier()
        self.image_captioning = ImageCaptioning()
        self.diagram_analyzer = DiagramAnalyzer()
        self.image_embeddings = ImageEmbeddings()
        logger.info("VisionServicer initialized")
    
    def ProcessOCR(self, request, context):
        """Process OCR on image"""
        try:
            image_id = request.image_id
            image_data = request.image_data
            language = request.language or "ind"
            options = dict(request.options)
            
            logger.info(f"ProcessOCR called for: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(image_data)
            
            # Process OCR
            ocr_result = self.ocr_processor.process(str(temp_file_path), language=language)
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Build protobuf response
            response = vision_service_pb2.ProcessOCRResponse(
                success=True,
                message="OCR processed successfully"
            )
            
            # Set OCR result
            ocr_result_proto = vision_service_pb2.OCRResult(
                text=ocr_result.get("text", ""),
                confidence=ocr_result.get("confidence", 0.0)
            )
            
            # Add words if available
            if "regions" in ocr_result:
                for region in ocr_result["regions"]:
                    word = vision_service_pb2.OcrWord(
                        text=region.get("text", ""),
                        confidence=region.get("confidence", 0.0)
                    )
                    
                    # Set bounding box if available
                    bbox = region.get("bounding_box", [])
                    if len(bbox) >= 4:
                        word.bbox.x = int(bbox[0])
                        word.bbox.y = int(bbox[1])
                        word.bbox.width = int(bbox[2])
                        word.bbox.height = int(bbox[3])
                    
                    ocr_result_proto.words.append(word)
            
            response.result.CopyFrom(ocr_result_proto)
            
            logger.info(f"ProcessOCR completed for: {image_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ProcessOCR: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def AnalyzeDiagram(self, request, context):
        """Analyze diagram structure"""
        try:
            diagram_id = request.diagram_id
            image_data = request.image_data
            diagram_type = request.diagram_type or "auto"
            options = dict(request.options)
            
            logger.info(f"AnalyzeDiagram called for: {diagram_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{diagram_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(image_data)
            
            # Analyze diagram
            diagram_result = self.diagram_analyzer.analyze(
                str(temp_file_path),
                diagram_type=diagram_type
            )
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Build protobuf response
            response = vision_service_pb2.AnalyzeDiagramResponse(
                success=True,
                message="Diagram analyzed successfully"
            )
            
            # Set diagram analysis result
            diagram_analysis = vision_service_pb2.DiagramAnalysis(
                diagram_type=diagram_result.get("diagram_type", diagram_type)
            )
            
            # Add elements if available
            if "elements" in diagram_result:
                for element in diagram_result["elements"]:
                    element_proto = vision_service_pb2.DiagramElement(
                        element_id=element.get("id", ""),
                        element_type=element.get("type", "")
                    )
                    
                    # Set bounding box if available
                    bbox = element.get("bounding_box", {})
                    if bbox:
                        element_proto.bbox.x = int(bbox.get("x", 0))
                        element_proto.bbox.y = int(bbox.get("y", 0))
                        element_proto.bbox.width = int(bbox.get("width", 0))
                        element_proto.bbox.height = int(bbox.get("height", 0))
                    
                    # Set properties
                    for key, value in element.get("properties", {}).items():
                        element_proto.properties[key] = str(value)
                    
                    diagram_analysis.elements.append(element_proto)
            
            # Add relationships if available
            if "relationships" in diagram_result:
                for rel in diagram_result["relationships"]:
                    relationship = vision_service_pb2.DiagramRelationship(
                        source_id=rel.get("source", ""),
                        target_id=rel.get("target", ""),
                        relationship_type=rel.get("type", "")
                    )
                    diagram_analysis.relationships.append(relationship)
            
            response.result.CopyFrom(diagram_analysis)
            
            logger.info(f"AnalyzeDiagram completed for: {diagram_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in AnalyzeDiagram: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ExtractFormula(self, request, context):
        """Extract mathematical formulas from image"""
        try:
            image_id = request.image_id
            image_data = request.image_data
            formula_type = request.formula_type or "auto"
            options = dict(request.options)
            
            logger.info(f"ExtractFormula called for: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(image_data)
            
            # Extract formulas (using diagram analyzer for now)
            formula_result = self.diagram_analyzer.analyze(
                str(temp_file_path),
                diagram_type="formula"
            )
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Build protobuf response
            response = vision_service_pb2.ExtractFormulaResponse(
                success=True,
                message="Formula extracted successfully"
            )
            
            # Set formula extraction result
            formula_extraction = vision_service_pb2.FormulaExtraction()
            
            # Add formulas if available
            if "elements" in formula_result:
                for idx, element in enumerate(formula_result["elements"]):
                    formula = vision_service_pb2.Formula(
                        formula_id=f"formula_{idx}",
                        latex=element.get("text", ""),
                        formula_type=element.get("type", formula_type),
                        confidence=element.get("confidence", 0.0)
                    )
                    
                    # Set bounding box if available
                    bbox = element.get("bounding_box", {})
                    if bbox:
                        formula.bbox.x = int(bbox.get("x", 0))
                        formula.bbox.y = int(bbox.get("y", 0))
                        formula.bbox.width = int(bbox.get("width", 0))
                        formula.bbox.height = int(bbox.get("height", 0))
                    
                    formula_extraction.formulas.append(formula)
            
            response.result.CopyFrom(formula_extraction)
            
            logger.info(f"ExtractFormula completed for: {image_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ExtractFormula: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def ClassifyImage(self, request, context):
        """Classify image content"""
        try:
            image_id = request.image_id
            image_data = request.image_data
            categories = list(request.categories) if request.categories else []
            options = dict(request.options)
            
            logger.info(f"ClassifyImage called for: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(image_data)
            
            # Classify image
            classification_result = self.image_classifier.classify(
                str(temp_file_path),
                classes=categories
            )
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Build protobuf response
            response = vision_service_pb2.ClassifyImageResponse(
                success=True,
                message="Image classified successfully"
            )
            
            # Set image classification result
            image_classification = vision_service_pb2.ImageClassification(
                primary_category=classification_result.get("predicted_class", ""),
                confidence=classification_result.get("confidence", 0.0)
            )
            
            # Add category scores if available
            if "classes" in classification_result:
                for cls in classification_result["classes"]:
                    score = vision_service_pb2.CategoryScore(
                        category=cls.get("class", ""),
                        score=cls.get("probability", 0.0)
                    )
                    image_classification.scores.append(score)
            
            response.result.CopyFrom(image_classification)
            
            logger.info(f"ClassifyImage completed for: {image_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in ClassifyImage: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def PreprocessImage(self, request, context):
        """Preprocess image with various operations"""
        try:
            image_id = request.image_id
            image_data = request.image_data
            operations = list(request.operations) if request.operations else []
            options = dict(request.options)
            
            logger.info(f"PreprocessImage called for: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(image_data)
            
            # Preprocess image (placeholder implementation)
            # In real implementation, this would apply the operations
            processed_data = image_data  # Placeholder
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Build protobuf response
            response = vision_service_pb2.PreprocessImageResponse(
                success=True,
                message="Image preprocessed successfully"
            )
            
            # Set image preprocessing result
            image_preprocessing = vision_service_pb2.ImagePreprocessing(
                processed_image=processed_data
            )
            
            # Add preprocessing steps
            for operation in operations:
                step = vision_service_pb2.PreprocessingStep(
                    operation=operation
                )
                for key, value in options.items():
                    step.parameters[key] = str(value)
                image_preprocessing.steps.append(step)
            
            response.result.CopyFrom(image_preprocessing)
            
            logger.info(f"PreprocessImage completed for: {image_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in PreprocessImage: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise


def serve(port: int = 50055):
    """Start gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer to server
    vision_service_pb2_grpc.add_VisionServiceServicer_to_server(
        VisionServicer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Vision Service gRPC server started on port {port}")
    
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server")
        server.stop(0)


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50055
    serve(port)