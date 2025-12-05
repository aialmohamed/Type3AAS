"""
Report Collector - Collects events during execution and generates summary reports
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
from pathlib import Path
import json
import os


class EventType(Enum):
    SYSTEM_START = "system_start"
    AGENT_STARTED = "agent_started"
    CFP_RECEIVED = "cfp_received"
    CFP_RESPONSE = "cfp_response"
    NEGOTIATION_RESULT = "negotiation_result"
    RESOURCE_SELECTED = "resource_selected"
    RESOURCE_REJECTED = "resource_rejected"
    EXECUTION_STARTED = "execution_started"
    OPERATION_STARTED = "operation_started"
    OPERATION_COMPLETED = "operation_completed"
    AAS_UPDATED = "aas_updated"
    JOB_COMPLETED = "job_completed"
    ERROR = "error"


@dataclass
class Event:
    event_type: EventType
    timestamp: datetime
    source: str
    message: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NegotiationSummary:
    request_skill: str
    request_time_slot: str
    participants: List[str] = field(default_factory=list)
    responses: Dict[str, Dict] = field(default_factory=dict)
    selected_resource: Optional[str] = None
    selection_reason: str = ""


@dataclass 
class ExecutionSummary:
    resource: str
    operations: List[Dict[str, Any]] = field(default_factory=list)
    total_time_seconds: float = 0.0
    status: str = "pending"


class ReportCollector:
    """Singleton report collector that aggregates events across the system"""
    
    _instance = None
    
    # Default report directory - Core/reports/production/
    REPORT_DIR = Path(__file__).parent.parent / "reports" / "production"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.events: List[Event] = []
        self.negotiation: NegotiationSummary = None
        self.execution: ExecutionSummary = None
        self.aas_updates: List[Dict[str, Any]] = []
        self.start_time: datetime = None
        self.end_time: datetime = None
        self.verbose = False
        self.run_id: str = None
        
        # Ensure report directory exists
        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    def reset(self):
        """Reset the collector for a new run"""
        self.events = []
        self.negotiation = None
        self.execution = None
        self.aas_updates = []
        self.start_time = None
        self.end_time = None
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def set_verbose(self, verbose: bool):
        """Enable/disable verbose mode (print events as they happen)"""
        self.verbose = verbose
    
    def set_report_dir(self, path: str):
        """Set custom report directory"""
        self.REPORT_DIR = Path(path)
        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    def log(self, event_type: EventType, source: str, message: str, data: Dict[str, Any] = None):
        """Log an event"""
        event = Event(
            event_type=event_type,
            timestamp=datetime.now(),
            source=source,
            message=message,
            data=data or {}
        )
        self.events.append(event)
        
        if self.verbose:
            print(f"[{event_type.value.upper()}] {source}: {message}")
    
    def start_run(self):
        """Mark the start of a production run"""
        self.reset()
        self.start_time = datetime.now()
        # Ensure directory exists on each run
        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)
        self.log(EventType.SYSTEM_START, "System", "Production run started")
    
    def end_run(self):
        """Mark the end of a production run"""
        self.end_time = datetime.now()
        self.log(EventType.JOB_COMPLETED, "System", "Production run completed")
    
    # ============== Negotiation Events ==============
    
    def log_cfp_sent(self, skill: str, time_slot: str, participants: List[str]):
        """Log CFP broadcast"""
        self.negotiation = NegotiationSummary(
            request_skill=skill,
            request_time_slot=time_slot,
            participants=participants
        )
        self.log(EventType.CFP_RECEIVED, "NegotiationCore", 
                 f"CFP sent for '{skill}' at {time_slot} to {len(participants)} resources",
                 {"skill": skill, "time_slot": time_slot, "participants": participants})
    
    def log_cfp_response(self, resource_id: str, response: Dict[str, Any]):
        """Log a CFP response from a resource"""
        if self.negotiation:
            self.negotiation.responses[resource_id] = response
        self.log(EventType.CFP_RESPONSE, resource_id,
                 f"Response: slot={response.get('time_slot_next')}, state={response.get('time_slot_state')}",
                 response)
    
    def log_resource_selected(self, resource_id: str, time_slot: str, reason: str):
        """Log the selected resource"""
        if self.negotiation:
            self.negotiation.selected_resource = resource_id
            self.negotiation.selection_reason = reason
        self.log(EventType.RESOURCE_SELECTED, "NegotiationCore",
                 f"Selected {resource_id} for slot {time_slot}",
                 {"resource": resource_id, "time_slot": time_slot, "reason": reason})
    
    # ============== Execution Events ==============
    
    def log_execution_started(self, resource_id: str, skill: str):
        """Log execution start"""
        self.execution = ExecutionSummary(resource=resource_id)
        self.log(EventType.EXECUTION_STARTED, resource_id,
                 f"Starting execution of '{skill}'",
                 {"skill": skill})
    
    def log_operation(self, resource_id: str, operation: str, status: str, 
                      duration: float = None, result: Any = None):
        """Log an operation (move, drill, etc.)"""
        op_data = {
            "operation": operation,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        if duration:
            op_data["duration_seconds"] = duration
        if result:
            op_data["result"] = result
            
        if self.execution:
            self.execution.operations.append(op_data)
            if duration:
                self.execution.total_time_seconds += duration
        
        event_type = EventType.OPERATION_STARTED if status == "running" else EventType.OPERATION_COMPLETED
        self.log(event_type, resource_id, f"{operation}: {status}", op_data)
    
    def log_execution_completed(self, resource_id: str, status: str = "success"):
        """Log execution completion"""
        if self.execution:
            self.execution.status = status
        self.log(EventType.JOB_COMPLETED, resource_id, f"Execution {status}")
    
    # ============== AAS Update Events ==============
    
    def log_aas_update(self, submodel: str, element: str, old_value: Any, new_value: Any):
        """Log an AAS update"""
        update = {
            "timestamp": datetime.now().isoformat(),
            "submodel": submodel,
            "element": element,
            "old_value": old_value,
            "new_value": new_value
        }
        self.aas_updates.append(update)
        self.log(EventType.AAS_UPDATED, "AAS",
                 f"{submodel}/{element}: {old_value} → {new_value}",
                 update)
    
    # ============== Report Generation ==============
    
    def generate_report(self) -> str:
        """Generate a formatted summary report"""
        lines = []
        
        # Header
        lines.append("")
        lines.append("╔" + "═" * 78 + "╗")
        lines.append("║" + " PRODUCTION RUN REPORT ".center(78) + "║")
        lines.append("╚" + "═" * 78 + "╝")
        lines.append("")
        
        # Timing
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
            lines.append("┌─ TIMING " + "─" * 69)
            lines.append(f"│  Start Time:    {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"│  End Time:      {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"│  Total Duration: {duration:.2f} seconds")
            lines.append("")
        
        # Negotiation Summary
        if self.negotiation:
            lines.append("┌─ NEGOTIATION " + "─" * 64)
            lines.append(f"│  Requested Skill:  {self.negotiation.request_skill}")
            lines.append(f"│  Requested Slot:   {self.negotiation.request_time_slot}")
            lines.append(f"│  Participants:     {', '.join(self.negotiation.participants)}")
            lines.append("│")
            lines.append("│  Responses:")
            for resource, response in self.negotiation.responses.items():
                state = response.get('time_slot_state', 'unknown')
                slot = response.get('time_slot_next', 'N/A')
                violations = response.get('violations', [])
                status_icon = "✓" if state == "available" else "✗"
                lines.append(f"│    {status_icon} {resource}: {slot} ({state})")
                if violations:
                    lines.append(f"│      Violations: {violations}")
            lines.append("│")
            lines.append(f"│  ★ Selected: {self.negotiation.selected_resource}")
            if self.negotiation.selection_reason:
                lines.append(f"│    Reason: {self.negotiation.selection_reason}")
            lines.append("")
        
        # Execution Summary
        if self.execution:
            lines.append("┌─ EXECUTION " + "─" * 66)
            lines.append(f"│  Resource:      {self.execution.resource}")
            lines.append(f"│  Status:        {self.execution.status}")
            lines.append(f"│  Total Time:    {self.execution.total_time_seconds:.2f} seconds")
            lines.append("│")
            lines.append("│  Operations:")
            for op in self.execution.operations:
                name = op.get('operation', 'unknown')
                status = op.get('status', 'unknown')
                duration = op.get('duration_seconds', 0)
                result = op.get('result', '')
                if status == "completed":
                    lines.append(f"│    ✓ {name}: {duration:.2f}s → {result}")
                else:
                    lines.append(f"│    → {name}: {status}")
            lines.append("")
        
        # AAS Updates
        if self.aas_updates:
            lines.append("┌─ AAS UPDATES " + "─" * 64)
            for update in self.aas_updates:
                submodel = update['submodel']
                element = update['element']
                new_val = update['new_value']
                lines.append(f"│  • {element}: {new_val}")
            lines.append("")
        
        # Footer
        lines.append("╔" + "═" * 78 + "╗")
        lines.append("║" + " END OF REPORT ".center(78) + "║")
        lines.append("╚" + "═" * 78 + "╝")
        lines.append("")
        
        return "\n".join(lines)
    
    def print_report(self):
        """Print the report to console"""
        print(self.generate_report())
    
    def save_report(self, filename: str = None):
        """Save report to file"""
        if filename is None:
            filename = f"production_run_{self.run_id}.txt"
        
        # Ensure directory exists
        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)
        
        filepath = self.REPORT_DIR / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.generate_report())
            print(f"📄 Report saved to: {filepath}")
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
        return filepath
    
    def save_all(self):
        """Save both text report and JSON export"""
        # Ensure directory exists
        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save text report
        txt_path = self.save_report()
        
        # Save JSON export
        json_filename = f"production_run_{self.run_id}.json"
        json_path = self.REPORT_DIR / json_filename
        try:
            self.export_json(str(json_path))
            print(f"📄 JSON saved to: {json_path}")
        except Exception as e:
            print(f"❌ Failed to save JSON: {e}")
        
        return txt_path, json_path
    
    def export_json(self, filepath: str = None) -> Dict[str, Any]:
        """Export all data as JSON"""
        data = {
            "run_id": self.run_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else None,
            "negotiation": {
                "request_skill": self.negotiation.request_skill if self.negotiation else None,
                "request_time_slot": self.negotiation.request_time_slot if self.negotiation else None,
                "participants": self.negotiation.participants if self.negotiation else [],
                "responses": self.negotiation.responses if self.negotiation else {},
                "selected_resource": self.negotiation.selected_resource if self.negotiation else None,
            } if self.negotiation else None,
            "execution": {
                "resource": self.execution.resource if self.execution else None,
                "operations": self.execution.operations if self.execution else [],
                "total_time_seconds": self.execution.total_time_seconds if self.execution else 0,
                "status": self.execution.status if self.execution else None,
            } if self.execution else None,
            "aas_updates": self.aas_updates,
            "events": [
                {
                    "type": e.event_type.value,
                    "timestamp": e.timestamp.isoformat(),
                    "source": e.source,
                    "message": e.message,
                    "data": e.data
                }
                for e in self.events
            ]
        }
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        
        return data


# Global instance
report = ReportCollector()