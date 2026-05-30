"""
Test script specifically for bkb10.pdf and siklus-air.pdf
Tests both files through the working services with detailed output
"""
import sys
import os
import json
import logging
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime

sys.path.append('/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/monolith')

# Import updated services with complete business logic
from app.services.document_ingestion.parser_service import ParserService
from app.services.content_processing.semantic_chunk_service import SemanticChunkService
from app.services.content_processing.semantic_enrichment_service import SemanticEnrichmentService

# Sample file paths
BKB10_PDF = "/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge/sample/bkb10.pdf"
SIKLUS_AIR_PDF = "/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge/sample/siklus-air.pdf"

class PDFSpecificTester:
    def __init__(self):
        self.results = {}
        self.test_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def print_separator(self, title):
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
        
    def print_pdf_info(self, pdf_path):
        """Print basic PDF information"""
        self.print_separator(f"PDF INFO: {Path(pdf_path).name}")
        try:
            doc = fitz.open(pdf_path)
            info = {
                "file_name": Path(pdf_path).name,
                "page_count": doc.page_count,
                "file_size": os.path.getsize(pdf_path),
                "metadata": doc.metadata
            }
            doc.close()
            print(json.dumps(info, indent=2, default=str))
            return info
        except Exception as e:
            print(f"❌ Error getting PDF info: {str(e)}")
            return None
    
    async def test_parser_service_with_pdf(self, pdf_path):
        """Test Parser Service with specific PDF file"""
        self.print_separator(f"PARSER SERVICE TEST: {Path(pdf_path).name}")
        
        try:
            parser_service = ParserService()
            parser_service.initialize()
            
            print("📋 Parser Service Health Check:")
            health = parser_service.health()
            print(json.dumps(health, indent=2, default=str))
            
            print(f"\n🔄 Testing with file: {pdf_path}")
            result = await parser_service.parse_document_from_path(
                pdf_path,
                metadata={"subject": "IPA", "grade": "6"}
            )
            
            print(f"\n📊 Parser Service Result:")
            if result.get("success"):
                print(f"✅ Success: {result['success']}")
                print(f"📄 Page Count: {result.get('page_count', 'N/A')}")
                print(f"📝 Text Content Length: {len(str(result.get('text_content', '')))}")
                print(f"⏱️ Processing Time: {result.get('processing_time', 0):.2f}s")
                print(f"🔧 Extraction Method: {result.get('extraction_method', 'unknown')}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            self.results[f'parser_service_{Path(pdf_path).name}'] = result
            return result
            
        except Exception as e:
            error_msg = f"Error in Parser Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results[f'parser_service_{Path(pdf_path).name}'] = {'error': error_msg}
            return None
    
    async def test_semantic_chunk_service_with_pdf(self, pdf_path):
        """Test Semantic Chunk Service with specific PDF file"""
        self.print_separator(f"SEMANTIC CHUNK SERVICE TEST: {Path(pdf_path).name}")
        
        try:
            chunk_service = SemanticChunkService()
            chunk_service.initialize()
            
            print("📋 Semantic Chunk Service Health Check:")
            health = chunk_service.health()
            print(json.dumps(health, indent=2, default=str))
            
            # Extract text from PDF for chunking
            doc = fitz.open(pdf_path)
            text_content = ""
            for page in doc[:min(3, doc.page_count)]:  # First 3 pages
                text_content += page.get_text()
            doc.close()
            
            # Truncate for testing
            text_content = text_content[:2000]
            
            print(f"\n📝 Sample Text Content ({len(text_content)} chars):")
            print(f"{text_content[:300]}...")
            
            # Test chunking
            sample_document = {
                'document_id': f'test_{Path(pdf_path).stem}',
                'text_content': text_content,
                'document_type': 'textbook',
                'metadata': {
                    'subject': 'IPA',
                    'grade': '6',
                    'phase': 'B'
                }
            }
            
            print(f"\n🔄 Chunking document...")
            result = await chunk_service.chunk_document(sample_document)
            
            print(f"\n📊 Chunking Result:")
            if result.get("success"):
                print(f"✅ Success: {result['success']}")
                print(f"📦 Chunk Count: {result['chunk_count']}")
                print(f"🏷️ Chunk Types: {result.get('chunk_types', {})}")
                print(f"⏱️ Processing Time: {result['processing_time_ms']}ms")
                print(f"🔧 Strategy: {result.get('chunking_strategy', 'unknown')}")
                
                print(f"\n📋 Chunk Details (first 2):")
                for i, chunk in enumerate(result['chunks'][:2]):
                    print(f"\n  Chunk {i+1}:")
                    print(f"    ID: {chunk.get('chunk_id', 'N/A')}")
                    print(f"    Type: {chunk.get('metadata', {}).get('chunk_type', 'N/A')}")
                    print(f"    Text Preview: {chunk.get('text', '')[:100]}...")
                    print(f"    Quality Score: {chunk.get('metadata', {}).get('chunk_quality_score', 'N/A')}")
                    print(f"    Educational Value: {chunk.get('metadata', {}).get('educational_value_score', 'N/A')}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            self.results[f'semantic_chunk_service_{Path(pdf_path).name}'] = result
            return result
            
        except Exception as e:
            error_msg = f"Error in Semantic Chunk Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results[f'semantic_chunk_service_{Path(pdf_path).name}'] = {'error': error_msg}
            return None
    
    async def test_semantic_enrichment_service_with_pdf(self, pdf_path):
        """Test Semantic Enrichment Service with specific PDF file"""
        self.print_separator(f"SEMANTIC ENRICHMENT SERVICE TEST: {Path(pdf_path).name}")
        
        try:
            enrichment_service = SemanticEnrichmentService()
            enrichment_service.initialize()
            
            print("📋 Semantic Enrichment Service Health Check:")
            health = enrichment_service.health()
            print(json.dumps(health, indent=2, default=str))
            
            # Create sample chunks from PDF
            doc = fitz.open(pdf_path)
            text_content = doc[0].get_text()[:500]  # First page, 500 chars
            doc.close()
            
            sample_chunks = [
                {
                    'chunk_id': f'chunk_{Path(pdf_path).stem}_1',
                    'text': text_content,
                    'metadata': {
                        'subject': 'IPA',
                        'grade': '6'
                    }
                }
            ]
            
            print(f"\n📝 Sample Chunk Content:")
            print(f"{text_content}")
            
            print(f"\n🔄 Enriching chunks...")
            result = await enrichment_service.enrich_chunks(
                sample_chunks,
                metadata={'subject': 'IPA', 'grade': '6'}
            )
            
            print(f"\n📊 Enrichment Result:")
            if result.get("success"):
                print(f"✅ Success: {result['success']}")
                print(f"📦 Enriched Chunks: {result['chunk_count']}")
                print(f"🏷️ Enrichment Types: {result.get('enrichment_types', [])}")
                print(f"⏱️ Processing Time: {result['processing_time_ms']}ms")
                
                if result['enriched_chunks']:
                    chunk = result['enriched_chunks'][0]
                    print(f"\n📋 Enrichment Details:")
                    enrichment = chunk.get('enrichment', {})
                    
                    print(f"  🎓 Pedagogy Classification:")
                    pedagogy = enrichment.get('pedagogy_classification', {})
                    print(f"    Type: {pedagogy.get('pedagogy_type', 'N/A')}")
                    print(f"    Confidence: {pedagogy.get('confidence', 'N/A')}")
                    
                    print(f"  📚 Taxonomy Tags:")
                    taxonomy = enrichment.get('taxonomy_tags', {})
                    if 'error' in taxonomy:
                        print(f"    ⚠️ Error: {taxonomy['error']}")
                    else:
                        print(f"    {taxonomy}")
                    
                    print(f"  🌐 Metadata:")
                    meta = enrichment.get('enrichment_metadata', {})
                    print(f"    Language: {meta.get('language', 'N/A')}")
                    print(f"    Word Count: {meta.get('word_count', 'N/A')}")
                    print(f"    Enriched At: {meta.get('enriched_at', 'N/A')}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            self.results[f'semantic_enrichment_service_{Path(pdf_path).name}'] = result
            return result
            
        except Exception as e:
            error_msg = f"Error in Semantic Enrichment Service: {str(e)}"
            print(f"❌ {error_msg}")
            self.results[f'semantic_enrichment_service_{Path(pdf_path).name}'] = {'error': error_msg}
            return None
    
    async def test_both_pdfs(self):
        """Test both PDF files through all services"""
        print("🚀 Starting Specific PDF Testing for bkb10.pdf and siklus-air.pdf")
        print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test bkb10.pdf
        print("\n" + "="*80)
        print("  TESTING BKB10.PDF")
        print("="*80)
        
        self.print_pdf_info(BKB10_PDF)
        await self.test_parser_service_with_pdf(BKB10_PDF)
        await self.test_semantic_chunk_service_with_pdf(BKB10_PDF)
        await self.test_semantic_enrichment_service_with_pdf(BKB10_PDF)
        
        # Test siklus-air.pdf
        print("\n" + "="*80)
        print("  TESTING SIKLUS-AIR.PDF")
        print("="*80)
        
        self.print_pdf_info(SIKLUS_AIR_PDF)
        await self.test_parser_service_with_pdf(SIKLUS_AIR_PDF)
        await self.test_semantic_chunk_service_with_pdf(SIKLUS_AIR_PDF)
        await self.test_semantic_enrichment_service_with_pdf(SIKLUS_AIR_PDF)
        
        # Save results
        output_file = self.save_results()
        
        # Print summary
        self.print_separator("PDF TESTING SUMMARY")
        print(f"Total tests performed: {len(self.results)}")
        
        # Count successes and failures
        successful_tests = sum(1 for v in self.results.values() if 'error' not in str(v))
        failed_tests = sum(1 for v in self.results.values() if 'error' in str(v))
        
        print(f"Successful tests: {successful_tests}")
        print(f"Failed tests: {failed_tests}")
        
        # Per-file breakdown
        bkb10_tests = [k for k in self.results.keys() if 'bkb10.pdf' in k]
        siklus_air_tests = [k for k in self.results.keys() if 'siklus-air.pdf' in k]
        
        print(f"\n📄 bkb10.pdf: {len(bkb10_tests)} tests")
        print(f"📄 siklus-air.pdf: {len(siklus_air_tests)} tests")
        
        print(f"\n✅ Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Results saved to: {output_file}")
        
        return self.results
    
    def save_results(self):
        """Save test results to a file"""
        output_file = f"/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/monolith/pdf_specific_test_results_{self.test_timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n✅ PDF-specific test results saved to: {output_file}")
        return output_file

async def main():
    """Main test function"""
    tester = PDFSpecificTester()
    results = await tester.test_both_pdfs()
    return results

if __name__ == "__main__":
    import asyncio
    results = asyncio.run(main())