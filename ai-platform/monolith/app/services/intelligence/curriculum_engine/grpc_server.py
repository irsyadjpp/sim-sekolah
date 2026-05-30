"""
Curriculum Engine gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50062"))


class CurriculumServicer:
    """gRPC servicer for Curriculum Engine"""
    
    def __init__(self):
        from .main import CurriculumEngine, CPStructure, ATPStructure
        self.curriculum_engine = CurriculumEngine()
        self.CPStructure = CPStructure
        self.ATPStructure = ATPStructure
    
    async def ValidateCP(self, request, context: ServicerContext):
        """Validate Curriculum Program"""
        try:
            cp_structure = self.CPStructure(
                id=request.id,
                name=request.name,
                phase=request.phase,
                grade=request.grade,
                subjects=list(request.subjects),
                competencies=[dict(comp) for comp in request.competencies],
                learning_objectives=list(request.learning_objectives)
            )
            
            result = self.curriculum_engine.validate_cp(cp_structure)
            
            # Return protobuf response
            # return curriculum_service_pb2.ValidationResult(
            #     is_valid=result["is_valid"],
            #     errors=result["errors"],
            #     warnings=result["warnings"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error validating CP: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error validating CP: {str(e)}")
            return None
    
    async def ValidateATP(self, request, context: ServicerContext):
        """Validate Annual Teaching Plan"""
        try:
            atp_structure = self.ATPStructure(
                id=request.id,
                cp_id=request.cp_id,
                phase=request.phase,
                grade=request.grade,
                semester=request.semester,
                topics=[dict(topic) for topic in request.topics],
                time_allocation=dict(request.time_allocation)
            )
            
            result = self.curriculum_engine.validate_atp(atp_structure)
            
            # Return protobuf response
            # return curriculum_service_pb2.ValidationResult(
            #     is_valid=result["is_valid"],
            #     errors=result["errors"],
            #     warnings=result["warnings"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error validating ATP: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error validating ATP: {str(e)}")
            return None
    
    async def CheckAlignment(self, request, context: ServicerContext):
        """Check CP/ATP alignment"""
        try:
            cp_structure = self.CPStructure(
                id=request.cp_structure.id,
                name=request.cp_structure.name,
                phase=request.cp_structure.phase,
                grade=request.cp_structure.grade,
                subjects=list(request.cp_structure.subjects),
                competencies=[dict(comp) for comp in request.cp_structure.competencies],
                learning_objectives=list(request.cp_structure.learning_objectives)
            )
            
            atp_structure = self.ATPStructure(
                id=request.atp_structure.id,
                cp_id=request.atp_structure.cp_id,
                phase=request.atp_structure.phase,
                grade=request.atp_structure.grade,
                semester=request.atp_structure.semester,
                topics=[dict(topic) for topic in request.atp_structure.topics],
                time_allocation=dict(request.atp_structure.time_allocation)
            )
            
            result = self.curriculum_engine.check_alignment(cp_structure, atp_structure)
            
            # Return protobuf response
            # return curriculum_service_pb2.AlignmentResult(
            #     is_aligned=result["is_aligned"],
            #     alignment_score=result["alignment_score"],
            #     missing_competencies=result["missing_competencies"],
            #     extra_topics=result["extra_topics"],
            #     recommendations=result["recommendations"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error checking alignment: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error checking alignment: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = CurriculumServicer()
    
    # Add servicer to server
    # curriculum_service_pb2_grpc.add_CurriculumServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Curriculum Engine gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Curriculum Engine gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
