"""
Test script for updated AI Platform Monolith services with complete business logic
Tests the services that have been migrated with actual business logic
"""
import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime

sys.path.append('/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/monolith')

# Import updated services with complete business logic
from app.services.document_ingestion.parser_service import ParserService
from app.services.content_processing.semantic_chunk_service import SemanticChunkService
from app.services.content_processing.semantic_enrichment_service import SemanticEnrichmentService
from app.services.content_processing.retrieval_service import RetrievalService
from app.services.content_processing.generation_service import GenerationService
from app.services.content_processing.vision_service import VisionService

# Sample file paths
BKB10_PDF = "/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge/sample/bkb10.pdf"
SIKLUS_AIR_PDF = "/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge/sample/siklus-air.pdf"

class UpdatedServiceTester:
    def __init__(self):
        self.results = {}
        self.test_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def print_separator(self, title):
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
        
    def print_result(self, service_name, result):
        print(f"\n{'-'*80}")
        print(f"  SERVICE: {service_name}")
        print(f"{'-'*80}")
        if isinstance(result, (dict, list)):
            print(json.dumps(result, indent=2, default=str))
        else:
            print(str(result))
    
    async def test_parser_service(self):
        """Test updated Parser Service"""
        self.print_separator("PARSER SERVICE TEST (UPDATED)")
        
        try:
            parser_service = ParserService()
            parser_service.initialize()
            
            # Test health check
            health = parser_service.health()
            self.print_result("Parser Service Health", health)
            
            # Test with siklus-air.pdf
            print(f"\nTesting with file: {SIKLUS_AIR_PDF}")
            result = await parser_service.parse_document_from_path(
                SIKLUS_AIR_PDF,
                metadata={"subject": "IPA", "grade": "6"}
            )
            
            self.results['parser_service'] = result
            self.print_result("Parser Service Result", result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error in Parser Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['parser_service'] = {'error': error_msg}
            return None
    
    async def test_semantic_chunk_service(self):
        """Test updated Semantic Chunk Service"""
        self.print_separator("SEMANTIC CHUNK SERVICE TEST (UPDATED)")
        
        try:
            chunk_service = SemanticChunkService()
            chunk_service.initialize()
            
            # Test health check
            health = chunk_service.health()
            self.print_result("Semantic Chunk Service Health", health)
            
            # Test with sample parsed document
            sample_document = {
                'document_id': 'test_doc_1',
                'text_content': 'Siklus air adalah pergerakan air yang terus menerus dari bumi ke atmosfer dan kembali lagi. Air menguap dari permukaan laut dan danau, membentuk awan, kemudian turun kembali sebagai hujan.',
                'document_type': 'textbook',
                'metadata': {
                    'subject': 'IPA',
                    'grade': '6',
                    'phase': 'B'
                }
            }
            
            result = await chunk_service.chunk_document(sample_document)
            
            self.results['semantic_chunk_service'] = result
            self.print_result("Semantic Chunk Service Result", result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error in Semantic Chunk Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['semantic_chunk_service'] = {'error': error_msg}
            return None
    
    async def test_semantic_enrichment_service(self):
        """Test updated Semantic Enrichment Service"""
        self.print_separator("SEMANTIC ENRICHMENT SERVICE TEST (UPDATED)")
        
        try:
            enrichment_service = SemanticEnrichmentService()
            enrichment_service.initialize()
            
            # Test health check
            health = enrichment_service.health()
            self.print_result("Semantic Enrichment Service Health", health)
            
            # Test with sample chunks
            sample_chunks = [
                {
                    'chunk_id': 'chunk_1',
                    'text': 'Siklus air adalah pergerakan air yang terus menerus dari bumi ke atmosfer dan kembali lagi.',
                    'metadata': {
                        'subject': 'IPA',
                        'grade': '6'
                    }
                }
            ]
            
            result = await enrichment_service.enrich_chunks(
                sample_chunks,
                metadata={'subject': 'IPA', 'grade': '6'}
            )
            
            self.results['semantic_enrichment_service'] = result
            self.print_result("Semantic Enrichment Service Result", result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error in Semantic Enrichment Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['semantic_enrichment_service'] = {'error': error_msg}
            return None
    
    async def test_retrieval_service(self):
        """Test updated Retrieval Service"""
        self.print_separator("RETRIEVAL SERVICE TEST (UPDATED)")
        
        try:
            retrieval_service = RetrievalService()
            retrieval_service.initialize()
            
            # Test health check
            health = retrieval_service.health()
            self.print_result("Retrieval Service Health", health)
            
            # Test semantic search
            result = await retrieval_service.retrieve_content(
                query="siklus air",
                top_k=5
            )
            
            self.results['retrieval_service'] = result
            self.print_result("Retrieval Service Result", result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error in Retrieval Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['retrieval_service'] = {'error': error_msg}
            return None
    
    async def test_generation_service(self):
        """Test updated Generation Service"""
        self.print_separator("GENERATION SERVICE TEST (UPDATED)")
        
        try:
            generation_service = GenerationService()
            generation_service.initialize()
            
            # Test health check
            health = generation_service.health()
            self.print_result("Generation Service Health", health)
            
            # Test content generation
            result = await generation_service.generate_content(
                topic="Siklus air",
                content_type="explanation"
            )
            
            self.results['generation_service'] = result
            self.print_result("Generation Service Result", result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error in Generation Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['generation_service'] = {'error': error_msg}
            return None
    
    async def test_vision_service(self):
        """Test updated Vision Service"""
        self.print_separator("VISION SERVICE TEST (UPDATED)")
        
        try:
            vision_service = VisionService()
            vision_service.initialize()
            
            # Test health check
            health = vision_service.health()
            self.print_result("Vision Service Health", health)
            
            # Test vision analysis with sample file
            result = await vision_service.analyze_document(SIKLUS_AIR_PDF)
            
            self.results['vision_service'] = result
            self.print_result("Vision Service Result", result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error in Vision Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['vision_service'] = {'error': error_msg}
            return None
    
    async def run_all_tests(self):
        """Run all service tests"""
        print("🚀 Starting Updated AI Platform Monolith Service Tests")
        print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test all updated services
        await self.test_parser_service()
        await self.test_semantic_chunk_service()
        await self.test_semantic_enrichment_service()
        await self.test_retrieval_service()
        await self.test_generation_service()
        await self.test_vision_service()
        
        # Save results
        output_file = self.save_results()
        
        # Print summary
        self.print_separator("UPDATED SERVICE TEST SUMMARY")
        print(f"Total services tested: {len(self.results)}")
        successful_tests = sum(1 for v in self.results.values() if 'error' not in str(v))
        failed_tests = sum(1 for v in self.results.values() if 'error' in str(v))
        print(f"Successful tests: {successful_tests}")
        print(f"Failed tests: {failed_tests}")
        
        print(f"\n✅ Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Results saved to: {output_file}")
        
        return self.results
    
    def save_results(self):
        """Save test results to a file"""
        output_file = f"/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/monolith/updated_service_test_results_{self.test_timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n✅ Updated service test results saved to: {output_file}")
        return output_file

async def main():
    """Main test function"""
    tester = UpdatedServiceTester()
    results = await tester.run_all_tests()
    return results

if __name__ == "__main__":
    import asyncio
    results = asyncio.run(main())