"""
TP Activity Linker

This module links Tujuan Pembelajaran (TP) to learning activities and instructional strategies.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ActivityType(str, Enum):
    """Types of learning activities"""
    PEMBELAJARAN = "pembelajaran"
    PENGAYAAN = "pengayaan"
    REMEDIAL = "remedial"
    P5 = "p5"
    PROYEK = "proyek"


class InstructionalStrategy(str, Enum):
    """Instructional strategies"""
    DISKUSI = "diskusi"
    CERAMAH_INTERAKTIF = "ceramah_interaktif"
    PROBLEM_BASED_LEARNING = "problem_based_learning"
    PROJECT_BASED_LEARNING = "project_based_learning"
    INQUIRY_BASED_LEARNING = "inquiry_based_learning"
    COOPERATIVE_LEARNING = "cooperative_learning"
    ROLE_PLAY = "role_play"
    SIMULASI = "simulasi"


class TPActivityLinker:
    """Linker for TP to learning activities"""
    
    def __init__(self):
        self.linkage_rules = self._initialize_linkage_rules()
        self.activity_templates = self._initialize_activity_templates()
    
    def link_tp_to_activity(
        self, 
        tp: Dict,
        activity_type: ActivityType = ActivityType.PEMBELAJARAN
    ) -> Dict:
        """Link a TP to learning activities"""
        activities = self._generate_activities(tp, activity_type)
        
        linkage = {
            "linkage_id": f"LINK_{tp['tp_id']}_{activity_type.value}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "tp_id": tp["tp_id"],
            "tujuan_pembelajaran": tp["tujuan_pembelajaran"],
            "domain": tp.get("domain", "kognitif"),
            "difficulty": tp.get("difficulty", "sedang"),
            "activity_type": activity_type.value,
            "activities": activities,
            "instructional_strategies": self._suggest_strategies(tp),
            "learning_resources": self._suggest_resources(tp),
            "created_at": datetime.utcnow().isoformat()
        }
        
        return linkage
    
    def link_tp_batch_to_activity(
        self, 
        tps: List[Dict],
        activity_type: ActivityType = ActivityType.PEMBELAJARAN
    ) -> List[Dict]:
        """Link multiple TPs to learning activities"""
        linkages = []
        
        for tp in tps:
            linkage = self.link_tp_to_activity(tp, activity_type)
            linkages.append(linkage)
        
        return linkages
    
    def generate_learning_sequence(
        self, 
        tps: List[Dict],
        fase: str,
        mata_pelajaran: str
    ) -> Dict:
        """Generate learning sequence from TPs"""
        sequence = {
            "sequence_id": f"SEQ_{fase}_{mata_pelajaran}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "fase": fase,
            "mata_pelajaran": mata_pelajaran,
            "total_tps": len(tps),
            "learning_phases": self._generate_learning_phases(tps),
            "time_allocation": self._calculate_time_allocation(tps),
            "differentiation": self._generate_differentiation(tps),
            "created_at": datetime.utcnow().isoformat()
        }
        
        return sequence
    
    def link_tp_to_p5_project(
        self, 
        tp: Dict,
        p5_dimension: str
    ) -> Dict:
        """Link TP to P5 (Projek Penguatan Profil Pelajar Pancasila) project"""
        project = {
            "project_id": f"P5_{tp['tp_id']}_{p5_dimension}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "tp_id": tp["tp_id"],
            "tujuan_pembelajaran": tp["tujuan_pembelajaran"],
            "p5_dimension": p5_dimension,
            "project_title": self._generate_p5_title(tp, p5_dimension),
            "project_phases": self._generate_p5_phases(tp),
            "student_roles": self._assign_student_roles(tp),
            "assessment_criteria": self._generate_p5_assessment(tp),
            "created_at": datetime.utcnow().isoformat()
        }
        
        return project
    
    def suggest_differentiated_activities(
        self, 
        tp: Dict,
        student_needs: List[str]
    ) -> Dict:
        """Suggest differentiated activities based on student needs"""
        activities = []
        
        for need in student_needs:
            activity = self._generate_differentiated_activity(tp, need)
            activities.append(activity)
        
        return {
            "tp_id": tp["tp_id"],
            "student_needs": student_needs,
            "differentiated_activities": activities,
            "suggested_at": datetime.utcnow().isoformat()
        }
    
    def _generate_activities(self, tp: Dict, activity_type: ActivityType) -> List[Dict]:
        """Generate learning activities from TP"""
        activities = []
        
        domain = tp.get("domain", "kognitif")
        difficulty = tp.get("difficulty", "sedang")
        
        # Determine activity templates based on domain and activity type
        templates = self._get_activity_templates(domain, activity_type)
        
        for i, template in enumerate(templates):
            activity = {
                "activity_id": f"ACT_{tp['tp_id']}_{i+1}",
                "tp_id": tp["tp_id"],
                "activity_type": activity_type.value,
                "title": template["title"],
                "description": template["description"].format(tp_text=tp["tujuan_pembelajaran"]),
                "steps": self._generate_activity_steps(tp, template),
                "duration": template["duration"],
                "grouping": template["grouping"],
                "materials": template["materials"]
            }
            activities.append(activity)
        
        return activities
    
    def _suggest_strategies(self, tp: Dict) -> List[str]:
        """Suggest instructional strategies based on TP"""
        domain = tp.get("domain", "kognitif")
        difficulty = tp.get("difficulty", "sedang")
        
        strategies = {
            "kognitif": {
                "mudah": ["ceramah_interaktif", "diskusi"],
                "sedang": ["problem_based_learning", "inquiry_based_learning"],
                "sulit": ["project_based_learning", "cooperative_learning"]
            },
            "psikomotorik": {
                "mudah": ["demonstrasi", "praktik_terbimbing"],
                "sedang": ["praktik_mandiri", "simulasi"],
                "sulit": ["project_based_learning", "role_play"]
            },
            "afektif": {
                "mudah": ["ceramah_interaktif", "diskusi"],
                "sedang": ["role_play", "simulasi"],
                "sulit": ["cooperative_learning", "project_based_learning"]
            }
        }
        
        domain_strategies = strategies.get(domain, strategies["kognitif"])
        return domain_strategies.get(difficulty, domain_strategies["sedang"])
    
    def _suggest_resources(self, tp: Dict) -> List[str]:
        """Suggest learning resources based on TP"""
        domain = tp.get("domain", "kognitif")
        
        resources = {
            "kognitif": ["buku teks", "video pembelajaran", "artikel", "infografis"],
            "psikomotorik": ["alat praktik", "bahan demonstrasi", "laboratorium", "peralatan"],
            "afektif": ["cerita inspiratif", "kasus nyata", "media sosial", "video motivasi"]
        }
        
        return resources.get(domain, resources["kognitif"])
    
    def _generate_learning_phases(self, tps: List[Dict]) -> List[Dict]:
        """Generate learning phases from TPs"""
        phases = []
        
        # Divide TPs into learning phases
        phase_size = max(1, len(tps) // 3)
        
        for i in range(0, len(tps), phase_size):
            phase_tps = tps[i:i+phase_size]
            phase = {
                "phase_number": len(phases) + 1,
                "phase_name": self._get_phase_name(len(phases)),
                "tps": [tp["tp_id"] for tp in phase_tps],
                "duration": self._calculate_phase_duration(phase_tps),
                "focus_area": self._determine_focus_area(phase_tps)
            }
            phases.append(phase)
        
        return phases
    
    def _calculate_time_allocation(self, tps: List[Dict]) -> Dict:
        """Calculate time allocation for learning sequence"""
        total_time = len(tps) * 45  # 45 minutes per TP (average)
        
        return {
            "total_minutes": total_time,
            "total_hours": total_time / 60,
            "per_tp": 45,
            "break_time": total_time // 90 * 10  # 10 minutes break every 90 minutes
        }
    
    def _generate_differentiation(self, tps: List[Dict]) -> Dict:
        """Generate differentiation strategies"""
        return {
            "content": ["Sederhanakan materi", "Tambahkan contoh", "Gunakan visual"],
            "process": ["Waktu tambahan", "Bimbingan individu", "Kerja kelompok"],
            "product": ["Pilihan tugas", "Format berbeda", "Kriteria fleksibel"]
        }
    
    def _generate_p5_title(self, tp: Dict, p5_dimension: str) -> str:
        """Generate P5 project title"""
        dimension_names = {
            "beriman": "Proyek Keimanan",
            "berkebinekaan_global": "Proyek Keberagaman",
            "gotong_royong": "Proyek Gotong Royong",
            "kreatif": "Proyek Kreativitas",
            "mandiri": "Proyek Kemandirian",
            "bernalir_kritis": "Proyek Berpikir Kritis"
        }
        
        base_title = dimension_names.get(p5_dimension, "Proyek P5")
        return f"{base_title}: {tp['tujuan_pembelajaran'][:30]}..."
    
    def _generate_p5_phases(self, tp: Dict) -> List[Dict]:
        """Generate P5 project phases"""
        return [
            {
                "phase": "Perencanaan",
                "description": "Merencanakan proyek berdasarkan TP",
                "duration": "1 minggu"
            },
            {
                "phase": "Implementasi",
                "description": "Melaksanakan proyek",
                "duration": "2-3 minggu"
            },
            {
                "phase": "Presentasi",
                "description": "Presentasi hasil proyek",
                "duration": "1 minggu"
            }
        ]
    
    def _assign_student_roles(self, tp: Dict) -> List[str]:
        """Assign student roles for P5 project"""
        return [
            "Ketua Proyek",
            "Sekretaris",
            "Peneliti",
            "Presenter",
            "Dokumentator"
        ]
    
    def _generate_p5_assessment(self, tp: Dict) -> Dict:
        """Generate P5 assessment criteria"""
        return {
            "process_criteria": [
                "Partisipasi aktif",
                "Kolaborasi tim",
                "Pengelolaan waktu"
            ],
            "product_criteria": [
                "Kualitas hasil",
                "Kreativitas",
                "Relevansi dengan TP"
            ],
            "p5_dimension_alignment": True
        }
    
    def _generate_differentiated_activity(self, tp: Dict, need: str) -> Dict:
        """Generate differentiated activity based on student need"""
        need_strategies = {
            "remedial": {
                "title": "Aktivitas Remedial",
                "description": "Aktivitas dengan bimbingan intensif",
                "duration": "30 menit",
                "grouping": "individual atau berpasangan"
            },
            "pengayaan": {
                "title": "Aktivitas Pengayaan",
                "description": "Aktivitas tingkat lanjut",
                "duration": "25 menit",
                "grouping": "kelompok kecil"
            },
            "visual": {
                "title": "Aktivitas Visual",
                "description": "Aktivitas dengan dukungan visual",
                "duration": "20 menit",
                "grouping": "individual"
            },
            "auditori": {
                "title": "Aktivitas Auditori",
                "description": "Aktivitas dengan dukungan audio",
                "duration": "20 menit",
                "grouping": "individual"
            }
        }
        
        strategy = need_strategies.get(need, need_strategies["remedial"])
        
        return {
            "activity_id": f"DIFF_{tp['tp_id']}_{need}",
            "tp_id": tp["tp_id"],
            "student_need": need,
            "title": strategy["title"],
            "description": strategy["description"],
            "duration": strategy["duration"],
            "grouping": strategy["grouping"]
        }
    
    def _get_activity_templates(self, domain: str, activity_type: ActivityType) -> List[Dict]:
        """Get activity templates based on domain and activity type"""
        templates = self.activity_templates.get(domain, self.activity_templates["kognitif"])
        return templates.get(activity_type.value, templates["pembelajaran"])
    
    def _generate_activity_steps(self, tp: Dict, template: Dict) -> List[str]:
        """Generate activity steps from template"""
        base_steps = template.get("base_steps", [])
        
        # Customize steps based on TP
        customized_steps = [
            step.format(tp_text=tp["tujuan_pembelajaran"][:30])
            for step in base_steps
        ]
        
        return customized_steps
    
    def _get_phase_name(self, phase_number: int) -> str:
        """Get phase name based on number"""
        phase_names = ["Pendahuluan", "Kegiatan Inti", "Penutup"]
        return phase_names[phase_number % len(phase_names)]
    
    def _calculate_phase_duration(self, tps: List[Dict]) -> str:
        """Calculate duration for learning phase"""
        return f"{len(tps) * 45} menit"
    
    def _determine_focus_area(self, tps: List[Dict]) -> str:
        """Determine focus area for learning phase"""
        if not tps:
            return "Umum"
        
        # Extract key concepts from TPs
        concepts = []
        for tp in tps:
            tp_text = tp["tujuan_pembelajaran"]
            words = tp_text.split()
            if len(words) > 3:
                concepts.append(" ".join(words[-3:]))
        
        return ", ".join(concepts[:3]) if concepts else "Umum"
    
    def _initialize_linkage_rules(self) -> Dict:
        """Initialize linkage rules"""
        return {
            "max_activities_per_tp": 5,
            "min_activity_duration": 10,
            "max_activity_duration": 60
        }
    
    def _initialize_activity_templates(self) -> Dict:
        """Initialize activity templates"""
        return {
            "kognitif": {
                "pembelajaran": [
                    {
                        "title": "Diskusi Kelompok",
                        "description": "Diskusi tentang {tp_text}",
                        "duration": "20 menit",
                        "grouping": "kelompok kecil",
                        "materials": ["lembar kerja", "buku teks"],
                        "base_steps": [
                            "Pendahuluan: Mengaitkan dengan pengalaman sebelumnya",
                            "Diskusi: {tp_text}",
                            "Penutup: Kesimpulan"
                        ]
                    },
                    {
                        "title": "Problem Solving",
                        "description": "Memecahkan masalah terkait {tp_text}",
                        "duration": "25 menit",
                        "grouping": "kelompok",
                        "materials": ["lembar masalah", "kertas"],
                        "base_steps": [
                            "Presentasi masalah",
                            "Diskusi solusi",
                            "Implementasi",
                            "Presentasi hasil"
                        ]
                    }
                ],
                "pengayaan": [
                    {
                        "title": "Proyek Mini",
                        "description": "Proyek mini tentang {tp_text}",
                        "duration": "30 menit",
                        "grouping": "kelompok",
                        "materials": ["bahan proyek"],
                        "base_steps": [
                            "Perencanaan",
                            "Implementasi",
                            "Presentasi"
                        ]
                    }
                ],
                "remedial": [
                    {
                        "title": "Remedial Terbimbing",
                        "description": "Bimbingan untuk {tp_text}",
                        "duration": "20 menit",
                        "grouping": "individual",
                        "materials": ["bahan remedial"],
                        "base_steps": [
                            "Ulang materi",
                            "Latihan terbimbing",
                            "Evaluasi"
                        ]
                    }
                ],
                "p5": [
                    {
                        "title": "Proyek P5",
                        "description": "Proyek P5 terkait {tp_text}",
                        "duration": "2-3 minggu",
                        "grouping": "kelompok besar",
                        "materials": ["bahan proyek"],
                        "base_steps": [
                            "Perencanaan",
                            "Implementasi",
                            "Presentasi"
                        ]
                    }
                ]
            },
            "psikomotorik": {
                "pembelajaran": [
                    {
                        "title": "Demonstrasi",
                        "description": "Demonstrasi {tp_text}",
                        "duration": "25 menit",
                        "grouping": "kelas",
                        "materials": ["alat demonstrasi"],
                        "base_steps": [
                            "Demonstrasi guru",
                            "Praktik siswa",
                            "Evaluasi"
                        ]
                    },
                    {
                        "title": "Praktik Mandiri",
                        "description": "Praktik mandiri {tp_text}",
                        "duration": "30 menit",
                        "grouping": "individual",
                        "materials": ["alat praktik"],
                        "base_steps": [
                            "Persiapan",
                            "Praktik",
                            "Evaluasi"
                        ]
                    }
                ],
                "pengayaan": [
                    {
                        "title": "Proyek Kreatif",
                        "description": "Proyek kreatif {tp_text}",
                        "duration": "40 menit",
                        "grouping": "kelompok",
                        "materials": ["bahan proyek"],
                        "base_steps": [
                            "Perencanaan",
                            "Implementasi",
                            "Presentasi"
                        ]
                    }
                ],
                "remedial": [
                    {
                        "title": "Praktik Terbimbing",
                        "description": "Praktik terbimbing {tp_text}",
                        "duration": "25 menit",
                        "grouping": "berpasangan",
                        "materials": ["alat praktik"],
                        "base_steps": [
                            "Demonstrasi ulang",
                            "Praktik dengan bimbingan",
                            "Evaluasi"
                        ]
                    }
                ],
                "p5": [
                    {
                        "title": "Proyek Kinerja",
                        "description": "Proyek kinerja {tp_text}",
                        "duration": "2-3 minggu",
                        "grouping": "kelompok",
                        "materials": ["bahan proyek"],
                        "base_steps": [
                            "Perencanaan",
                            "Implementasi",
                            "Presentasi"
                        ]
                    }
                ]
            },
            "afektif": {
                "pembelajaran": [
                    {
                        "title": "Role Play",
                        "description": "Role play tentang {tp_text}",
                        "duration": "20 menit",
                        "grouping": "kelompok",
                        "materials": ["skenario"],
                        "base_steps": [
                            "Persiapan",
                            "Role play",
                            "Refleksi"
                        ]
                    },
                    {
                        "title": "Simulasi",
                        "description": "Simulasi {tp_text}",
                        "duration": "25 menit",
                        "grouping": "kelas",
                        "materials": ["bahan simulasi"],
                        "base_steps": [
                            "Persiapan",
                            "Simulasi",
                            "Debriefing"
                        ]
                    }
                ],
                "pengayaan": [
                    {
                        "title": "Proyek Sosial",
                        "description": "Proyek sosial {tp_text}",
                        "duration": "30 menit",
                        "grouping": "kelompok",
                        "materials": ["bahan proyek"],
                        "base_steps": [
                            "Perencanaan",
                            "Implementasi",
                            "Refleksi"
                        ]
                    }
                ],
                "remedial": [
                    {
                        "title": "Kasus Nyata",
                        "description": "Studi kasus {tp_text}",
                        "duration": "20 menit",
                        "grouping": "diskusi",
                        "materials": ["kasus"],
                        "base_steps": [
                            "Presentasi kasus",
                            "Diskusi",
                            "Refleksi"
                        ]
                    }
                ],
                "p5": [
                    {
                        "title": "Proyek Sosial",
                        "description": "Proyek sosial {tp_text}",
                        "duration": "2-3 minggu",
                        "grouping": "kelompok",
                        "materials": ["bahan proyek"],
                        "base_steps": [
                            "Perencanaan",
                            "Implementasi",
                            "Presentasi"
                        ]
                    }
                ]
            }
        }
