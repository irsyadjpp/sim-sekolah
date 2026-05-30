"""
Test actual monolith components with sample PDF files
Tests the working components that have been migrated from legacy services
"""
import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime

sys.path.append('/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/monolith')

import fitz  # PyMuPDF

# Import actual working components
from app.extractors.table_extractor import TableExtractor
from app.extractors.image_extractor import ImageExtractor
from app.extractors.ocr_extractor import OCRExtractor
from app.extractors.layout_detector import LayoutDetector
from app.extractors.enhanced_layout_detector import EnhancedLayoutDetector
from app.extractors.formula_extractor import FormulaExtractor
from app.extractors.figure_extractor import FigureExtractor

from app.chunkers.competency_chunker import CompetencyChunker
from app.chunkers.activity_chunker import ActivityChunker
from app.chunkers.assessment_chunker import AssessmentChunker
from app.chunkers.inquiry_chunker import InquiryChunker
from app.chunkers.lesson_plan_chunker import LessonPlanChunker

from app.builders.chunk_builder import ChunkBuilder
from app.enrichers.chunk_enricher import ChunkEnricher
from app.hierarchy.hierarchy_detector import HierarchyDetector
from app.pedagogy.pedagogy_classifier import PedagogyClassifier
from app.taxonomy.taxonomy_tagger import TaxonomyTagger

# Sample file paths
BKB10_PDF = "/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge/sample/bkb10.pdf"
SIKLUS_AIR_PDF = "/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge/sample/siklus-air.pdf"

