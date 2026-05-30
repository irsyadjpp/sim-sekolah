"""
Parent Communication Portal

This module provides a comprehensive parent communication portal including
parent dashboard, communication features, and reporting system.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict


class CommunicationType(str, Enum):
    """Types of communication"""
    ANNOUNCEMENT = "announcement"
    DIRECT_MESSAGE = "direct_message"
    PROGRESS_UPDATE = "progress_update"
    ALERT = "alert"
    EVENT_INVITATION = "event_invitation"


class ReportType(str, Enum):
    """Types of reports"""
    ACADEMIC_PROGRESS = "academic_progress"
    CHARACTER_DEVELOPMENT = "character_development"
    ATTENDANCE = "attendance"
    ASSESSMENT_RESULTS = "assessment_results"
    BEHAVIOR = "behavior"


class ParentCommunicationPortal:
    """Comprehensive parent communication portal"""
    
    def __init__(self):
        self.parent_accounts: Dict[str, Dict] = {}
        self.student_parent_mapping: Dict[str, str] = {}  # student_id -> parent_id
        self.communications: Dict[str, List[Dict]] = defaultdict(list)
        self.reports: Dict[str, List[Dict]] = defaultdict(list)
        self.parent_teacher_meetings: Dict[str, List[Dict]] = defaultdict(list)
    
    def get_parent_dashboard(self, parent_id: str) -> Dict:
        """Get comprehensive parent dashboard"""
        parent_data = self.parent_accounts.get(parent_id, {})
        student_ids = self._get_student_ids_for_parent(parent_id)
        
        dashboard = {
            "parent_id": parent_id,
            "parent_name": parent_data.get("name", ""),
            "last_updated": datetime.utcnow().isoformat(),
            "children": [
                self._get_child_summary(student_id) 
                for student_id in student_ids
            ],
            "recent_communications": self._get_recent_communications(parent_id),
            "upcoming_events": self._get_upcoming_events(parent_id),
            "pending_actions": self._get_pending_actions(parent_id),
            "quick_links": self._get_quick_links(parent_id)
        }
        
        return dashboard
    
    def _get_child_summary(self, student_id: str) -> Dict:
        """Get summary of child's status"""
        return {
            "student_id": student_id,
            "name": f"Student {student_id}",
            "grade": "5",
            "overall_progress": 0.78,
            "recent_achievements": [
                "Completed math unit assessment",
                "5-day reflection streak"
            ],
            "areas_of_concern": [
                "Needs support in science transfer skills"
            ],
            "next_parent_teacher_meeting": "2026-06-15"
        }
    
    def _get_student_ids_for_parent(self, parent_id: str) -> List[str]:
        """Get list of student IDs for a parent"""
        return [
            student_id for student_id, pid in self.student_parent_mapping.items()
            if pid == parent_id
        ]
    
    def _get_recent_communications(self, parent_id: str) -> List[Dict]:
        """Get recent communications for parent"""
        communications = self.communications.get(parent_id, [])
        return [
            {
                "id": comm["id"],
                "type": comm["type"],
                "from": comm["from"],
                "subject": comm["subject"],
                "date": comm["created_at"],
                "read": comm.get("read", False)
            }
            for comm in communications[-5:]
        ]
    
    def _get_upcoming_events(self, parent_id: str) -> List[Dict]:
        """Get upcoming events for parent"""
        return [
            {
                "event_id": "event_1",
                "title": "Parent-Teacher Conference",
                "date": "2026-06-15",
                "time": "14:00",
                "location": "School Hall"
            },
            {
                "event_id": "event_2",
                "title": "School Performance",
                "date": "2026-06-20",
                "time": "10:00",
                "location": "Auditorium"
            }
        ]
    
    def _get_pending_actions(self, parent_id: str) -> List[Dict]:
        """Get pending actions for parent"""
        return [
            {
                "action": "Review student progress report",
                "deadline": "2026-06-10",
                "priority": "high"
            },
            {
                "action": "Confirm attendance for parent-teacher meeting",
                "deadline": "2026-06-12",
                "priority": "medium"
            }
        ]
    
    def _get_quick_links(self, parent_id: str) -> List[Dict]:
        """Get quick links for parent dashboard"""
        return [
            {
                "title": "View Student Progress",
                "url": "/progress",
                "icon": "chart"
            },
            {
                "title": "Communicate with Teacher",
                "url": "/messages",
                "icon": "message"
            },
            {
                "title": "View Reports",
                "url": "/reports",
                "icon": "document"
            },
            {
                "title": "Schedule Meeting",
                "url": "/meetings",
                "icon": "calendar"
            }
        ]
    
    def send_communication(
        self,
        from_id: str,
        to_parent_id: str,
        communication_type: CommunicationType,
        subject: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Send communication to parent"""
        communication = {
            "id": f"comm_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "from": from_id,
            "to": to_parent_id,
            "type": communication_type.value,
            "subject": subject,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "read": False
        }
        
        self.communications[to_parent_id].append(communication)
        
        return {
            "communication_id": communication["id"],
            "status": "sent",
            "sent_at": communication["created_at"]
        }
    
    def get_communications(
        self,
        parent_id: str,
        communication_type: Optional[CommunicationType] = None,
        unread_only: bool = False
    ) -> List[Dict]:
        """Get communications for parent with filtering"""
        communications = self.communications.get(parent_id, [])
        
        if communication_type:
            communications = [c for c in communications if c["type"] == communication_type.value]
        
        if unread_only:
            communications = [c for c in communications if not c.get("read", False)]
        
        return communications
    
    def mark_communication_read(self, parent_id: str, communication_id: str) -> Dict:
        """Mark communication as read"""
        communications = self.communications.get(parent_id, [])
        
        for comm in communications:
            if comm["id"] == communication_id:
                comm["read"] = True
                comm["read_at"] = datetime.utcnow().isoformat()
                return {"status": "marked_read", "communication_id": communication_id}
        
        return {"error": "Communication not found"}
    
    def send_direct_message(
        self,
        from_id: str,
        to_parent_id: str,
        student_id: str,
        message: str
    ) -> Dict:
        """Send direct message to parent about student"""
        return self.send_communication(
            from_id=from_id,
            to_parent_id=to_parent_id,
            communication_type=CommunicationType.DIRECT_MESSAGE,
            subject=f"Message about {student_id}",
            content=message,
            metadata={"student_id": student_id}
        )
    
    def send_progress_update(
        self,
        from_id: str,
        to_parent_id: str,
        student_id: str,
        progress_data: Dict
    ) -> Dict:
        """Send progress update to parent"""
        content = self._format_progress_update(progress_data)
        
        return self.send_communication(
            from_id=from_id,
            to_parent_id=to_parent_id,
            communication_type=CommunicationType.PROGRESS_UPDATE,
            subject=f"Progress Update for {student_id}",
            content=content,
            metadata={"student_id": student_id, "progress_data": progress_data}
        )
    
    def send_alert(
        self,
        from_id: str,
        to_parent_id: str,
        student_id: str,
        alert_type: str,
        message: str,
        priority: str = "medium"
    ) -> Dict:
        """Send alert to parent"""
        return self.send_communication(
            from_id=from_id,
            to_parent_id=to_parent_id,
            communication_type=CommunicationType.ALERT,
            subject=f"Alert: {alert_type}",
            content=message,
            metadata={
                "student_id": student_id,
                "alert_type": alert_type,
                "priority": priority
            }
        )
    
    def generate_report(
        self,
        parent_id: str,
        student_id: str,
        report_type: ReportType,
        date_range: Optional[Dict] = None
    ) -> Dict:
        """Generate report for parent"""
        report = {
            "report_id": f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "parent_id": parent_id,
            "student_id": student_id,
            "report_type": report_type.value,
            "generated_at": datetime.utcnow().isoformat(),
            "date_range": date_range or self._get_default_date_range(),
            "data": self._get_report_data(student_id, report_type),
            "summary": self._generate_report_summary(student_id, report_type),
            "recommendations": self._generate_report_recommendations(student_id, report_type)
        }
        
        self.reports[parent_id].append(report)
        
        return report
    
    def get_reports(
        self,
        parent_id: str,
        student_id: Optional[str] = None,
        report_type: Optional[ReportType] = None
    ) -> List[Dict]:
        """Get reports for parent with filtering"""
        reports = self.reports.get(parent_id, [])
        
        if student_id:
            reports = [r for r in reports if r["student_id"] == student_id]
        
        if report_type:
            reports = [r for r in reports if r["report_type"] == report_type.value]
        
        return reports
    
    def schedule_parent_teacher_meeting(
        self,
        parent_id: str,
        teacher_id: str,
        student_id: str,
        date: str,
        time: str,
        agenda: Optional[List[str]] = None
    ) -> Dict:
        """Schedule parent-teacher meeting"""
        meeting = {
            "meeting_id": f"meeting_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "parent_id": parent_id,
            "teacher_id": teacher_id,
            "student_id": student_id,
            "date": date,
            "time": time,
            "agenda": agenda or [],
            "status": "scheduled",
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.parent_teacher_meetings[parent_id].append(meeting)
        
        # Send notification to parent
        self.send_communication(
            from_id=teacher_id,
            to_parent_id=parent_id,
            communication_type=CommunicationType.EVENT_INVITATION,
            subject="Parent-Teacher Meeting Scheduled",
            content=f"Meeting scheduled for {date} at {time}",
            metadata={"meeting_id": meeting["meeting_id"], "student_id": student_id}
        )
        
        return meeting
    
    def get_parent_teacher_meetings(
        self,
        parent_id: str,
        status: Optional[str] = None
    ) -> List[Dict]:
        """Get parent-teacher meetings with filtering"""
        meetings = self.parent_teacher_meetings.get(parent_id, [])
        
        if status:
            meetings = [m for m in meetings if m["status"] == status]
        
        return meetings
    
    def get_academic_progress_report(
        self,
        parent_id: str,
        student_id: str
    ) -> Dict:
        """Get detailed academic progress report"""
        return self.generate_report(
            parent_id=parent_id,
            student_id=student_id,
            report_type=ReportType.ACADEMIC_PROGRESS
        )
    
    def get_character_development_report(
        self,
        parent_id: str,
        student_id: str
    ) -> Dict:
        """Get character development report"""
        return self.generate_report(
            parent_id=parent_id,
            student_id=student_id,
            report_type=ReportType.CHARACTER_DEVELOPMENT
        )
    
    def get_attendance_report(
        self,
        parent_id: str,
        student_id: str,
        date_range: Optional[Dict] = None
    ) -> Dict:
        """Get attendance report"""
        return self.generate_report(
            parent_id=parent_id,
            student_id=student_id,
            report_type=ReportType.ATTENDANCE,
            date_range=date_range
        )
    
    def get_assessment_results_report(
        self,
        parent_id: str,
        student_id: str,
        date_range: Optional[Dict] = None
    ) -> Dict:
        """Get assessment results report"""
        return self.generate_report(
            parent_id=parent_id,
            student_id=student_id,
            report_type=ReportType.ASSESSMENT_RESULTS,
            date_range=date_range
        )
    
    def _format_progress_update(self, progress_data: Dict) -> str:
        """Format progress update for communication"""
        overall = progress_data.get("overall_progress", 0)
        subjects = progress_data.get("subjects", {})
        
        content = f"Overall Progress: {overall:.1%}\n\n"
        content += "Subject Progress:\n"
        
        for subject, data in subjects.items():
            content += f"- {subject}: {data.get('progress', 0):.1%}\n"
        
        return content
    
    def _get_default_date_range(self) -> Dict:
        """Get default date range for reports"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        return {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        }
    
    def _get_report_data(self, student_id: str, report_type: ReportType) -> Dict:
        """Get data for specific report type"""
        if report_type == ReportType.ACADEMIC_PROGRESS:
            return self._get_academic_progress_data(student_id)
        elif report_type == ReportType.CHARACTER_DEVELOPMENT:
            return self._get_character_development_data(student_id)
        elif report_type == ReportType.ATTENDANCE:
            return self._get_attendance_data(student_id)
        elif report_type == ReportType.ASSESSMENT_RESULTS:
            return self._get_assessment_results_data(student_id)
        elif report_type == ReportType.BEHAVIOR:
            return self._get_behavior_data(student_id)
        else:
            return {}
    
    def _get_academic_progress_data(self, student_id: str) -> Dict:
        """Get academic progress data"""
        return {
            "overall_progress": 0.78,
            "subjects": {
                "matematika": {"progress": 0.75, "grade": "B+"},
                "bahasa_indonesia": {"progress": 0.88, "grade": "A"},
                "ipa": {"progress": 0.72, "grade": "B"},
                "ips": {"progress": 0.65, "grade": "B-"}
            },
            "learning_objectives": {
                "completed": 45,
                "in_progress": 12,
                "not_started": 5
            },
            "strengths": ["language arts", "creative writing"],
            "areas_for_improvement": ["science transfer skills", "math problem solving"]
        }
    
    def _get_character_development_data(self, student_id: str) -> Dict:
        """Get character development data"""
        return {
            "profil_pelajar_pancasila": {
                "beriman": {"score": 0.85, "growth": "+0.10"},
                "berkebinekaan_global": {"score": 0.80, "growth": "+0.15"},
                "gotong_royong": {"score": 0.75, "growth": "+0.05"},
                "kreatif": {"score": 0.90, "growth": "+0.20"},
                "mandiri": {"score": 0.82, "growth": "+0.12"},
                "bernalir_kritis": {"score": 0.78, "growth": "+0.08"}
            },
            "character_strengths": ["kreatif", "beriman"],
            "character_goals": [
                "Improve collaboration skills",
                "Strengthen critical thinking"
            ],
            "evidence": [
                "Helped peer with group project",
                "Created innovative solution"
            ]
        }
    
    def _get_attendance_data(self, student_id: str) -> Dict:
        """Get attendance data"""
        return {
            "total_days": 100,
            "present": 95,
            "absent": 3,
            "late": 2,
            "attendance_rate": 0.95,
            "monthly_breakdown": [
                {"month": "January", "present": 20, "absent": 0, "late": 0},
                {"month": "February", "present": 18, "absent": 1, "late": 1},
                {"month": "March", "present": 19, "absent": 1, "late": 0},
                {"month": "April", "present": 20, "absent": 0, "late": 0},
                {"month": "May", "present": 18, "absent": 1, "late": 1}
            ]
        }
    
    def _get_assessment_results_data(self, student_id: str) -> Dict:
        """Get assessment results data"""
        return {
            "total_assessments": 15,
            "average_score": 82.5,
            "grade_distribution": {
                "A": 5,
                "B": 7,
                "C": 2,
                "D": 1
            },
            "recent_assessments": [
                {
                    "assessment": "Math Unit 3 Test",
                    "date": "2026-05-25",
                    "score": 85,
                    "grade": "B+"
                },
                {
                    "assessment": "Language Arts Essay",
                    "date": "2026-05-20",
                    "score": 92,
                    "grade": "A-"
                },
                {
                    "assessment": "Science Project",
                    "date": "2026-05-15",
                    "score": 78,
                    "grade": "B"
                }
            ],
            "strengths": ["written assessments", "creative projects"],
            "areas_for_improvement": ["problem-solving tests", "time management"]
        }
    
    def _get_behavior_data(self, student_id: str) -> Dict:
        """Get behavior data"""
        return {
            "overall_behavior_rating": "excellent",
            "positive_behaviors": [
                "Helps classmates",
                "Participates actively",
                "Shows respect"
            ],
            "areas_for_growth": [
                "Needs to improve focus during long activities"
            ],
            "teacher_comments": [
                "Student is respectful and helpful to peers",
                "Shows great enthusiasm for learning",
                "Could benefit from more structured activities"
            ]
        }
    
    def _generate_report_summary(self, student_id: str, report_type: ReportType) -> str:
        """Generate summary for report"""
        summaries = {
            ReportType.ACADEMIC_PROGRESS: "Student is making good progress overall, with strength in language arts and areas for improvement in science transfer skills.",
            ReportType.CHARACTER_DEVELOPMENT: "Student demonstrates strong character development, particularly in creativity and faith dimensions. Continued focus on collaboration is recommended.",
            ReportType.ATTENDANCE: "Student has excellent attendance at 95%, with only 3 absences this semester.",
            ReportType.ASSESSMENT_RESULTS: "Student performs well on assessments with an average score of 82.5%. Strength in written assessments, room for improvement in problem-solving.",
            ReportType.BEHAVIOR: "Student demonstrates excellent behavior overall, with positive interactions with peers and teachers."
        }
        
        return summaries.get(report_type, "Report generated successfully.")
    
    def _generate_report_recommendations(self, student_id: str, report_type: ReportType) -> List[str]:
        """Generate recommendations based on report"""
        recommendations = {
            ReportType.ACADEMIC_PROGRESS: [
                "Provide additional support for science transfer skills",
                "Encourage practice with math problem-solving",
                "Continue supporting language arts strengths"
            ],
            ReportType.CHARACTER_DEVELOPMENT: [
                "Encourage participation in group activities",
                "Provide opportunities for collaborative projects",
                "Continue supporting creative expression"
            ],
            ReportType.ATTENDANCE: [
                "Maintain current excellent attendance",
                "Address any patterns in absences if they emerge"
            ],
            ReportType.ASSESSMENT_RESULTS: [
                "Practice problem-solving strategies",
                "Work on time management during tests",
                "Continue leveraging writing strengths"
            ],
            ReportType.BEHAVIOR: [
                "Continue positive reinforcement",
                "Provide structured activities to improve focus"
            ]
        }
        
        return recommendations.get(report_type, [])
