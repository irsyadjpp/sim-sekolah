"""
Audit Service gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext
import asyncpg

# Import generated protobuf modules (will be generated from proto file)
# from .proto import audit_service_pb2
# from .proto import audit_service_pb2_grpc

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50059"))
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ai_platform:ai_platform@postgres:5432/ai_platform")


class AuditServicer:
    """gRPC servicer for Audit Service"""
    
    def __init__(self):
        self.db_pool: Optional[asyncpg.Pool] = None
    
    async def initialize_db(self):
        """Initialize database connection"""
        self.db_pool = await asyncpg.create_pool(DATABASE_URL)
    
    async def LogEvent(self, request, context: ServicerContext):
        """Log an audit event"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO audit_logs 
                    (id, timestamp, user_id, session_id, request_id, event_type, event_data, 
                     latency_ms, token_count, model_version, compliance_status, ip_address, user_agent)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                    """,
                    request.id,
                    datetime.utcnow(),
                    request.user_id,
                    request.session_id,
                    request.request_id,
                    request.event_type,
                    request.event_data,
                    request.latency_ms if request.HasField("latency_ms") else None,
                    request.token_count if request.HasField("token_count") else None,
                    request.model_version,
                    request.compliance_status,
                    request.ip_address,
                    request.user_agent
                )
            
            # Return response
            # return audit_service_pb2.LogEventResponse(id=request.id, status="logged")
            return {"id": request.id, "status": "logged"}
            
        except Exception as e:
            logger.error(f"Error logging event: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error logging event: {str(e)}")
            return None
    
    async def QueryLogs(self, request, context: ServicerContext):
        """Query audit logs"""
        try:
            conditions = []
            params = []
            param_count = 1
            
            if request.user_id:
                conditions.append(f"user_id = ${param_count}")
                params.append(request.user_id)
                param_count += 1
            
            if request.session_id:
                conditions.append(f"session_id = ${param_count}")
                params.append(request.session_id)
                param_count += 1
            
            if request.event_type:
                conditions.append(f"event_type = ${param_count}")
                params.append(request.event_type)
                param_count += 1
            
            where_clause = " AND ".join(conditions) if conditions else "TRUE"
            
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    f"""
                    SELECT * FROM audit_logs
                    WHERE {where_clause}
                    ORDER BY timestamp DESC
                    LIMIT ${param_count} OFFSET ${param_count + 1}
                    """,
                    *params,
                    request.limit,
                    request.offset
                )
            
            # Convert to protobuf response
            # logs = [audit_service_pb2.AuditLog(**dict(row)) for row in rows]
            # return audit_service_pb2.QueryLogsResponse(logs=logs)
            return {"logs": [dict(row) for row in rows]}
            
        except Exception as e:
            logger.error(f"Error querying logs: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error querying logs: {str(e)}")
            return None
    
    async def CheckCompliance(self, request, context: ServicerContext):
        """Check compliance for an event"""
        try:
            violations = []
            
            # Example compliance rules
            if request.event_type == "prompt":
                prompt_text = request.event_data.get("prompt", "")
                if "password" in prompt_text.lower() or "secret" in prompt_text.lower():
                    violations.append("Potential PII detected in prompt")
            
            if request.event_type == "answer":
                answer_text = request.event_data.get("answer", "")
                if len(answer_text) < 10:
                    violations.append("Answer too short")
            
            is_compliant = len(violations) == 0
            compliance_status = "compliant" if is_compliant else "non_compliant"
            
            # return audit_service_pb2.ComplianceResult(
            #     request_id=request.request_id,
            #     is_compliant=is_compliant,
            #     violations=violations,
            #     compliance_status=compliance_status
            # )
            return {
                "request_id": request.request_id,
                "is_compliant": is_compliant,
                "violations": violations,
                "compliance_status": compliance_status
            }
            
        except Exception as e:
            logger.error(f"Error checking compliance: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error checking compliance: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = AuditServicer()
    await servicer.initialize_db()
    
    # Add servicer to server
    # audit_service_pb2_grpc.add_AuditServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Audit Service gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Audit Service gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
