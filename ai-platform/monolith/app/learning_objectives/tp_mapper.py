"""
TP Mapper

This module maps Tujuan Pembelajaran (TP) to ATP (Alur Tujuan Pembelajaran),
assessment items, and learning activities.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class TPMapper:
    """Mapper for Tujuan Pembelajaran (Learning Objectives)"""
    
    def __init__(self):
        self.mapping_rules = self._initialize_mapping_rules()
    
    def map_tp_to_atp(
        self, 
        tps: List[Dict],
        cp_data: Dict,
        fase: str,
        mata_pelajaran: str
    ) -> List[Dict]:
        """Map TPs to ATP structure"""
        atp_structure = []
        
        # Group TPs by phase/period
        tp_groups = self._group_tps_by_period(tps)
        
        for period, period_tps in tp_groups.items():
            atp_item = {
                "atp_id": f"ATP_{fase}_{mata_pelajaran}_{period}",
                "fase": fase,
                "mata_pelajaran": mata_pelajaran,
                "periode": period,
                "minggu_ke": self._determine_week_range(period),
                "tujuan_pembelajaran": [tp["tujuan_pembelajaran"] for tp in period_tps],
                "tp_ids": [tp["tp_id"] for tp in period_tps],
                "alur_materi": self._generate_material_flow(period_tps),
                "created_at": datetime.utcnow().isoformat()
            }
            atp_structure.append(atp_item)
        
        return atp_structure
    
    def map_tp_to_assessment(
        self, 
        tps: List[Dict],
        assessment_type: str = "formatif"
    ) -> List[Dict]:
        """Map TPs to assessment items"""
        assessment_items = []
        
        for tp in tps:
            item = {
                "item_id": f"ITEM_{tp['tp_id']}",
                "tp_id": tp["tp_id"],
                "tujuan_pembelajaran": tp["tujuan_pembelajaran"],
                "domain": tp.get("domain", "kognitif"),
                "difficulty": tp.get("difficulty", "sedang"),
                "assessment_type": assessment_type,
                "item_type": self._determine_item_type(tp),
                "rubric_criteria": self._generate_rubric_criteria(tp),
                "created_at": datetime.utcnow().isoformat()
            }
            assessment_items.append(item)
        
        return assessment_items
    
    def map_tp_to_activity(
        self, 
        tps: List[Dict],
        activity_type: str = "pembelajaran"
    ) -> List[Dict]:
        """Map TPs to learning activities"""
        activities = []
        
        for tp in tps:
            activity = {
                "activity_id": f"ACT_{tp['tp_id']}",
                "tp_id": tp["tp_id"],
                "tujuan_pembelajaran": tp["tujuan_pembelajaran"],
                "domain": tp.get("domain", "kognitif"),
                "activity_type": activity_type,
                "metode_pembelajaran": self._suggest_method(tp),
                "langkah_pembelajaran": self._generate_activity_steps(tp),
                "sumber_belajar": self._suggest_resources(tp),
                "created_at": datetime.utcnow().isoformat()
            }
            activities.append(activity)
        
        return activities
    
    def map_tp_to_modul_ajar(
        self, 
        tps: List[Dict],
        fase: str,
        mata_pelajaran: str,
        topik: str
    ) -> Dict:
        """Map TPs to Modul Ajar structure"""
        modul_ajar = {
            "modul_ajar_id": f"MA_{fase}_{mata_pelajaran}_{topik.replace(' ', '_')}",
            "fase": fase,
            "mata_pelajaran": mata_pelajaran,
            "topik": topik,
            "tujuan_pembelajaran": [tp["tujuan_pembelajaran"] for tp in tps],
            "tp_ids": [tp["tp_id"] for tp in tps],
            "pemahaman_bermakna": self._generate_meaningful_understanding(tps),
            "inquiry_based": self._generate_inquiry_activities(tps),
            "p5_project": self._suggest_p5_project(tps),
            "asesmen": self._map_tp_to_assessment(tps),
            "created_at": datetime.utcnow().isoformat()
        }
        
        return modul_ajar
    
    def _group_tps_by_period(self, tps: List[Dict]) -> Dict:
        """Group TPs by learning period"""
        # Simple grouping - in production, use more sophisticated logic
        groups = {}
        period_size = max(1, len(tps) // 4)  # Divide into 4 periods
        
        for i, tp in enumerate(tps):
            period = (i // period_size) + 1
            if period not in groups:
                groups[period] = []
            groups[period].append(tp)
        
        return groups
    
    def _determine_week_range(self, period: int) -> str:
        """Determine week range for period"""
        week_ranges = {
            1: "Minggu 1-4",
            2: "Minggu 5-8",
            3: "Minggu 9-12",
            4: "Minggu 13-16"
        }
        return week_ranges.get(period, f"Minggu {(period-1)*4+1}-{period*4}")
    
    def _generate_material_flow(self, tps: List[Dict]) -> List[str]:
        """Generate material flow from TPs"""
        # Extract key concepts from TPs
        concepts = []
        for tp in tps:
            tp_text = tp["tujuan_pembelajaran"]
            # Simple concept extraction - in production, use NLP
            words = tp_text.split()
            if len(words) > 3:
                concepts.append(" ".join(words[-3:]))  # Last 3 words as concept
        
        return concepts
    
    def _determine_item_type(self, tp: Dict) -> str:
        """Determine assessment item type based on TP"""
        domain = tp.get("domain", "kognitif")
        difficulty = tp.get("difficulty", "sedang")
        
        if domain == "kognitif":
            if difficulty == "mudah":
                return "pilihan_ganda"
            elif difficulty == "sedang":
                return "isian_singkat"
            else:
                return "esai"
        elif domain == "psikomotorik":
            return "kinerja"
        else:  # afektif
            return "observasi"
    
    def _generate_rubric_criteria(self, tp: Dict) -> List[str]:
        """Generate rubric criteria from TP"""
        tp_text = tp["tujuan_pembelajaran"]
        
        # Simple criteria generation - in production, use AI
        criteria = [
            f"Memahami {tp_text[:30]}...",
            f"Menerapkan konsep {tp_text[:30]}...",
            f"Komunikasi hasil belajar"
        ]
        
        return criteria
    
    def _suggest_method(self, tp: Dict) -> str:
        """Suggest learning method based on TP"""
        domain = tp.get("domain", "kognitif")
        
        methods = {
            "kognitif": ["diskusi", "ceramah interaktif", "problem based learning"],
            "psikomotorik": ["praktik", "demonstrasi", "project based learning"],
            "afektif": ["role play", "simulasi", "cooperative learning"]
        }
        
        domain_methods = methods.get(domain, methods["kognitif"])
        return domain_methods[0]  # Return first suggestion
    
    def _generate_activity_steps(self, tp: Dict) -> List[str]:
        """Generate activity steps from TP"""
        tp_text = tp["tujuan_pembelajaran"]
        
        steps = [
            "Pendahuluan: Mengaitkan dengan pengalaman sebelumnya",
            f"Kegiatan Inti: {tp_text[:50]}...",
            "Penutup: Refleksi dan penyimpulan"
        ]
        
        return steps
    
    def _suggest_resources(self, tp: Dict) -> List[str]:
        """Suggest learning resources based on TP"""
        domain = tp.get("domain", "kognitif")
        
        resources = {
            "kognitif": ["buku teks", "video pembelajaran", "artikel"],
            "psikomotorik": ["alat praktik", "bahan demonstrasi", "laboratorium"],
            "afektif": ["cerita inspiratif", "kasus nyata", "media sosial"]
        }
        
        return resources.get(domain, resources["kognitif"])
    
    def _generate_meaningful_understanding(self, tps: List[Dict]) -> Dict:
        """Generate meaningful understanding components"""
        return {
            "konteks": "Kehidupan sehari-hari",
            "pertanyaan_pemantik": [
                "Apa yang sudah kamu ketahui?",
                "Mengapa hal ini penting?",
                "Bagaimana ini berguna?"
            ],
            "aktivitas_bermakna": [
                "Menghubungkan dengan pengalaman",
                "Mencari contoh nyata",
                "Menerapkan dalam konteks"
            ]
        }
    
    def _generate_inquiry_activities(self, tps: List[Dict]) -> List[Dict]:
        """Generate inquiry-based learning activities"""
        activities = []
        
        for tp in tps[:3]:  # Limit to 3 activities
            activity = {
                "pertanyaan": f"Bagaimana {tp['tujuan_pembelajaran'][:30]}...?",
                "penyelidikan": [
                    "Mencari informasi",
                    "Menganalisis data",
                    "Menarik kesimpulan"
                ],
                "produk": "Laporan penyelidikan"
            }
            activities.append(activity)
        
        return activities
    
    def _suggest_p5_project(self, tps: List[Dict]) -> Dict:
        """Suggest P5 (Projek Penguatan Profil Pelajar Pancasila) project"""
        return {
            "judul": "Profil Pelajar Pancasila Project",
            "dimensi": [
                "Beriman, bertakwa kepada Tuhan YME",
                "Berkebinekaan global",
                "Gotong royong",
                "Kreatif",
                "Mandiri",
                "Bernalar kritis"
            ],
            "aktivitas": [
                "Identifikasi masalah",
                "Perencanaan solusi",
                "Implementasi",
                "Presentasi hasil"
            ]
        }
    
    def _initialize_mapping_rules(self) -> Dict:
        """Initialize mapping rules"""
        return {
            "domain_to_method": {
                "kognitif": ["diskusi", "ceramah", "pbl"],
                "psikomotorik": ["praktik", "demonstrasi", "pbl"],
                "afektif": ["role play", "simulasi", "cooperative"]
            },
            "difficulty_to_item_type": {
                "mudah": "pilihan_ganda",
                "sedang": "isian_singkat",
                "sulit": "esai"
            }
        }
    
    def validate_mapping(
        self, 
        source_type: str, 
        target_type: str, 
        mapped_data: List[Dict]
    ) -> Dict:
        """Validate mapping results"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {
                "total_items": len(mapped_data),
                "mapped_tps": len(set(item.get("tp_id", "") for item in mapped_data))
            }
        }
        
        # Check if all TPs are mapped
        if validation_result["statistics"]["mapped_tps"] < len(mapped_data):
            validation_result["warnings"].append(
                f"Some TPs may not be mapped: {validation_result['statistics']['mapped_tps']} TPs mapped"
            )
        
        # Check data completeness
        for item in mapped_data:
            if not item.get("tp_id"):
                validation_result["valid"] = False
                validation_result["errors"].append("Item missing tp_id")
        
        return validation_result
