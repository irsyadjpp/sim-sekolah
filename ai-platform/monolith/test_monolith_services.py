"""
Test script for AI Platform Monolith services
Tests each service with sample PDF files and shows results
"""
import sys
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Add the app directory to path
sys.path.append('/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/monolith')

from app.services.document_ingestion.parser_service import ParserService
from app.services.content_processing.semantic_chunk_service import SemanticChunkService
from app.services.content_processing.semantic_enrichment_service import SemanticEnrichmentService
from app.services.content_processing.retrieval_service import RetrievalService
from app.services.content_processing.generation_service import GenerationService
from app.services.content_processing.ontology_validation_service import OntologyValidationService
from app.services.content_processing.vision_service import VisionService
from app.services.content_processing.metadata_service import MetadataService
from app.services.intelligence.pedagogy_service import PedagogyService
from app.services.intelligence.assessment_service import AssessmentService
from app.services.intelligence.curriculum_service import CurriculumService
from app.services.intelligence.strategic_analysis_service import StrategicAnalysisService
from app.services.intelligence.adaptive_learning_service import AdaptiveLearningService

# Sample file paths
BKB10_PDF = "/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge/sample/bkb10.pdf"
SIKLUS_AIR_PDF = "/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge/sample/siklus-air.pdf"