class ComponentTester:
    def __init__(self):
        self.results = {}
        
    def print_separator(self, title):
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
        
    def print_result(self, component_name, result):
        print(f"\n{'-'*80}")
        print(f"  COMPONENT: {component_name}")
        print(f"{'-'*80}")
        if isinstance(result, (dict, list)):
            print(json.dumps(result, indent=2, default=str))
        else:
            print(str(result))
    
    def test_pdf_basic_info(self, pdf_path):
        """Test basic PDF info extraction"""
        self.print_separator("BASIC PDF INFO")
        print(f"Testing file: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
            result = {
                "file_name": Path(pdf_path).name,
                "page_count": doc.page_count,
                "metadata": doc.metadata,
                "file_size": os.path.getsize(pdf_path)
            }
            doc.close()
            
            self.results['pdf_basic_info'] = result
            self.print_result("Basic PDF Info", result)
            return result
            
        except Exception as e:
            error_msg = f"Error getting PDF info: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['pdf_basic_info'] = {'error': error_msg}
            return None
    
    def test_text_extraction(self, pdf_path):
        """Test basic text extraction from PDF"""
        self.print_separator("TEXT EXTRACTION")
        print(f"Testing file: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
            text_content = []
            
            for page_num in range(min(doc.page_count, 3)):  # Test first 3 pages
                page = doc[page_num]
                text = page.get_text()
                text_content.append({
                    "page_number": page_num + 1,
                    "character_count": len(text),
                    "sample_text": text[:200] + "..." if len(text) > 200 else text
                })
            
            doc.close()
            
            result = {
                "total_pages_tested": len(text_content),
                "text_extraction_results": text_content
            }
            
            self.results['text_extraction'] = result
            self.print_result("Text Extraction", result)
            return result
            
        except Exception as e:
            error_msg = f"Error extracting text: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['text_extraction'] = {'error': error_msg}
            return None
    
    def test_table_extractor(self, pdf_path):
        """Test TableExtractor component"""
        self.print_separator("TABLE EXTRACTOR")
        print(f"Testing file: {pdf_path}")
        
        try:
            extractor = TableExtractor()
            tables = extractor.extract(pdf_path)
            
            result = {
                "tables_found": len(tables),
                "table_details": tables[:5]  # Show first 5 tables
            }
            
            self.results['table_extractor'] = result
            self.print_result("Table Extractor", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in TableExtractor: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['table_extractor'] = {'error': error_msg}
            return None
    
    def test_image_extractor(self, pdf_path):
        """Test ImageExtractor component"""
        self.print_separator("IMAGE EXTRACTOR")
        print(f"Testing file: {pdf_path}")
        
        try:
            extractor = ImageExtractor()
            images = extractor.extract(pdf_path)
            
            result = {
                "images_found": len(images) if images else 0,
                "image_details": images[:5] if images else []
            }
            
            self.results['image_extractor'] = result
            self.print_result("Image Extractor", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in ImageExtractor: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['image_extractor'] = {'error': error_msg}
            return None
    
    def test_layout_detector(self, pdf_path):
        """Test LayoutDetector component"""
        self.print_separator("LAYOUT DETECTOR")
        print(f"Testing file: {pdf_path}")
        
        try:
            detector = LayoutDetector()
            layouts = detector.detect(pdf_path)
            
            result = {
                "layouts_detected": len(layouts) if layouts else 0,
                "layout_details": layouts[:3] if layouts else []
            }
            
            self.results['layout_detector'] = result
            self.print_result("Layout Detector", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in LayoutDetector: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['layout_detector'] = {'error': error_msg}
            return None
    
    def test_enhanced_layout_detector(self, pdf_path):
        """Test EnhancedLayoutDetector component"""
        self.print_separator("ENHANCED LAYOUT DETECTOR")
        print(f"Testing file: {pdf_path}")
        
        try:
            detector = EnhancedLayoutDetector()
            layouts = detector.detect(pdf_path)
            
            result = {
                "enhanced_layouts_detected": len(layouts) if layouts else 0,
                "layout_details": layouts[:3] if layouts else []
            }
            
            self.results['enhanced_layout_detector'] = result
            self.print_result("Enhanced Layout Detector", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in EnhancedLayoutDetector: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['enhanced_layout_detector'] = {'error': error_msg}
            return None
    
    def test_competency_chunker(self, pdf_path):
        """Test CompetencyChunker component"""
        self.print_separator("COMPETENCY CHUNKER")
        
        try:
            # First extract text from PDF
            doc = fitz.open(pdf_path)
            text_content = ""
            for page in doc[:2]:  # Get first 2 pages
                text_content += page.get_text()
            doc.close()
            
            chunker = CompetencyChunker()
            chunks = chunker.chunk(
                content=text_content[:1000],  # Sample text
                curriculum_phase="phase_b",
                subject="IPA"
            )
            
            result = {
                "chunks_created": len(chunks) if chunks else 0,
                "chunk_details": chunks[:3] if chunks else []
            }
            
            self.results['competency_chunker'] = result
            self.print_result("Competency Chunker", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in CompetencyChunker: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['competency_chunker'] = {'error': error_msg}
            return None
    
    def test_activity_chunker(self, pdf_path):
        """Test ActivityChunker component"""
        self.print_separator("ACTIVITY CHUNKER")
        
        try:
            # First extract text from PDF
            doc = fitz.open(pdf_path)
            text_content = ""
            for page in doc[:2]:  # Get first 2 pages
                text_content += page.get_text()
            doc.close()
            
            chunker = ActivityChunker()
            chunks = chunker.chunk(
                content=text_content[:1000],  # Sample text
                activity_type="praktikum"
            )
            
            result = {
                "chunks_created": len(chunks) if chunks else 0,
                "chunk_details": chunks[:3] if chunks else []
            }
            
            self.results['activity_chunker'] = result
            self.print_result("Activity Chunker", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in ActivityChunker: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['activity_chunker'] = {'error': error_msg}
            return None
    
    def test_assessment_chunker(self, pdf_path):
        """Test AssessmentChunker component"""
        self.print_separator("ASSESSMENT CHUNKER")
        
        try:
            # First extract text from PDF
            doc = fitz.open(pdf_path)
            text_content = ""
            for page in doc[:2]:  # Get first 2 pages
                text_content += page.get_text()
            doc.close()
            
            chunker = AssessmentChunker()
            chunks = chunker.chunk(
                content=text_content[:1000],  # Sample text
                assessment_type="kuis"
            )
            
            result = {
                "chunks_created": len(chunks) if chunks else 0,
                "chunk_details": chunks[:3] if chunks else []
            }
            
            self.results['assessment_chunker'] = result
            self.print_result("Assessment Chunker", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in AssessmentChunker: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['assessment_chunker'] = {'error': error_msg}
            return None
    
    def test_chunk_builder(self, pdf_path):
        """Test ChunkBuilder component"""
        self.print_separator("CHUNK BUILDER")
        
        try:
            # First extract text from PDF
            doc = fitz.open(pdf_path)
            text_content = doc[0].get_text()  # Get first page
            doc.close()
            
            builder = ChunkBuilder()
            chunk_data = {
                "content": text_content[:500],
                "chunk_id": "test_chunk_1",
                "metadata": {
                    "subject": "IPA",
                    "grade_level": "6"
                }
            }
            
            built_chunk = builder.build(chunk_data, chunk_data["metadata"])
            
            result = {
                "chunk_built": built_chunk is not None,
                "chunk_details": built_chunk
            }
            
            self.results['chunk_builder'] = result
            self.print_result("Chunk Builder", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in ChunkBuilder: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['chunk_builder'] = {'error': error_msg}
            return None
    
    def test_chunk_enricher(self, pdf_path):
        """Test ChunkEnricher component"""
        self.print_separator("CHUNK ENRICHER")
        
        try:
            # First extract text from PDF
            doc = fitz.open(pdf_path)
            text_content = doc[0].get_text()  # Get first page
            doc.close()
            
            enricher = ChunkEnricher()
            chunks = [{
                "content": text_content[:500],
                "chunk_id": "test_chunk_1",
                "metadata": {
                    "subject": "IPA",
                    "grade_level": "6"
                }
            }]
            
            enriched_chunks = enricher.enrich(chunks, {"subject": "IPA", "grade": "6"})
            
            result = {
                "chunks_enriched": len(enriched_chunks) if enriched_chunks else 0,
                "chunk_details": enriched_chunks[:2] if enriched_chunks else []
            }
            
            self.results['chunk_enricher'] = result
            self.print_result("Chunk Enricher", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in ChunkEnricher: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['chunk_enricher'] = {'error': error_msg}
            return None
    
    def test_hierarchy_detector(self, pdf_path):
        """Test HierarchyDetector component"""
        self.print_separator("HIERARCHY DETECTOR")
        
        try:
            # First extract text from PDF
            doc = fitz.open(pdf_path)
            text_content = doc[0].get_text()  # Get first page
            doc.close()
            
            detector = HierarchyDetector()
            chunks = [{
                "content": text_content[:300],
                "chunk_id": "test_chunk_1"
            }]
            
            hierarchy = detector.detect_hierarchy(chunks)
            
            result = {
                "hierarchy_detected": hierarchy is not None,
                "hierarchy_details": hierarchy
            }
            
            self.results['hierarchy_detector'] = result
            self.print_result("Hierarchy Detector", result)
            return result
            
        except Exception as e:
            error_msg = f"Error in HierarchyDetector: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['hierarchy_detector'] = {'error': error_msg}
            return None
    
    def test_pedagogy_classifier(self, pdf_path):
        """Test PedagogyClassifier component"""
        self.print_separator("PEDAGOGY CLASSIFIER")
        
        try:
            # First extract text from PDF
            doc = fitz.open(pdf_path)
            text_content = doc[0].get_text()  # Get first page
            doc.close()
            
            classifier = PedagogyClassifier()
            
            result = classifier.classify(text_content[:500])
            
            result_data = {
                "classification_result": result
            }
            
            self.results['pedagogy_classifier'] = result_data
            self.print_result("Pedagogy Classifier", result_data)
            return result_data
            
        except Exception as e:
            error_msg = f"Error in PedagogyClassifier: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['pedagogy_classifier'] = {'error': error_msg}
            return None
    
    def test_taxonomy_tagger(self, pdf_path):
        """Test TaxonomyTagger component"""
        self.print_separator("TAXONOMY TAGGER")
        
        try:
            # First extract text from PDF
            doc = fitz.open(pdf_path)
            text_content = doc[0].get_text()  # Get first page
            doc.close()
            
            tagger = TaxonomyTagger()
            
            result = tagger.tag(text_content[:500], "IPA", "6")
            
            result_data = {
                "taxonomy_result": result
            }
            
            self.results['taxonomy_tagger'] = result_data
            self.print_result("Taxonomy Tagger", result_data)
            return result_data
            
        except Exception as e:
            error_msg = f"Error in TaxonomyTagger: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['taxonomy_tagger'] = {'error': error_msg}
            return None
    
    def run_all_tests(self, pdf_path):
        """Run all component tests for a PDF file"""
        self.print_separator(f"TESTING ALL COMPONENTS - {Path(pdf_path).name}")
        
        # Basic PDF tests
        self.test_pdf_basic_info(pdf_path)
        self.test_text_extraction(pdf_path)
        
        # Extractor tests
        self.test_table_extractor(pdf_path)
        self.test_image_extractor(pdf_path)
        self.test_layout_detector(pdf_path)
        self.test_enhanced_layout_detector(pdf_path)
        
        # Chunker tests
        self.test_competency_chunker(pdf_path)
        self.test_activity_chunker(pdf_path)
        self.test_assessment_chunker(pdf_path)
        
        # Builder/Enricher tests
        self.test_chunk_builder(pdf_path)
        self.test_chunk_enricher(pdf_path)
        
        # Advanced component tests
        self.test_hierarchy_detector(pdf_path)
        self.test_pedagogy_classifier(pdf_path)
        self.test_taxonomy_tagger(pdf_path)
        
        return self.results
    
    def save_results(self):
        """Save test results to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/monolith/component_test_results_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n✅ Component test results saved to: {output_file}")
        return output_file

def main():
    """Main test function"""
    print("🚀 Starting AI Platform Monolith Component Tests")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = ComponentTester()
    
    # Test with bkb10.pdf
    print(f"\n📄 Testing with BKB10 PDF...")
    bkb10_results = tester.run_all_tests(BKB10_PDF)
    
    # Test with siklus-air.pdf
    print(f"\n📄 Testing with SIKLUS AIR PDF...")
    siklus_air_results = tester.run_all_tests(SIKLUS_AIR_PDF)
    
    # Save results
    output_file = tester.save_results()
    
    # Print summary
    tester.print_separator("COMPONENT TEST SUMMARY")
    print(f"Total components tested: {len(tester.results)}")
    successful_tests = sum(1 for v in tester.results.values() if 'error' not in str(v))
    failed_tests = sum(1 for v in tester.results.values() if 'error' in str(v))
    print(f"Successful tests: {successful_tests}")
    print(f"Failed tests: {failed_tests}")
    
    print(f"\n✅ Component testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Results saved to: {output_file}")
    
    return tester.results

if __name__ == "__main__":
    results = main()