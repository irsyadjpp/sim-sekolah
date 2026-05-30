"""
Workflow Analytics Service

This module provides workflow analytics including completion rates, time tracking,
bottleneck identification, and success metrics.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
import json
from pathlib import Path


class MetricType(str, Enum):
    """Types of workflow metrics"""
    COMPLETION_RATE = "completion_rate"
    AVERAGE_TIME = "average_time"
    BOTTLENECK_FREQUENCY = "bottleneck_frequency"
    SUCCESS_SCORE = "success_score"
    USER_SATISFACTION = "user_satisfaction"


class WorkflowAnalyticsService:
    """Analytics service for teacher workflows"""
    
    def __init__(self, analytics_dir: str = "/tmp/workflow_analytics"):
        self.analytics_dir = Path(analytics_dir)
        self.analytics_dir.mkdir(parents=True, exist_ok=True)
        
        self.workflow_data: Dict[str, List[Dict]] = defaultdict(list)
        self._load_historical_data()
    
    def record_workflow_completion(
        self, 
        workflow_type: str, 
        session_data: Dict,
        user_id: Optional[str] = None
    ):
        """Record workflow completion data"""
        completion_record = {
            "workflow_type": workflow_type,
            "user_id": user_id,
            "session_id": session_data.get("session_id"),
            "started_at": session_data.get("started_at"),
            "completed_at": session_data.get("completed_at"),
            "duration_minutes": self._calculate_duration(session_data),
            "progress": session_data.get("workflow_state", {}).get("progress", 0),
            "success": session_data.get("final_result", {}).get("success", False),
            "steps_completed": self._count_completed_steps(session_data),
            "bottlenecks": session_data.get("bottlenecks", []),
            "user_satisfaction": session_data.get("user_satisfaction", None)
        }
        
        self.workflow_data[workflow_type].append(completion_record)
        self._save_workflow_data(workflow_type)
    
    def get_completion_rates(
        self, 
        workflow_type: Optional[str] = None,
        time_period: Optional[str] = None
    ) -> Dict:
        """Get workflow completion rates"""
        if workflow_type:
            data = self.workflow_data.get(workflow_type, [])
        else:
            data = []
            for wf_data in self.workflow_data.values():
                data.extend(wf_data)
        
        # Filter by time period if specified
        if time_period:
            data = self._filter_by_time_period(data, time_period)
        
        total = len(data)
        completed = sum(1 for record in data if record.get("success", False))
        
        completion_rate = completed / total if total > 0 else 0
        
        return {
            "workflow_type": workflow_type or "all",
            "time_period": time_period or "all_time",
            "total_workflows": total,
            "completed_workflows": completed,
            "completion_rate": completion_rate,
            "target_rate": 0.80,  # From success criteria
            "meets_target": completion_rate >= 0.80
        }
    
    def get_time_tracking_metrics(
        self, 
        workflow_type: Optional[str] = None
    ) -> Dict:
        """Get time tracking metrics"""
        if workflow_type:
            data = self.workflow_data.get(workflow_type, [])
        else:
            data = []
            for wf_data in self.workflow_data.values():
                data.extend(wf_data)
        
        if not data:
            return {"error": "No data available"}
        
        durations = [record.get("duration_minutes", 0) for record in data]
        
        return {
            "workflow_type": workflow_type or "all",
            "average_duration": sum(durations) / len(durations),
            "median_duration": sorted(durations)[len(durations) // 2],
            "min_duration": min(durations),
            "max_duration": max(durations),
            "target_duration": self._get_target_duration(workflow_type),
            "meets_target": (sum(durations) / len(durations)) <= self._get_target_duration(workflow_type),
            "time_distribution": self._get_time_distribution(durations)
        }
    
    def identify_bottlenecks(
        self, 
        workflow_type: Optional[str] = None
    ) -> Dict:
        """Identify workflow bottlenecks"""
        if workflow_type:
            data = self.workflow_data.get(workflow_type, [])
        else:
            data = []
            for wf_data in self.workflow_data.values():
                data.extend(wf_data)
        
        bottleneck_counts = defaultdict(int)
        bottleneck_durations = defaultdict(list)
        
        for record in data:
            for bottleneck in record.get("bottlenecks", []):
                bottleneck_counts[bottleneck] += 1
                bottleneck_durations[bottleneck].append(record.get("duration_minutes", 0))
        
        # Calculate bottleneck statistics
        bottleneck_stats = []
        for bottleneck, count in bottleneck_counts.items():
            avg_duration = sum(bottleneck_durations[bottleneck]) / len(bottleneck_durations[bottleneck])
            bottleneck_stats.append({
                "bottleneck": bottleneck,
                "frequency": count / len(data),
                "average_delay": avg_duration,
                "severity": self._assess_bottleneck_severity(count / len(data), avg_duration)
            })
        
        # Sort by severity
        bottleneck_stats.sort(key=lambda x: x["severity"], reverse=True)
        
        return {
            "workflow_type": workflow_type or "all",
            "total_bottlenecks_identified": len(bottleneck_stats),
            "bottlenecks": bottleneck_stats[:5],  # Top 5 bottlenecks
            "recommendations": self._generate_bottleneck_recommendations(bottleneck_stats)
        }
    
    def get_success_metrics(
        self, 
        workflow_type: Optional[str] = None
    ) -> Dict:
        """Get overall success metrics"""
        if workflow_type:
            data = self.workflow_data.get(workflow_type, [])
        else:
            data = []
            for wf_data in self.workflow_data.values():
                data.extend(wf_data)
        
        if not data:
            return {"error": "No data available"}
        
        completion_rate = sum(1 for r in data if r.get("success", False)) / len(data)
        avg_duration = sum(r.get("duration_minutes", 0) for r in data) / len(data)
        avg_satisfaction = sum(
            r.get("user_satisfaction", 0) for r in data 
            if r.get("user_satisfaction") is not None
        ) / len([r for r in data if r.get("user_satisfaction") is not None])
        
        return {
            "workflow_type": workflow_type or "all",
            "completion_rate": completion_rate,
            "average_duration": avg_duration,
            "user_satisfaction": avg_satisfaction,
            "overall_success_score": (completion_rate * 0.4 + 
                                    (1 - avg_duration / self._get_target_duration(workflow_type)) * 0.3 +
                                    avg_satisfaction / 5 * 0.3),
            "targets_met": {
                "completion_rate": completion_rate >= 0.80,
                "time": avg_duration <= self._get_target_duration(workflow_type),
                "satisfaction": avg_satisfaction >= 4.0
            }
        }
    
    def get_user_analytics(self, user_id: str) -> Dict:
        """Get analytics for a specific user"""
        user_data = []
        for wf_type, records in self.workflow_data.items():
            user_data.extend([r for r in records if r.get("user_id") == user_id])
        
        if not user_data:
            return {"error": "No data for user"}
        
        workflow_counts = defaultdict(int)
        for record in user_data:
            workflow_counts[record["workflow_type"]] += 1
        
        return {
            "user_id": user_id,
            "total_workflows": len(user_data),
            "workflow_breakdown": dict(workflow_counts),
            "average_completion_rate": sum(1 for r in user_data if r.get("success", False)) / len(user_data),
            "average_duration": sum(r.get("duration_minutes", 0) for r in user_data) / len(user_data),
            "most_used_workflow": max(workflow_counts, key=workflow_counts.get),
            "improvement_trend": self._calculate_improvement_trend(user_data)
        }
    
    def generate_analytics_report(
        self, 
        workflow_type: Optional[str] = None,
        time_period: Optional[str] = None
    ) -> Dict:
        """Generate comprehensive analytics report"""
        return {
            "completion_rates": self.get_completion_rates(workflow_type, time_period),
            "time_tracking": self.get_time_tracking_metrics(workflow_type),
            "bottlenecks": self.identify_bottlenecks(workflow_type),
            "success_metrics": self.get_success_metrics(workflow_type),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _calculate_duration(self, session_data: Dict) -> float:
        """Calculate workflow duration in minutes"""
        if "started_at" not in session_data or "completed_at" not in session_data:
            return 0.0
        
        start = datetime.fromisoformat(session_data["started_at"])
        end = datetime.fromisoformat(session_data["completed_at"])
        duration = (end - start).total_seconds() / 60
        
        return duration
    
    def _count_completed_steps(self, session_data: Dict) -> int:
        """Count number of completed steps in workflow"""
        workflow_state = session_data.get("workflow_state", {})
        return sum(1 for key, value in workflow_state.items() if isinstance(value, dict))
    
    def _filter_by_time_period(self, data: List[Dict], time_period: str) -> List[Dict]:
        """Filter data by time period"""
        now = datetime.utcnow()
        
        if time_period == "last_7_days":
            cutoff = now - timedelta(days=7)
        elif time_period == "last_30_days":
            cutoff = now - timedelta(days=30)
        elif time_period == "last_90_days":
            cutoff = now - timedelta(days=90)
        else:
            return data
        
        return [
            record for record in data 
            if datetime.fromisoformat(record.get("started_at", "")) >= cutoff
        ]
    
    def _get_target_duration(self, workflow_type: Optional[str]) -> float:
        """Get target duration for workflow"""
        target_durations = {
            "modul_ajar": 30,
            "cp_atp": 15,
            "assessment": 20,
            "remediation": 25
        }
        return target_durations.get(workflow_type, 30)
    
    def _get_time_distribution(self, durations: List[float]) -> Dict:
        """Get distribution of completion times"""
        if not durations:
            return {}
        
        sorted_durations = sorted(durations)
        n = len(sorted_durations)
        
        return {
            "p25": sorted_durations[int(n * 0.25)],
            "p50": sorted_durations[int(n * 0.50)],
            "p75": sorted_durations[int(n * 0.75)],
            "p90": sorted_durations[int(n * 0.90)]
        }
    
    def _assess_bottleneck_severity(self, frequency: float, avg_delay: float) -> str:
        """Assess severity of bottleneck"""
        if frequency > 0.5 and avg_delay > 10:
            return "critical"
        elif frequency > 0.3 and avg_delay > 5:
            return "high"
        elif frequency > 0.2:
            return "medium"
        else:
            return "low"
    
    def _generate_bottleneck_recommendations(self, bottleneck_stats: List[Dict]) -> List[str]:
        """Generate recommendations for addressing bottlenecks"""
        recommendations = []
        
        for bottleneck in bottleneck_stats[:3]:  # Top 3
            severity = bottleneck["severity"]
            name = bottleneck["bottleneck"]
            
            if severity == "critical":
                recommendations.append(
                    f"URGENT: Address {name} bottleneck - affects {bottleneck['frequency']:.1%} of workflows"
                )
            elif severity == "high":
                recommendations.append(
                    f"Priority: Optimize {name} step to reduce delays"
                )
            else:
                recommendations.append(
                    f"Consider improvements for {name} step"
                )
        
        return recommendations
    
    def _calculate_improvement_trend(self, user_data: List[Dict]) -> str:
        """Calculate user's improvement trend over time"""
        if len(user_data) < 3:
            return "insufficient_data"
        
        # Sort by completion time
        sorted_data = sorted(user_data, key=lambda x: x.get("completed_at", ""))
        
        # Compare first third vs last third
        n = len(sorted_data)
        first_third = sorted_data[:n//3]
        last_third = sorted_data[-n//3:]
        
        first_avg_duration = sum(r.get("duration_minutes", 0) for r in first_third) / len(first_third)
        last_avg_duration = sum(r.get("duration_minutes", 0) for r in last_third) / len(last_third)
        
        if last_avg_duration < first_avg_duration * 0.9:
            return "improving"
        elif last_avg_duration > first_avg_duration * 1.1:
            return "declining"
        else:
            return "stable"
    
    def _load_historical_data(self):
        """Load historical analytics data from disk"""
        for workflow_file in self.analytics_dir.glob("*.json"):
            workflow_type = workflow_file.stem
            try:
                with open(workflow_file, 'r') as f:
                    self.workflow_data[workflow_type] = json.load(f)
            except:
                self.workflow_data[workflow_type] = []
    
    def _save_workflow_data(self, workflow_type: str):
        """Save workflow data to disk"""
        data_file = self.analytics_dir / f"{workflow_type}.json"
        with open(data_file, 'w') as f:
            json.dump(self.workflow_data[workflow_type], f, indent=2)
