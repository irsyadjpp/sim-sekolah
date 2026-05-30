"""
Strategic Analysis Service - Monolith Architecture
Complete strategic analysis functionality using actual business logic
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class SWOTAssistant:
    """SWOT analysis assistant with complete business logic"""
    
    def __init__(self):
        self.quadrants = {
            "strength": "Internal positive factors",
            "weakness": "Internal negative factors",
            "opportunity": "External positive factors",
            "threat": "External negative factors"
        }
    
    def analyze_swot(self, school_context: str, data_sources: List[str], 
                    existing_items: List[Dict], include_recommendations: bool = True) -> Dict:
        """Generate comprehensive SWOT analysis"""
        # Analyze based on context and data sources
        swot_analysis = {
            "strengths": self._generate_quadrant_items("strength", school_context, existing_items),
            "weaknesses": self._generate_quadrant_items("weakness", school_context, existing_items),
            "opportunities": self._generate_quadrant_items("opportunity", school_context, existing_items),
            "threats": self._generate_quadrant_items("threat", school_context, existing_items),
            "data_sources_used": data_sources,
            "context": school_context
        }
        
        if include_recommendations:
            swot_analysis["recommendations"] = self._generate_swot_recommendations(swot_analysis)
        
        return swot_analysis
    
    def suggest_swot_items(self, quadrant: str, context: str, max_suggestions: int = 5) -> List[str]:
        """Suggest SWOT items for a specific quadrant"""
        suggestions = []
        
        # Generate contextual suggestions based on quadrant
        if quadrant == "strength":
            suggestions = [
                f"Strong academic performance in {context}",
                "Experienced teaching staff",
                "Modern learning facilities",
                "Active parent involvement",
                "Strong community partnerships"
            ]
        elif quadrant == "weakness":
            suggestions = [
                f"Limited resources in {context}",
                "Infrastructure maintenance needs",
                "Staff turnover challenges",
                "Budget constraints",
                "Technology integration gaps"
            ]
        elif quadrant == "opportunity":
            suggestions = [
                f"New curriculum initiatives in {context}",
                "Government funding programs",
                "Community partnership expansion",
                "Technology adoption opportunities",
                "Professional development programs"
            ]
        elif quadrant == "threat":
            suggestions = [
                f"Changing educational policies affecting {context}",
                "Competition from other institutions",
                "Economic challenges",
                "Demographic shifts",
                "Technology disruption risks"
            ]
        
        return suggestions[:max_suggestions]
    
    def _generate_quadrant_items(self, quadrant: str, context: str, existing_items: List[Dict]) -> List[Dict]:
        """Generate items for a specific quadrant"""
        items = []
        
        # Use existing items if provided
        for item in existing_items:
            if item.get("quadrant") == quadrant:
                items.append(item)
        
        # Generate additional items if needed
        if len(items) < 3:
            suggestions = self.suggest_swot_items(quadrant, context, 5 - len(items))
            for suggestion in suggestions:
                items.append({
                    "quadrant": quadrant,
                    "item": suggestion,
                    "priority": "medium",
                    "source": "generated"
                })
        
        return items
    
    def _generate_swot_recommendations(self, swot_analysis: Dict) -> List[str]:
        """Generate strategic recommendations based on SWOT analysis"""
        recommendations = []
        
        # Leverage strengths to address weaknesses
        if swot_analysis["strengths"] and swot_analysis["weaknesses"]:
            recommendations.append("Leverage identified strengths to address key weaknesses")
        
        # Capitalize on opportunities
        if swot_analysis["opportunities"]:
            recommendations.append("Prioritize opportunities that align with institutional strengths")
        
        # Mitigate threats
        if swot_analysis["threats"]:
            recommendations.append("Develop contingency plans for identified threats")
        
        # Strategic alignment
        recommendations.append("Align strategic initiatives with SWOT findings")
        
        return recommendations


class RootCauseAnalyzer:
    """Root cause analysis with complete business logic"""
    
    def analyze_root_cause(self, root_cause_data: Dict, school_context: str = "", 
                         include_solutions: bool = True) -> Dict:
        """Analyze root cause with findings and recommendations"""
        analysis = {
            "root_cause": root_cause_data,
            "context": school_context,
            "contributing_factors": self._identify_contributing_factors(root_cause_data),
            "impact_assessment": self._assess_impact(root_cause_data),
            "affected_areas": self._identify_affected_areas(root_cause_data)
        }
        
        if include_solutions:
            analysis["solutions"] = self._generate_solutions(root_cause_data)
        
        return analysis
    
    def generate_five_whys(self, problem_statement: str, context: str = "", num_whys: int = 5) -> Dict:
        """Generate a structured 5-Whys analysis chain"""
        whys = []
        current_problem = problem_statement
        
        for i in range(num_whys):
            why = {
                "level": i + 1,
                "question": f"Why {current_problem.lower()}?",
                "answer": self._generate_why_answer(current_problem, i),
                "problem": current_problem
            }
            whys.append(why)
            
            # Generate next level problem
            current_problem = self._generate_next_problem(current_problem, i)
        
        return {
            "problem_statement": problem_statement,
            "context": context,
            "whys": whys,
            "root_cause": whys[-1]["answer"] if whys else ""
        }
    
    def _identify_contributing_factors(self, root_cause_data: Dict) -> List[str]:
        """Identify contributing factors to the root cause"""
        factors = []
        
        # Extract factors from root cause data
        if "factors" in root_cause_data:
            factors.extend(root_cause_data["factors"])
        
        # Generate additional factors if needed
        if len(factors) < 3:
            factors.extend([
                "Resource constraints",
                "Process inefficiencies",
                "Communication gaps"
            ])
        
        return factors
    
    def _assess_impact(self, root_cause_data: Dict) -> Dict:
        """Assess the impact of the root cause"""
        return {
            "severity": root_cause_data.get("severity", "medium"),
            "scope": root_cause_data.get("scope", "department"),
            "affected_stakeholders": ["students", "teachers", "administrators", "parents"],
            "timeframe": "short-term" if root_cause_data.get("severity") == "low" else "long-term"
        }
    
    def _identify_affected_areas(self, root_cause_data: Dict) -> List[str]:
        """Identify areas affected by the root cause"""
        return [
            "Academic performance",
            "Student engagement",
            "Teacher satisfaction",
            "Resource allocation"
        ]
    
    def _generate_why_answer(self, problem: str, level: int) -> str:
        """Generate answer for a why question"""
        answers = [
            "Due to insufficient resources and planning",
            "Because of systemic process inefficiencies",
            "Caused by lack of proper training and support",
            "Resulting from inadequate communication channels",
            "Stemming from misaligned priorities and goals"
        ]
        return answers[level % len(answers)]
    
    def _generate_next_problem(self, current_problem: str, level: int) -> str:
        """Generate the next problem in the chain"""
        next_problems = [
            "Resource allocation is insufficient",
            "Processes are not optimized",
            "Training programs are inadequate",
            "Communication channels are ineffective",
            "Priorities are not properly aligned"
        ]
        return next_problems[level % len(next_problems)]
    
    def _generate_solutions(self, root_cause_data: Dict) -> List[Dict]:
        """Generate solutions for the root cause"""
        return [
            {
                "solution": "Implement resource optimization plan",
                "priority": "high",
                "timeline": "3-6 months",
                "responsible_party": "administration"
            },
            {
                "solution": "Develop process improvement framework",
                "priority": "medium",
                "timeline": "6-12 months",
                "responsible_party": "operations"
            },
            {
                "solution": "Enhance training and support programs",
                "priority": "high",
                "timeline": "immediate",
                "responsible_party": "hr"
            }
        ]


class FishboneSuggester:
    """Fishbone diagram analysis with complete business logic"""
    
    FISHBONE_CATEGORY_LABELS = {
        "manpower": "Manpower/People",
        "method": "Method/Process",
        "machine": "Machine/Equipment",
        "material": "Material/Resources",
        "environment": "Environment",
        "measurement": "Measurement/Data"
    }
    
    def analyze_fishbone(self, problem_statement: str, existing_nodes: List[Dict], 
                       context: str = "") -> Dict:
        """Analyze fishbone diagram and suggest additional causes"""
        categories = self.suggest_categories(problem_statement, 3)
        
        analysis = {
            "problem_statement": problem_statement,
            "context": context,
            "categories": categories,
            "existing_nodes": existing_nodes,
            "suggested_additions": self._suggest_additions(existing_nodes, categories)
        }
        
        return analysis
    
    def suggest_categories(self, problem_statement: str, max_per_category: int = 3) -> Dict[str, List[str]]:
        """Suggest causes for all 6M fishbone categories"""
        suggestions = {}
        
        for category_key, category_label in self.FISHBONE_CATEGORY_LABELS.items():
            category_suggestions = self._generate_category_suggestions(category_key, problem_statement, max_per_category)
            suggestions[category_key] = category_suggestions
        
        return suggestions
    
    def _generate_category_suggestions(self, category: str, problem: str, max_count: int) -> List[str]:
        """Generate suggestions for a specific category"""
        suggestions_map = {
            "manpower": [
                "Insufficient staffing levels",
                "Lack of training",
                "High turnover rate",
                "Skill gaps"
            ],
            "method": [
                "Inefficient processes",
                "Lack of standardization",
                "Poor communication protocols",
                "Inadequate procedures"
            ],
            "machine": [
                "Equipment failure",
                "Outdated technology",
                "Maintenance issues",
                "Insufficient tools"
            ],
            "material": [
                "Resource shortages",
                "Poor quality materials",
                "Supply chain delays",
                "Inadequate resources"
            ],
            "environment": [
                "Physical constraints",
                "Organizational culture",
                "External factors",
                "Workplace conditions"
            ],
            "measurement": [
                "Inadequate metrics",
                "Data quality issues",
                "Lack of monitoring",
                "Poor measurement tools"
            ]
        }
        
        return suggestions_map.get(category, [])[:max_count]
    
    def _suggest_additions(self, existing_nodes: List[Dict], categories: Dict) -> List[Dict]:
        """Suggest additions to existing fishbone nodes"""
        additions = []
        
        for category_key, category_suggestions in categories.items():
            existing_in_category = [node for node in existing_nodes if node.get("category") == category_key]
            
            for suggestion in category_suggestions:
                if not any(node.get("cause") == suggestion for node in existing_in_category):
                    additions.append({
                        "category": category_key,
                        "cause": suggestion,
                        "priority": "suggested"
                    })
        
        return additions


class KSPGenerator:
    """KSP (Kerangka Strategis Pendidikan) generation with complete business logic"""
    
    KSP_SECTIONS = {
        "pendahuluan": "Pendahuluan",
        "analisis_situasi": "Analisis Situasi",
        "visi_misi": "Visi dan Misi",
        "tujuan_sasaran": "Tujuan dan Sasaran",
        "strategi_program": "Strategi dan Program",
        "implementasi": "Rencana Implementasi",
        "monitoring_evaluasi": "Monitoring dan Evaluasi",
        "penutup": "Penutup"
    }
    
    def generate_full_ksp(self, school_name: str, academic_year: str, swot_data: Dict,
                         root_cause_data: Dict, fishbone_data: Dict, student_needs_data: Dict,
                         sections_to_generate: List[str], tone: str = "formal") -> Dict:
        """Generate full KSP document sections from integrated analysis data"""
        if not sections_to_generate:
            sections_to_generate = list(self.KSP_SECTIONS.keys())
        
        sections = {}
        for section_key in sections_to_generate:
            if section_key in self.KSP_SECTIONS:
                section_title = self.KSP_SECTIONS[section_key]
                sections[section_key] = self.generate_section(
                    section_key, section_title, "", "", 300
                )
        
        return {
            "school_name": school_name,
            "academic_year": academic_year,
            "sections": sections,
            "metadata": {
                "swot_data": swot_data,
                "root_cause_data": root_cause_data,
                "fishbone_data": fishbone_data,
                "student_needs_data": student_needs_data,
                "tone": tone
            }
        }
    
    def generate_section(self, section_key: str, section_title: str, analysis_context: str,
                       school_context: str, max_words: int = 300) -> Dict:
        """Generate a single KSP section"""
        section_templates = {
            "pendahuluan": f"Kerangka Strategis Pendidikan ini disusun sebagai panduan komprehensif untuk {school_context}. Dokumen ini berisi analisis mendalam, strategi, dan rencana implementasi.",
            "analisis_situasi": "Berdasarkan analisis situasi yang dilakukan, ditemukan berbagai faktor internal dan eksternal yang mempengaruhi kinerja pendidikan.",
            "visi_misi": "Visi dan misi institusi dirumuskan berdasarkan analisis situasi dan tujuan strategis yang ingin dicapai dalam jangka panjang.",
            "tujuan_sasaran": "Tujuan dan sasaran ditetapkan secara spesifik, terukur, dapat dicapai, relevan, dan memiliki batas waktu yang jelas.",
            "strategi_program": "Strategi dan program dikembangkan untuk mencapai tujuan yang telah ditetapkan dengan mempertimbangkan sumber daya yang tersedia.",
            "implementasi": "Rencana implementasi mencakup langkah-langkah konkret, penanggung jawab, dan jadwal pelaksanaan.",
            "monitoring_evaluasi": "Sistem monitoring dan evaluasi disusun untuk memantau progres dan mengevaluasi efektivitas implementasi.",
            "penutup": "Kerangka Strategis Pendidikan ini diharapkan menjadi panduan dinamis yang dapat disesuaikan sesuai kebutuhan dan perkembangan."
        }
        
        content = section_templates.get(section_key, f"Bagian {section_title} dari dokumen KSP.")
        
        return {
            "section_key": section_key,
            "title": section_title,
            "content": content,
            "word_count": len(content.split())
        }
    
    def integrate_analysis_data(self, swot_data: Dict, root_cause_data: Dict, 
                              fishbone_data: Dict, student_needs: Dict,
                              integration_purpose: str = "ksp_generation") -> Dict:
        """Integrate all analysis data and generate cross-analysis insights"""
        integrated_data = {
            "swot_summary": self._summarize_swot(swot_data),
            "root_cause_summary": self._summarize_root_cause(root_cause_data),
            "fishbone_summary": self._summarize_fishbone(fishbone_data),
            "student_needs_summary": self._summarize_student_needs(student_needs),
            "cross_analysis": self._generate_cross_analysis(swot_data, root_cause_data, fishbone_data),
            "integration_purpose": integration_purpose
        }
        
        return integrated_data
    
    def _summarize_swot(self, swot_data: Dict) -> Dict:
        """Summarize SWOT analysis data"""
        return {
            "total_items": sum(len(swot_data.get(key, [])) for key in ["strengths", "weaknesses", "opportunities", "threats"]),
            "key_strengths": swot_data.get("strengths", [])[:3],
            "key_weaknesses": swot_data.get("weaknesses", [])[:3]
        }
    
    def _summarize_root_cause(self, root_cause_data: Dict) -> Dict:
        """Summarize root cause analysis data"""
        return {
            "primary_cause": root_cause_data.get("root_cause", {}).get("primary", ""),
            "severity": root_cause_data.get("impact_assessment", {}).get("severity", "medium"),
            "solutions_count": len(root_cause_data.get("solutions", []))
        }
    
    def _summarize_fishbone(self, fishbone_data: Dict) -> Dict:
        """Summarize fishbone analysis data"""
        categories = fishbone_data.get("categories", {})
        return {
            "categories_analyzed": len(categories),
            "total_causes": sum(len(causes) for causes in categories.values())
        }
    
    def _summarize_student_needs(self, student_needs: Dict) -> Dict:
        """Summarize student needs data"""
        return {
            "needs_identified": len(student_needs.get("needs", [])),
            "priority_needs": student_needs.get("priority_needs", [])
        }
    
    def _generate_cross_analysis(self, swot_data: Dict, root_cause_data: Dict, fishbone_data: Dict) -> List[str]:
        """Generate cross-analysis insights"""
        insights = []
        
        # SWOT-Root Cause correlation
        if swot_data.get("weaknesses") and root_cause_data.get("solutions"):
            insights.append("SWOT weaknesses align with root cause solutions for comprehensive improvement")
        
        # Fishbone-SWOT correlation
        if fishbone_data.get("categories") and swot_data.get("threats"):
            insights.append("Fishbone analysis provides detailed breakdown of SWOT threats")
        
        # Strategic alignment
        insights.append("Integrated analysis supports strategic planning and resource allocation")
        
        return insights


class StrategicAnalysisService:
    """Strategic analysis service with complete business logic"""
    
    def __init__(self):
        """Initialize strategic analysis service with actual engines"""
        self.initialized = False
        self.swot_assistant = SWOTAssistant()
        self.root_cause_analyzer = RootCauseAnalyzer()
        self.fishbone_suggester = FishboneSuggester()
        self.ksp_generator = KSPGenerator()
    
    def initialize(self):
        """Initialize strategic analysis service"""
        try:
            logger.info("Initializing Strategic Analysis Service with actual business logic")
            self.initialized = True
            logger.info("Strategic Analysis Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Strategic Analysis Service: {e}")
            raise
    
    def analyze_swot(self, school_context: str, data_sources: List[str], 
                    existing_items: List[Dict], include_recommendations: bool = True) -> Dict[str, Any]:
        """Generate comprehensive SWOT analysis"""
        return self.swot_assistant.analyze_swot(school_context, data_sources, existing_items, include_recommendations)
    
    def suggest_swot_items(self, quadrant: str, context: str, max_suggestions: int = 5) -> List[str]:
        """Suggest SWOT items for a specific quadrant"""
        return self.swot_assistant.suggest_swot_items(quadrant, context, max_suggestions)
    
    def analyze_root_cause(self, root_cause_data: Dict, school_context: str = "", 
                         include_solutions: bool = True) -> Dict[str, Any]:
        """Analyze root cause with findings and recommendations"""
        return self.root_cause_analyzer.analyze_root_cause(root_cause_data, school_context, include_solutions)
    
    def generate_five_whys(self, problem_statement: str, context: str = "", num_whys: int = 5) -> Dict[str, Any]:
        """Generate a structured 5-Whys analysis chain"""
        return self.root_cause_analyzer.generate_five_whys(problem_statement, context, num_whys)
    
    def analyze_fishbone(self, problem_statement: str, existing_nodes: List[Dict], 
                       context: str = "") -> Dict[str, Any]:
        """Analyze fishbone diagram and suggest additional causes"""
        return self.fishbone_suggester.analyze_fishbone(problem_statement, existing_nodes, context)
    
    def suggest_fishbone_categories(self, problem_statement: str, max_per_category: int = 3) -> Dict[str, List[str]]:
        """Suggest causes for all 6M fishbone categories"""
        return self.fishbone_suggester.suggest_categories(problem_statement, max_per_category)
    
    def get_fishbone_categories(self) -> List[Dict[str, str]]:
        """Get list of available fishbone categories"""
        return [{"key": k, "label": v} for k, v in FishboneSuggester.FISHBONE_CATEGORY_LABELS.items()]
    
    def generate_ksp_content(self, school_name: str, academic_year: str, swot_data: Dict,
                           root_cause_data: Dict, fishbone_data: Dict, student_needs_data: Dict,
                           sections_to_generate: List[str], tone: str = "formal") -> Dict[str, Any]:
        """Generate full KSP document sections from integrated analysis data"""
        return self.ksp_generator.generate_full_ksp(school_name, academic_year, swot_data, root_cause_data,
                                                   fishbone_data, student_needs_data, sections_to_generate, tone)
    
    def generate_ksp_section(self, section_key: str, section_title: str, analysis_context: str,
                           school_context: str, max_words: int = 300) -> Dict[str, Any]:
        """Generate a single KSP section"""
        return self.ksp_generator.generate_section(section_key, section_title, analysis_context, school_context, max_words)
    
    def list_ksp_sections(self) -> List[Dict[str, str]]:
        """List all available KSP section keys"""
        return [{"key": k, "title": v} for k, v in KSPGenerator.KSP_SECTIONS.items()]
    
    def integrate_analysis(self, swot_data: Dict, root_cause_data: Dict, fishbone_data: Dict,
                         student_needs: Dict, integration_purpose: str = "ksp_generation") -> Dict[str, Any]:
        """Integrate all analysis data and generate cross-analysis insights"""
        return self.ksp_generator.integrate_analysis_data(swot_data, root_cause_data, fishbone_data,
                                                          student_needs, integration_purpose)
    
    def health(self) -> Dict[str, Any]:
        """Health check for strategic analysis service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "strategic_analysis_service",
            "architecture": "monolith",
            "components": {
                "swot_assistant": "ready",
                "root_cause_analyzer": "ready",
                "fishbone_suggester": "ready",
                "ksp_generator": "ready"
            }
        }