class MonolithTester:
    def __init__(self):
        self.results = {}
        
    def print_separator(self, title):
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
        
    def print_service_result(self, service_name, result):
        print(f"\n{'-'*80}")
        print(f"  SERVICE: {service_name}")
        print(f"{'-'*80}")
        if isinstance(result, dict):
            print(json.dumps(result, indent=2, default=str))
        elif hasattr(result, '__dict__'):
            print(json.dumps(result.__dict__, indent=2, default=str))
        else:
            print(str(result))
    
    async def test_parser_service(self, pdf_path):
        """Test Parser Service with PDF file"""
        self.print_separator("PARSER SERVICE TEST")
        print(f"Testing with file: {pdf_path}")
        
        try:
            parser_service = ParserService()
            await parser_service.initialize()
            
            # Read the PDF file
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
            
            # Parse the document
            result = await parser_service.parse_document(pdf_content, pdf_path)
            
            self.results['parser_service'] = result
            self.print_service_result("Parser Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Parser Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['parser_service'] = {'error': error_msg}
            return None
    
    async def test_semantic_chunk_service(self, parsed_content):
        """Test Semantic Chunk Service"""
        self.print_separator("SEMANTIC CHUNK SERVICE TEST")
        
        if not parsed_content:
            print("⚠️ Skipping - No parsed content available")
            return None
            
        try:
            chunk_service = SemanticChunkService()
            await chunk_service.initialize()
            
            # Create chunks from parsed content
            result = await chunk_service.create_chunks(parsed_content)
            
            self.results['semantic_chunk_service'] = result
            self.print_service_result("Semantic Chunk Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Semantic Chunk Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['semantic_chunk_service'] = {'error': error_msg}
            return None
    
    async def test_semantic_enrichment_service(self, chunks):
        """Test Semantic Enrichment Service"""
        self.print_separator("SEMANTIC ENRICHMENT SERVICE TEST")
        
        if not chunks:
            print("⚠️ Skipping - No chunks available")
            return None
            
        try:
            enrichment_service = SemanticEnrichmentService()
            await enrichment_service.initialize()
            
            # Enrich the chunks
            result = await enrichment_service.enrich_chunks(chunks)
            
            self.results['semantic_enrichment_service'] = result
            self.print_service_result("Semantic Enrichment Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Semantic Enrichment Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['semantic_enrichment_service'] = {'error': error_msg}
            return None
    
    async def test_retrieval_service(self):
        """Test Retrieval Service"""
        self.print_separator("RETRIEVAL SERVICE TEST")
        
        try:
            retrieval_service = RetrievalService()
            await retrieval_service.initialize()
            
            # Test basic retrieval
            result = await retrieval_service.retrieve_content("siklus air", top_k=5)
            
            self.results['retrieval_service'] = result
            self.print_service_result("Retrieval Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Retrieval Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['retrieval_service'] = {'error': error_msg}
            return None
    
    async def test_generation_service(self):
        """Test Generation Service"""
        self.print_separator("GENERATION SERVICE TEST")
        
        try:
            generation_service = GenerationService()
            await generation_service.initialize()
            
            # Test content generation
            result = await generation_service.generate_content(
                topic="Siklus air",
                content_type="explanation"
            )
            
            self.results['generation_service'] = result
            self.print_service_result("Generation Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Generation Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['generation_service'] = {'error': error_msg}
            return None
    
    async def test_ontology_validation_service(self):
        """Test Ontology Validation Service"""
        self.print_separator("ONTOLOGY VALIDATION SERVICE TEST")
        
        try:
            ontology_service = OntologyValidationService()
            await ontology_service.initialize()
            
            # Test ontology validation
            test_content = {
                "subject": "IPA",
                "grade_level": "6",
                "topic": "Siklus air"
            }
            result = await ontology_service.validate_content(test_content)
            
            self.results['ontology_validation_service'] = result
            self.print_service_result("Ontology Validation Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Ontology Validation Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['ontology_validation_service'] = {'error': error_msg}
            return None
    
    async def test_vision_service(self, pdf_path):
        """Test Vision Service with PDF file"""
        self.print_separator("VISION SERVICE TEST")
        print(f"Testing with file: {pdf_path}")
        
        try:
            vision_service = VisionService()
            await vision_service.initialize()
            
            # Test vision analysis
            result = await vision_service.analyze_document(pdf_path)
            
            self.results['vision_service'] = result
            self.print_service_result("Vision Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Vision Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['vision_service'] = {'error': error_msg}
            return None
    
    async def test_metadata_service(self):
        """Test Metadata Service"""
        self.print_separator("METADATA SERVICE TEST")
        
        try:
            metadata_service = MetadataService()
            await metadata_service.initialize()
            
            # Test metadata extraction
            result = await metadata_service.extract_metadata("test content", {
                "subject": "IPA",
                "grade": "6"
            })
            
            self.results['metadata_service'] = result
            self.print_service_result("Metadata Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Metadata Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['metadata_service'] = {'error': error_msg}
            return None
    
    async def test_pedagogy_service(self):
        """Test Pedagogy Service"""
        self.print_separator("PEDAGOGY SERVICE TEST")
        
        try:
            pedagogy_service = PedagogyService()
            await pedagogy_service.initialize()
            
            # Test pedagogy analysis
            test_content = "Guru menjelaskan siklus air dengan menggunakan diagram dan demonstrasi praktis."
            result = await pedagogy_service.analyze_pedagogy(test_content)
            
            self.results['pedagogy_service'] = result
            self.print_service_result("Pedagogy Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Pedagogy Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['pedagogy_service'] = {'error': error_msg}
            return None
    
    async def test_assessment_service(self):
        """Test Assessment Service"""
        self.print_separator("ASSESSMENT SERVICE TEST")
        
        try:
            assessment_service = AssessmentService()
            await assessment_service.initialize()
            
            # Test assessment generation
            result = await assessment_service.generate_assessment(
                topic="Siklus air",
                grade_level="6",
                question_count=3
            )
            
            self.results['assessment_service'] = result
            self.print_service_result("Assessment Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Assessment Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['assessment_service'] = {'error': error_msg}
            return None
    
    async def test_curriculum_service(self):
        """Test Curriculum Service"""
        self.print_separator("CURRICULUM SERVICE TEST")
        
        try:
            curriculum_service = CurriculumService()
            await curriculum_service.initialize()
            
            # Test curriculum alignment
            result = await curriculum_service.check_alignment(
                content="Siklus air adalah pergerakan air yang terus menerus dari bumi ke atmosfer dan kembali lagi.",
                curriculum="Kurikulum Merdeka",
                grade="6"
            )
            
            self.results['curriculum_service'] = result
            self.print_service_result("Curriculum Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Curriculum Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['curriculum_service'] = {'error': error_msg}
            return None
    
    async def test_strategic_analysis_service(self):
        """Test Strategic Analysis Service"""
        self.print_separator("STRATEGIC ANALYSIS SERVICE TEST")
        
        try:
            strategic_service = StrategicAnalysisService()
            await strategic_service.initialize()
            
            # Test SWOT analysis
            result = await strategic_service.perform_swot_analysis(
                topic="Pembelajaran IPA SD"
            )
            
            self.results['strategic_analysis_service'] = result
            self.print_service_result("Strategic Analysis Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Strategic Analysis Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['strategic_analysis_service'] = {'error': error_msg}
            return None
    
    async def test_adaptive_learning_service(self):
        """Test Adaptive Learning Service"""
        self.print_separator("ADAPTIVE LEARNING SERVICE TEST")
        
        try:
            adaptive_service = AdaptiveLearningService()
            await adaptive_service.initialize()
            
            # Test personalized learning path
            result = await adaptive_service.generate_learning_path(
                student_profile={"grade": "6", "subject": "IPA"},
                topic="Siklus air"
            )
            
            self.results['adaptive_learning_service'] = result
            self.print_service_result("Adaptive Learning Service", result)
            
            return result
        except Exception as e:
            error_msg = f"Error in Adaptive Learning Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['adaptive_learning_service'] = {'error': error_msg}
            return None
    
    async def run_full_pipeline(self, pdf_path):
        """Run the complete pipeline for a PDF file"""
        self.print_separator(f"FULL PIPELINE TEST - {Path(pdf_path).name}")
        
        # Step 1: Parser Service
        parsed_content = await self.test_parser_service(pdf_path)
        
        # Step 2: Semantic Chunk Service (depends on parser)
        chunks = await self.test_semantic_chunk_service(parsed_content)
        
        # Step 3: Semantic Enrichment Service (depends on chunks)
        enriched_chunks = await self.test_semantic_enrichment_service(chunks)
        
        # Step 4: Vision Service
        vision_results = await self.test_vision_service(pdf_path)
        
        return {
            'parsed_content': parsed_content,
            'chunks': chunks,
            'enriched_chunks': enriched_chunks,
            'vision_results': vision_results
        }
    
    async def run_standalone_tests(self):
        """Run standalone tests for services that don't depend on previous results"""
        await self.test_retrieval_service()
        await self.test_generation_service()
        await self.test_ontology_validation_service()
        await self.test_metadata_service()
        await self.test_pedagogy_service()
        await self.test_assessment_service()
        await self.test_curriculum_service()
        await self.test_strategic_analysis_service()
        await self.test_adaptive_learning_service()
    
    def save_results(self):
        """Save test results to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/monolith/test_results_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n✅ Test results saved to: {output_file}")
        return output_file

async def main():
    """Main test function"""
    print("🚀 Starting AI Platform Monolith Service Tests")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = MonolithTester()
    
    # Test with bkb10.pdf
    print(f"\n📄 Testing with BKB10 PDF...")
    bkb10_results = await tester.run_full_pipeline(BKB10_PDF)
    
    # Test with siklus-air.pdf
    print(f"\n📄 Testing with SIKLUS AIR PDF...")
    siklus_air_results = await tester.run_full_pipeline(SIKLUS_AIR_PDF)
    
    # Run standalone tests
    print(f"\n🔧 Running standalone service tests...")
    await tester.run_standalone_tests()
    
    # Save results
    output_file = tester.save_results()
    
    # Print summary
    tester.print_separator("TEST SUMMARY")
    print(f"Total services tested: {len(tester.results)}")
    print(f"Successful tests: {sum(1 for v in tester.results.values() if 'error' not in str(v))}")
    print(f"Failed tests: {sum(1 for v in tester.results.values() if 'error' in str(v))}")
    print(f"\n✅ Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Results saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())