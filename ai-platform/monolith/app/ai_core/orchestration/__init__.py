"""
Orchestration Engine Module

This module provides orchestration capabilities for:
- Agent orchestration for multi-agent coordination
- Tool orchestration for AI tool selection and execution
- Workflow orchestration for end-to-end workflow management
"""

from .agent_orchestrator import AgentOrchestrator
from .tool_orchestrator import ToolOrchestrator
from .workflow_orchestrator import WorkflowOrchestrator

__all__ = [
    "OrchestrationEngine",
    "AgentOrchestrator",
    "ToolOrchestrator",
    "WorkflowOrchestrator"
]

class OrchestrationEngine:
    """Main class for orchestration management"""
    
    def __init__(self):
        self.agent_orchestrator = AgentOrchestrator()
        self.tool_orchestrator = ToolOrchestrator()
        self.workflow_orchestrator = WorkflowOrchestrator()
    
    def orchestrate_agents(self, task: str, agents: list, context: dict) -> dict:
        """Orchestrate multiple agents for a task"""
        return self.agent_orchestrator.orchestrate(task, agents, context)
    
    def orchestrate_tools(self, task: str, available_tools: list, context: dict) -> dict:
        """Orchestrate tool selection and execution"""
        return self.tool_orchestrator.orchestrate(task, available_tools, context)
    
    def orchestrate_workflow(self, workflow_name: str, steps: list, context: dict) -> dict:
        """Orchestrate workflow execution"""
        return self.workflow_orchestrator.orchestrate(workflow_name, steps, context)