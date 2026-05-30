"""
Unified Workflow Orchestrator

This module provides unified workflow management across all teacher workflows with:
- Cross-workflow integration
- Progress tracking across workflows
- Save/resume capabilities
- Workflow state persistence
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
from pathlib import Path

from .modul_ajar_workflow import ModulAjarWorkflow
from .cp_atp_workflow import CPATPWorkflow
from .assessment_workflow import AssessmentWorkflow
from .remediation_workflow import RemediationWorkflow


class WorkflowStatus(str, Enum):
    """Workflow status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowType(str, Enum):
    """Workflow type enumeration"""
    MODUL_AJAR = "modul_ajar"
    CP_ATP = "cp_atp"
    ASSESSMENT = "assessment"
    REMEDIATION = "remediation"


class WorkflowOrchestrator:
    """Unified orchestrator for all teacher workflows with cross-workflow integration"""
    
    def __init__(self, state_dir: str = "/tmp/workflow_states"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        self.workflows = {
            WorkflowType.MODUL_AJAR: ModulAjarWorkflow(),
            WorkflowType.CP_ATP: CPATPWorkflow(),
            WorkflowType.ASSESSMENT: AssessmentWorkflow(),
            WorkflowType.REMEDIATION: RemediationWorkflow()
        }
        
        self.active_sessions: Dict[str, Dict] = {}
        self.workflow_history: List[Dict] = []
    
    def start_workflow(
        self, 
        workflow_type: WorkflowType, 
        context: Dict,
        session_id: Optional[str] = None
    ) -> Dict:
        """Start a workflow with session management"""
        if session_id and session_id in self.active_sessions:
            return self.resume_workflow(session_id)
        
        workflow = self.workflows[workflow_type]
        result = workflow.start(context)
        
        session_id = session_id or f"{workflow_type.value}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        session = {
            "session_id": session_id,
            "workflow_type": workflow_type.value,
            "status": WorkflowStatus.IN_PROGRESS.value,
            "started_at": datetime.utcnow().isoformat(),
            "context": context,
            "workflow_state": workflow.workflow_state,
            "cross_workflow_data": {}
        }
        
        self.active_sessions[session_id] = session
        self._save_session_state(session_id)
        
        return {
            "session_id": session_id,
            "workflow_type": workflow_type.value,
            "status": session["status"],
            "workflow_result": result,
            "can_pause": True,
            "can_resume": True
        }
    
    def proceed_workflow(
        self, 
        session_id: str, 
        step_data: Dict
    ) -> Dict:
        """Proceed to next step in workflow"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        workflow_type = WorkflowType(session["workflow_type"])
        workflow = self.workflows[workflow_type]
        
        result = workflow.proceed_to_next_step(step_data)
        
        # Update session state
        session["workflow_state"] = workflow.workflow_state
        session["last_updated"] = datetime.utcnow().isoformat()
        
        # Check for cross-workflow integration opportunities
        cross_workflow_suggestions = self._check_cross_workflow_integration(
            workflow_type, 
            workflow.workflow_state
        )
        
        self._save_session_state(session_id)
        
        return {
            "session_id": session_id,
            "workflow_result": result,
            "cross_workflow_suggestions": cross_workflow_suggestions,
            "progress": session["workflow_state"].get("progress", 0)
        }
    
    def pause_workflow(self, session_id: str) -> Dict:
        """Pause a workflow for later resumption"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        session["status"] = WorkflowStatus.PAUSED.value
        session["paused_at"] = datetime.utcnow().isoformat()
        
        self._save_session_state(session_id)
        
        return {
            "session_id": session_id,
            "status": session["status"],
            "paused_at": session["paused_at"],
            "can_resume": True
        }
    
    def resume_workflow(self, session_id: str) -> Dict:
        """Resume a paused workflow"""
        # Try to load from disk if not in memory
        if session_id not in self.active_sessions:
            session = self._load_session_state(session_id)
            if not session:
                return {"error": "Session not found"}
            self.active_sessions[session_id] = session
        
        session = self.active_sessions[session_id]
        workflow_type = WorkflowType(session["workflow_type"])
        workflow = self.workflows[workflow_type]
        
        # Restore workflow state
        workflow.workflow_state = session["workflow_state"]
        workflow.current_step = session["workflow_state"].get("current_step")
        
        session["status"] = WorkflowStatus.IN_PROGRESS.value
        session["resumed_at"] = datetime.utcnow().isoformat()
        
        self._save_session_state(session_id)
        
        return {
            "session_id": session_id,
            "workflow_type": workflow_type.value,
            "status": session["status"],
            "resumed_at": session["resumed_at"],
            "current_step": workflow.current_step,
            "progress": session["workflow_state"].get("progress", 0)
        }
    
    def complete_workflow(self, session_id: str) -> Dict:
        """Complete a workflow"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        workflow_type = WorkflowType(session["workflow_type"])
        workflow = self.workflows[workflow_type]
        
        result = workflow.complete_workflow()
        
        session["status"] = WorkflowStatus.COMPLETED.value
        session["completed_at"] = datetime.utcnow().isoformat()
        session["final_result"] = result
        
        # Add to history
        self.workflow_history.append(session.copy())
        
        self._save_session_state(session_id)
        
        # Suggest next workflows
        next_workflow_suggestions = self._suggest_next_workflows(
            workflow_type, 
            result
        )
        
        return {
            "session_id": session_id,
            "workflow_type": workflow_type.value,
            "status": session["status"],
            "completed_at": session["completed_at"],
            "result": result,
            "next_workflow_suggestions": next_workflow_suggestions
        }
    
    def get_all_active_sessions(self) -> List[Dict]:
        """Get all active workflow sessions"""
        return [
            {
                "session_id": session_id,
                "workflow_type": session["workflow_type"],
                "status": session["status"],
                "started_at": session["started_at"],
                "progress": session["workflow_state"].get("progress", 0)
            }
            for session_id, session in self.active_sessions.items()
        ]
    
    def get_session_progress(self, session_id: str) -> Dict:
        """Get detailed progress for a session"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        workflow_type = WorkflowType(session["workflow_type"])
        workflow = self.workflows[workflow_type]
        
        return {
            "session_id": session_id,
            "workflow_type": workflow_type.value,
            "status": session["status"],
            "current_step": workflow.current_step,
            "progress": session["workflow_state"].get("progress", 0),
            "workflow_definition": workflow.get_workflow_definition(),
            "time_elapsed": self._calculate_time_elapsed(session),
            "estimated_remaining": self._estimate_remaining_time(session)
        }
    
    def _check_cross_workflow_integration(
        self, 
        workflow_type: WorkflowType, 
        workflow_state: Dict
    ) -> List[Dict]:
        """Check for cross-workflow integration opportunities"""
        suggestions = []
        
        # Modul Ajar → Assessment integration
        if workflow_type == WorkflowType.MODUL_AJAR:
            if "define_learning_objectives" in workflow_state:
                suggestions.append({
                    "target_workflow": WorkflowType.ASSESSMENT.value,
                    "reason": "Learning objectives defined in Modul Ajar can be used for assessment creation",
                    "action": "Create assessments aligned with these learning objectives",
                    "data_transfer": {
                        "learning_objectives": workflow_state["define_learning_objectives"]
                    }
                })
        
        # CP → ATP → Modul Ajar integration
        if workflow_type == WorkflowType.CP_ATP:
            if "generate_atp_from_cp" in workflow_state:
                suggestions.append({
                    "target_workflow": WorkflowType.MODUL_AJAR.value,
                    "reason": "ATP topics can inform Modul Ajar activity design",
                    "action": "Use ATP topic sequence to structure Modul Ajar activities",
                    "data_transfer": {
                        "topics": workflow_state.get("topics", [])
                    }
                })
        
        # Assessment → Remediation integration
        if workflow_type == WorkflowType.ASSESSMENT:
            if "create_assessment_tasks" in workflow_state:
                suggestions.append({
                    "target_workflow": WorkflowType.REMEDIATION.value,
                    "reason": "Assessment results can inform remediation planning",
                    "action": "Prepare remediation based on assessment criteria",
                    "data_transfer": {
                        "assessment_tasks": workflow_state["create_assessment_tasks"]
                    }
                })
        
        return suggestions
    
    def _suggest_next_workflows(
        self, 
        completed_workflow: WorkflowType, 
        result: Dict
    ) -> List[Dict]:
        """Suggest next workflows after completion"""
        suggestions = []
        
        workflow_sequences = {
            WorkflowType.CP_ATP: [
                {
                    "workflow": WorkflowType.MODUL_AJAR.value,
                    "reason": "Use ATP to create detailed Modul Ajar",
                    "priority": "high"
                }
            ],
            WorkflowType.MODUL_AJAR: [
                {
                    "workflow": WorkflowType.ASSESSMENT.value,
                    "reason": "Create assessments aligned with Modul Ajar learning objectives",
                    "priority": "high"
                }
            ],
            WorkflowType.ASSESSMENT: [
                {
                    "workflow": WorkflowType.REMEDIATION.value,
                    "reason": "Prepare remediation based on assessment results",
                    "priority": "medium"
                }
            ]
        }
        
        if completed_workflow in workflow_sequences:
            suggestions = workflow_sequences[completed_workflow]
        
        return suggestions
    
    def _save_session_state(self, session_id: str):
        """Save session state to disk"""
        if session_id in self.active_sessions:
            state_file = self.state_dir / f"{session_id}.json"
            with open(state_file, 'w') as f:
                json.dump(self.active_sessions[session_id], f, indent=2)
    
    def _load_session_state(self, session_id: str) -> Optional[Dict]:
        """Load session state from disk"""
        state_file = self.state_dir / f"{session_id}.json"
        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)
        return None
    
    def _calculate_time_elapsed(self, session: Dict) -> str:
        """Calculate time elapsed since session start"""
        if "started_at" not in session:
            return "Unknown"
        
        start = datetime.fromisoformat(session["started_at"])
        now = datetime.utcnow()
        elapsed = now - start
        return str(elapsed)
    
    def _estimate_remaining_time(self, session: Dict) -> str:
        """Estimate remaining time based on progress"""
        progress = session["workflow_state"].get("progress", 0)
        if progress >= 100:
            return "0 minutes"
        
        elapsed = self._calculate_time_elapsed(session)
        if elapsed == "Unknown":
            return "Unknown"
        
        # Simple estimation: if 50% done, same amount remaining
        try:
            elapsed_seconds = sum(
                int(x) * 60 ** i 
                for i, x in enumerate(reversed(elapsed.split(':')[:3]))
            )
            if progress > 0:
                remaining_seconds = elapsed_seconds * ((100 - progress) / progress)
                minutes = int(remaining_seconds / 60)
                return f"{minutes} minutes"
        except:
            pass
        
        return "Unknown"
