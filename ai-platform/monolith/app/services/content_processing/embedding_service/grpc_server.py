"""
gRPC Server for Embedding Service
Handles synchronous embedding generation requests via gRPC
"""
import sys
import os
sys.path.append('/app')

import grpc
from concurrent import futures
import logging
import time

# Import proto files
import app.embedding_service_pb2 as embedding_service_pb2
import app.embedding_service_pb2_grpc as embedding_service_pb2_grpc

# Import embedding components
from app.embedders.text_embedder import TextEmbedder
from app.embedders.image_embedder import ImageEmbedder
from app.embedders.table_embedder import TableEmbedder
from app.embedders.formula_embedder import FormulaEmbedder

logger = logging.getLogger(__name__)


class EmbeddingServicer(embedding_service_pb2_grpc.EmbeddingServiceServicer):
    """gRPC Servicer for Embedding Service"""
    
    def __init__(self):
        # Initialize embedders
        self.text_embedder = TextEmbedder()
        self.image_embedder = ImageEmbedder()
        self.table_embedder = TableEmbedder()
        self.formula_embedder = FormulaEmbedder()
        logger.info("EmbeddingServicer initialized")
    
    def EmbedText(self, request, context):
        """Generate text embedding"""
        try:
            text_id = request.text_id
            text_content = request.text_content
            model = request.model or "default"
            options = dict(request.options)
            
            logger.info(f"EmbedText called for: {text_id}")
            
            start_time = time.time()
            
            # Generate embedding
            embedding_result = self.text_embedder.embed(
                text=text_content,
                model=model,
                options=options
            )
            
            embedding_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = embedding_service_pb2.EmbedTextResponse(
                success=True,
                message="Text embedding generated successfully"
            )
            
            # Build embedding result
            embedding_proto = embedding_service_pb2.EmbeddingResult(
                text_id=text_id,
                dimension=len(embedding_result.get("embedding", [])),
                model=model,
                embedding_time_ms=embedding_time
            )
            
            # Add embedding vector
            for value in embedding_result.get("embedding", []):
                embedding_proto.embedding.append(float(value))
            
            response.result.CopyFrom(embedding_proto)
            
            logger.info(f"EmbedText completed for: {text_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in EmbedText: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def EmbedImage(self, request, context):
        """Generate image embedding"""
        try:
            image_id = request.image_id
            image_data = request.image_data
            model = request.model or "default"
            options = dict(request.options)
            
            logger.info(f"EmbedImage called for: {image_id}")
            
            # Generate embedding
            embedding_result = self.image_embedder.embed(
                image_data=image_data,
                model=model,
                options=options
            )
            
            # Build protobuf response
            response = embedding_service_pb2.EmbedImageResponse(
                success=True,
                message="Image embedding generated successfully"
            )
            
            # Build image embedding result
            image_embedding_proto = embedding_service_pb2.ImageEmbeddingResult(
                image_id=image_id,
                dimension=len(embedding_result.get("embedding", [])),
                model=model
            )
            
            # Add embedding vector
            for value in embedding_result.get("embedding", []):
                image_embedding_proto.embedding.append(float(value))
            
            # Add detected objects
            for obj in embedding_result.get("detected_objects", []):
                image_embedding_proto.detected_objects.append(obj)
            
            response.result.CopyFrom(image_embedding_proto)
            
            logger.info(f"EmbedImage completed for: {image_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in EmbedImage: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def EmbedTable(self, request, context):
        """Generate table embedding"""
        try:
            table_id = request.table_id
            headers = list(request.headers)
            rows = list(request.rows)
            model = request.model or "default"
            options = dict(request.options)
            
            logger.info(f"EmbedTable called for: {table_id}")
            
            # Convert protobuf rows to list format
            row_data = []
            for row in rows:
                row_data.append(list(row.cells))
            
            # Generate embedding
            embedding_result = self.table_embedder.embed(
                headers=headers,
                rows=row_data,
                model=model,
                options=options
            )
            
            # Build protobuf response
            response = embedding_service_pb2.EmbedTableResponse(
                success=True,
                message="Table embedding generated successfully"
            )
            
            # Build table embedding result
            table_embedding_proto = embedding_service_pb2.TableEmbeddingResult(
                table_id=table_id,
                dimension=len(embedding_result.get("embedding", [])),
                model=model
            )
            
            # Add embedding vector
            for value in embedding_result.get("embedding", []):
                table_embedding_proto.embedding.append(float(value))
            
            # Add cell embeddings if available
            if "cell_embeddings" in embedding_result:
                for cell_emb in embedding_result["cell_embeddings"]:
                    cell_proto = embedding_service_pb2.CellEmbedding(
                        cell_id=cell_emb.get("cell_id", "")
                    )
                    for value in cell_emb.get("embedding", []):
                        cell_proto.embedding.append(float(value))
                    table_embedding_proto.cell_embeddings.append(cell_proto)
            
            response.result.CopyFrom(table_embedding_proto)
            
            logger.info(f"EmbedTable completed for: {table_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in EmbedTable: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def EmbedFormula(self, request, context):
        """Generate formula embedding"""
        try:
            formula_id = request.formula_id
            formula_latex = request.formula_latex
            model = request.model or "default"
            options = dict(request.options)
            
            logger.info(f"EmbedFormula called for: {formula_id}")
            
            # Generate embedding
            embedding_result = self.formula_embedder.embed(
                latex=formula_latex,
                model=model,
                options=options
            )
            
            # Build protobuf response
            response = embedding_service_pb2.EmbedFormulaResponse(
                success=True,
                message="Formula embedding generated successfully"
            )
            
            # Build formula embedding result
            formula_embedding_proto = embedding_service_pb2.FormulaEmbeddingResult(
                formula_id=formula_id,
                dimension=len(embedding_result.get("embedding", [])),
                model=model
            )
            
            # Add embedding vector
            for value in embedding_result.get("embedding", []):
                formula_embedding_proto.embedding.append(float(value))
            
            # Add components if available
            if "components" in embedding_result:
                for comp in embedding_result["components"]:
                    comp_proto = embedding_service_pb2.FormulaComponent(
                        component_id=comp.get("component_id", ""),
                        component_type=comp.get("component_type", "")
                    )
                    for value in comp.get("embedding", []):
                        comp_proto.embedding.append(float(value))
                    formula_embedding_proto.components.append(comp_proto)
            
            response.result.CopyFrom(formula_embedding_proto)
            
            logger.info(f"EmbedFormula completed for: {formula_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in EmbedFormula: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def BatchEmbedText(self, request, context):
        """Batch generate text embeddings"""
        try:
            items = list(request.items)
            model = request.model or "default"
            options = dict(request.options)
            
            logger.info(f"BatchEmbedText called for {len(items)} items")
            
            start_time = time.time()
            successful_items = 0
            failed_items = 0
            total_time = 0.0
            
            # Build protobuf response
            response = embedding_service_pb2.BatchEmbedTextResponse(
                success=True,
                message="Batch text embedding completed successfully"
            )
            
            # Build batch embedding result
            batch_result = embedding_service_pb2.BatchEmbeddingResult()
            
            # Process each item
            for item in items:
                try:
                    item_start_time = time.time()
                    
                    # Generate embedding
                    embedding_result = self.text_embedder.embed(
                        text=item.text_content,
                        model=model,
                        options=options
                    )
                    
                    item_time = (time.time() - item_start_time) * 1000
                    total_time += item_time
                    
                    # Build embedding result
                    embedding_proto = embedding_service_pb2.EmbeddingResult(
                        text_id=item.text_id,
                        dimension=len(embedding_result.get("embedding", [])),
                        model=model,
                        embedding_time_ms=item_time
                    )
                    
                    # Add embedding vector
                    for value in embedding_result.get("embedding", []):
                        embedding_proto.embedding.append(float(value))
                    
                    batch_result.embeddings.append(embedding_proto)
                    successful_items += 1
                    
                except Exception as e:
                    logger.error(f"Error embedding item {item.text_id}: {str(e)}")
                    failed_items += 1
            
            # Build summary
            average_time = total_time / successful_items if successful_items > 0 else 0.0
            total_batch_time = (time.time() - start_time)
            throughput = successful_items / total_batch_time if total_batch_time > 0 else 0.0
            
            summary = embedding_service_pb2.BatchSummary(
                total_items=len(items),
                successful_items=successful_items,
                failed_items=failed_items,
                average_time_ms=average_time,
                throughput_per_sec=throughput
            )
            
            batch_result.summary.CopyFrom(summary)
            response.result.CopyFrom(batch_result)
            
            logger.info(f"BatchEmbedText completed")
            return response
            
        except Exception as e:
            logger.error(f"Error in BatchEmbedText: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def GetEmbeddingInfo(self, request, context):
        """Get embedding model information"""
        try:
            model = request.model or "default"
            
            logger.info(f"GetEmbeddingInfo called for model: {model}")
            
            # Get model info
            model_info = self.text_embedder.get_model_info(model)
            
            # Build protobuf response
            response = embedding_service_pb2.GetEmbeddingInfoResponse(
                success=True,
                message="Model info retrieved successfully"
            )
            
            # Build model info
            model_info_proto = embedding_service_pb2.ModelInfo(
                model_name=model_info.get("model_name", model),
                dimension=model_info.get("dimension", 0),
                model_type=model_info.get("model_type", "text"),
                max_sequence_length=model_info.get("max_sequence_length", 512),
                version=model_info.get("version", "1.0")
            )
            
            # Add supported languages
            for lang in model_info.get("supported_languages", ["en"]):
                model_info_proto.supported_languages.append(lang)
            
            response.result.CopyFrom(model_info_proto)
            
            logger.info(f"GetEmbeddingInfo completed for model: {model}")
            return response
            
        except Exception as e:
            logger.error(f"Error in GetEmbeddingInfo: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise


def serve(port: int = 50052):
    """Start gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer to server
    embedding_service_pb2_grpc.add_EmbeddingServiceServicer_to_server(
        EmbeddingServicer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Embedding Service gRPC server started on port {port}")
    
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server")
        server.stop(0)


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50052
    serve(port)