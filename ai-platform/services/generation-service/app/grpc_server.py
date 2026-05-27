"""
gRPC Server for Generation Service
Handles synchronous text generation requests via gRPC
"""
import sys
import os
sys.path.append('/app')

import grpc
from concurrent import futures
import logging
import time

# Import proto files
import app.generation_service_pb2 as generation_service_pb2
import app.generation_service_pb2_grpc as generation_service_pb2_grpc

# Import generation components
from app.generators.text_generator import TextGenerator
from app.generators.quiz_generator import QuizGenerator
from app.generators.lesson_plan_generator import LessonPlanGenerator
from app.generators.explanation_generator import ExplanationGenerator

logger = logging.getLogger(__name__)


class GenerationServicer(generation_service_pb2_grpc.GenerationServiceServicer):
    """gRPC Servicer for Generation Service"""
    
    def __init__(self):
        # Initialize generators
        self.text_generator = TextGenerator()
        self.quiz_generator = QuizGenerator()
        self.lesson_plan_generator = LessonPlanGenerator()
        self.explanation_generator = ExplanationGenerator()
        logger.info("GenerationServicer initialized")
    
    def GenerateText(self, request, context):
        """Generate text from prompt"""
        try:
            request_id = request.request_id
            prompt = request.prompt
            provider = request.provider or "openai"
            model = request.model or "gpt-3.5-turbo"
            temperature = request.temperature if request.temperature > 0 else 0.7
            max_tokens = request.max_tokens if request.max_tokens > 0 else 1000
            parameters = dict(request.parameters)
            
            logger.info(f"GenerateText called for: {request_id}")
            
            start_time = time.time()
            
            # Generate text
            generation_result = self.text_generator.generate(
                prompt=prompt,
                provider=provider,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                parameters=parameters
            )
            
            generation_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = generation_service_pb2.GenerateTextResponse(
                success=True,
                message="Text generation completed successfully"
            )
            
            # Build generation result
            generation_result_proto = generation_service_pb2.GenerationResult(
                generated_text=generation_result.get("text", ""),
                tokens_used=generation_result.get("tokens_used", 0),
                generation_time_ms=generation_time,
                model=model,
                provider=provider
            )
            
            response.result.CopyFrom(generation_result_proto)
            
            logger.info(f"GenerateText completed for: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in GenerateText: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def GenerateWithContext(self, request, context):
        """Generate text with context"""
        try:
            request_id = request.request_id
            prompt = request.prompt
            context_text = request.context
            provider = request.provider or "openai"
            model = request.model or "gpt-3.5-turbo"
            temperature = request.temperature if request.temperature > 0 else 0.7
            max_tokens = request.max_tokens if request.max_tokens > 0 else 1000
            parameters = dict(request.parameters)
            
            logger.info(f"GenerateWithContext called for: {request_id}")
            
            start_time = time.time()
            
            # Generate text with context
            generation_result = self.text_generator.generate_with_context(
                prompt=prompt,
                context=context_text,
                provider=provider,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                parameters=parameters
            )
            
            generation_time = (time.time() - start_time) * 1000
            
            # Build protobuf response
            response = generation_service_pb2.GenerateWithContextResponse(
                success=True,
                message="Text generation with context completed successfully"
            )
            
            # Build generation result
            generation_result_proto = generation_service_pb2.GenerationResult(
                generated_text=generation_result.get("text", ""),
                tokens_used=generation_result.get("tokens_used", 0),
                generation_time_ms=generation_time,
                model=model,
                provider=provider
            )
            
            response.result.CopyFrom(generation_result_proto)
            
            logger.info(f"GenerateWithContext completed for: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in GenerateWithContext: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def StreamText(self, request, context):
        """Stream text generation (placeholder implementation)"""
        try:
            request_id = request.request_id
            prompt = request.prompt
            provider = request.provider or "openai"
            model = request.model or "gpt-3.5-turbo"
            temperature = request.temperature if request.temperature > 0 else 0.7
            max_tokens = request.max_tokens if request.max_tokens > 0 else 1000
            parameters = dict(request.parameters)
            
            logger.info(f"StreamText called for: {request_id}")
            
            # Placeholder: generate complete text and send in chunks
            generation_result = self.text_generator.generate(
                prompt=prompt,
                provider=provider,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                parameters=parameters
            )
            
            text = generation_result.get("text", "")
            chunk_size = 100  # Send in 100-character chunks
            
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i + chunk_size]
                is_last = (i + chunk_size) >= len(text)
                
                response = generation_service_pb2.StreamTextResponse(
                    chunk_id=f"{request_id}_{i // chunk_size}",
                    text_chunk=chunk,
                    is_last=is_last
                )
                
                yield response
                
            logger.info(f"StreamText completed for: {request_id}")
            
        except Exception as e:
            logger.error(f"Error in StreamText: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def GenerateQuiz(self, request, context):
        """Generate quiz questions"""
        try:
            request_id = request.request_id
            topic = request.topic
            subject = request.subject or ""
            grade = request.grade or ""
            num_questions = request.num_questions if request.num_questions > 0 else 5
            difficulty = request.difficulty or "medium"
            question_type = request.question_type or "multiple_choice"
            options = dict(request.options)
            
            logger.info(f"GenerateQuiz called for: {request_id}")
            
            # Generate quiz
            quiz_result = self.quiz_generator.generate(
                topic=topic,
                subject=subject,
                grade=grade,
                num_questions=num_questions,
                difficulty=difficulty,
                question_type=question_type,
                options=options
            )
            
            # Build protobuf response
            response = generation_service_pb2.GenerateQuizResponse(
                success=True,
                message="Quiz generation completed successfully"
            )
            
            # Build quiz generation result
            quiz_result_proto = generation_service_pb2.QuizGenerationResult(
                quiz_topic=topic,
                difficulty_level=difficulty
            )
            
            # Add questions
            for q in quiz_result.get("questions", []):
                question_proto = generation_service_pb2.QuizQuestion(
                    question_id=q.get("question_id", ""),
                    question_text=q.get("question_text", ""),
                    correct_answer=q.get("correct_answer", ""),
                    explanation=q.get("explanation", "")
                )
                
                # Add options
                for opt in q.get("options", []):
                    question_proto.options.append(opt)
                
                quiz_result_proto.questions.append(question_proto)
            
            response.result.CopyFrom(quiz_result_proto)
            
            logger.info(f"GenerateQuiz completed for: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in GenerateQuiz: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def GenerateLessonPlan(self, request, context):
        """Generate lesson plan"""
        try:
            request_id = request.request_id
            topic = request.topic
            subject = request.subject or ""
            grade = request.grade or ""
            duration_minutes = request.duration_minutes if request.duration_minutes > 0 else 60
            learning_objectives = list(request.learning_objectives)
            pedagogy_type = request.pedagogy_type or "direct_instruction"
            options = dict(request.options)
            
            logger.info(f"GenerateLessonPlan called for: {request_id}")
            
            # Generate lesson plan
            lesson_plan_result = self.lesson_plan_generator.generate(
                topic=topic,
                subject=subject,
                grade=grade,
                duration_minutes=duration_minutes,
                learning_objectives=learning_objectives,
                pedagogy_type=pedagogy_type,
                options=options
            )
            
            # Build protobuf response
            response = generation_service_pb2.GenerateLessonPlanResponse(
                success=True,
                message="Lesson plan generation completed successfully"
            )
            
            # Build lesson plan result
            lesson_plan_result_proto = generation_service_pb2.LessonPlanResult()
            
            # Build lesson plan
            lesson_plan_data = lesson_plan_result.get("lesson_plan", {})
            lesson_plan_proto = generation_service_pb2.LessonPlan(
                plan_id=lesson_plan_data.get("plan_id", request_id),
                topic=topic,
                assessment_strategy=lesson_plan_data.get("assessment_strategy", "")
            )
            
            # Add activities
            for activity in lesson_plan_data.get("activities", []):
                activity_proto = generation_service_pb2.LessonActivity(
                    activity_id=activity.get("activity_id", ""),
                    title=activity.get("title", ""),
                    description=activity.get("description", ""),
                    duration_minutes=activity.get("duration_minutes", 0),
                    activity_type=activity.get("activity_type", "")
                )
                lesson_plan_proto.activities.append(activity_proto)
            
            # Add resources
            for resource in lesson_plan_data.get("resources", []):
                resource_proto = generation_service_pb2.LessonResource(
                    resource_id=resource.get("resource_id", ""),
                    resource_type=resource.get("resource_type", ""),
                    title=resource.get("title", ""),
                    url_or_path=resource.get("url_or_path", "")
                )
                lesson_plan_proto.resources.append(resource_proto)
            
            lesson_plan_result_proto.lesson_plan.CopyFrom(lesson_plan_proto)
            response.result.CopyFrom(lesson_plan_result_proto)
            
            logger.info(f"GenerateLessonPlan completed for: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in GenerateLessonPlan: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise
    
    def GenerateExplanation(self, request, context):
        """Generate explanation for a concept"""
        try:
            request_id = request.request_id
            concept = request.concept
            subject = request.subject or ""
            grade = request.grade or ""
            explanation_type = request.explanation_type or "detailed"
            target_audience = request.target_audience or "student"
            options = dict(request.options)
            
            logger.info(f"GenerateExplanation called for: {request_id}")
            
            # Generate explanation
            explanation_result = self.explanation_generator.generate(
                concept=concept,
                subject=subject,
                grade=grade,
                explanation_type=explanation_type,
                target_audience=target_audience,
                options=options
            )
            
            # Build protobuf response
            response = generation_service_pb2.GenerateExplanationResponse(
                success=True,
                message="Explanation generation completed successfully"
            )
            
            # Build explanation result
            explanation_result_proto = generation_service_pb2.ExplanationResult(
                explanation_text=explanation_result.get("explanation_text", "")
            )
            
            # Add sections
            for section in explanation_result.get("sections", []):
                section_proto = generation_service_pb2.ExplanationSection(
                    section_title=section.get("title", ""),
                    section_content=section.get("content", "")
                )
                explanation_result_proto.sections.append(section_proto)
            
            # Add examples
            for example in explanation_result.get("examples", []):
                example_proto = generation_service_pb2.Example(
                    example_id=example.get("example_id", ""),
                    description=example.get("description", ""),
                    solution=example.get("solution", "")
                )
                explanation_result_proto.examples.append(example_proto)
            
            response.result.CopyFrom(explanation_result_proto)
            
            logger.info(f"GenerateExplanation completed for: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in GenerateExplanation: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise


def serve(port: int = 50053):
    """Start gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer to server
    generation_service_pb2_grpc.add_GenerationServiceServicer_to_server(
        GenerationServicer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Generation Service gRPC server started on port {port}")
    
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server")
        server.stop(0)


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50053
    serve(port)