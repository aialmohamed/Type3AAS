"""
Simulator Report - Collects and displays simulation metrics
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any
from enum import Enum
from pathlib import Path
import json


class OperationType(Enum):
    MOVE = "move"
    DRILL = "drill"


@dataclass
class OperationRecord:
    operation_type: OperationType
    start_time: datetime
    end_time: datetime = None
    duration_seconds: float = 0.0
    parameters: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    status: str = "running"


@dataclass
class SimulatorReport:
    machine_id: str
    machine_type: str  # "drill" or "movexy"
    port: int
    start_time: datetime = None
    operations: List[OperationRecord] = field(default_factory=list)
    
    # Aggregate stats
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    total_processing_time: float = 0.0
    total_idle_time: float = 0.0
    
    # Position tracking (for move machines)
    initial_position: Dict[str, float] = field(default_factory=lambda: {"x": 0.0, "y": 0.0})
    current_position: Dict[str, float] = field(default_factory=lambda: {"x": 0.0, "y": 0.0})
    total_distance_traveled: float = 0.0
    
    # Drill tracking
    total_depth_drilled: float = 0.0
    
    # Report directory
    REPORT_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent / "reports" / "simulators")
    
    def __post_init__(self):
        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    def reset(self):
        """Reset all statistics"""
        self.start_time = datetime.now()
        self.operations = []
        self.total_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0
        self.total_processing_time = 0.0
        self.total_idle_time = 0.0
        self.current_position = {"x": 0.0, "y": 0.0}
        self.total_distance_traveled = 0.0
        self.total_depth_drilled = 0.0
    
    def start_operation(self, op_type: OperationType, parameters: Dict[str, Any]) -> OperationRecord:
        """Start tracking a new operation"""
        record = OperationRecord(
            operation_type=op_type,
            start_time=datetime.now(),
            parameters=parameters,
            status="running"
        )
        self.operations.append(record)
        self.total_operations += 1
        return record
    
    def complete_operation(self, record: OperationRecord, result: Any, 
                          duration: float, success: bool = True):
        """Complete an operation"""
        record.end_time = datetime.now()
        record.duration_seconds = duration
        record.result = result
        record.status = "success" if success else "failed"
        
        self.total_processing_time += duration
        
        if success:
            self.successful_operations += 1
            
            # Update type-specific stats
            if record.operation_type == OperationType.MOVE:
                x = record.parameters.get('target_x', 0)
                y = record.parameters.get('target_y', 0)
                old_x = self.current_position['x']
                old_y = self.current_position['y']
                distance = ((x - old_x)**2 + (y - old_y)**2) ** 0.5
                self.total_distance_traveled += distance
                self.current_position = {"x": x, "y": y}
                
            elif record.operation_type == OperationType.DRILL:
                depth = record.parameters.get('depth', 0)
                self.total_depth_drilled += depth
        else:
            self.failed_operations += 1
    
    def get_utilization(self) -> float:
        """Calculate machine utilization percentage"""
        if not self.start_time:
            return 0.0
        total_time = (datetime.now() - self.start_time).total_seconds()
        if total_time == 0:
            return 0.0
        return (self.total_processing_time / total_time) * 100
    
    def get_average_operation_time(self) -> float:
        """Get average operation time"""
        if self.successful_operations == 0:
            return 0.0
        return self.total_processing_time / self.successful_operations
    
    def generate_report(self) -> str:
        """Generate a formatted report"""
        lines = []
        
        # Header
        lines.append("")
        lines.append("┌" + "─" * 58 + "┐")
        lines.append(f"│{f' {self.machine_id} SIMULATION REPORT ':^58}│")
        lines.append("└" + "─" * 58 + "┘")
        lines.append("")
        
        # Machine Info
        lines.append(f"  Machine Type:    {self.machine_type}")
        lines.append(f"  Port:            {self.port}")
        if self.start_time:
            lines.append(f"  Running Since:   {self.start_time.strftime('%H:%M:%S')}")
            uptime = (datetime.now() - self.start_time).total_seconds()
            lines.append(f"  Uptime:          {uptime:.1f}s")
        lines.append("")
        
        # Statistics
        lines.append("  ┌─ STATISTICS " + "─" * 43)
        lines.append(f"  │  Total Operations:     {self.total_operations}")
        lines.append(f"  │  Successful:           {self.successful_operations}")
        lines.append(f"  │  Failed:               {self.failed_operations}")
        lines.append(f"  │  Total Processing:     {self.total_processing_time:.2f}s")
        lines.append(f"  │  Avg Operation Time:   {self.get_average_operation_time():.2f}s")
        lines.append(f"  │  Utilization:          {self.get_utilization():.1f}%")
        lines.append("")
        
        # Type-specific stats
        if self.machine_type == "movexy":
            lines.append("  ┌─ MOVEMENT STATS " + "─" * 39)
            lines.append(f"  │  Current Position:     ({self.current_position['x']:.1f}, {self.current_position['y']:.1f})")
            lines.append(f"  │  Total Distance:       {self.total_distance_traveled:.2f} units")
            lines.append("")
        elif self.machine_type == "drill":
            lines.append("  ┌─ DRILLING STATS " + "─" * 38)
            lines.append(f"  │  Total Depth Drilled:  {self.total_depth_drilled:.2f} mm")
            lines.append("")
        
        # Recent Operations (last 5)
        if self.operations:
            lines.append("  ┌─ RECENT OPERATIONS " + "─" * 36)
            for op in self.operations[-5:]:
                status_icon = "✓" if op.status == "success" else "✗" if op.status == "failed" else "→"
                time_str = op.start_time.strftime('%H:%M:%S')
                lines.append(f"  │  {status_icon} [{time_str}] {op.operation_type.value}: {op.duration_seconds:.2f}s")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_report(self, filename: str = None):
        """Save report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.machine_id}_{timestamp}.txt"
        
        filepath = self.REPORT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
        
        print(f"📄 Simulator report saved to: {filepath}")
        return filepath
    
    def save_json(self, filename: str = None):
        """Save report as JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.machine_id}_{timestamp}.json"
        
        filepath = self.REPORT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        print(f"📄 Simulator JSON saved to: {filepath}")
        return filepath
    
    def save_all(self):
        """Save both text and JSON reports"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_path = self.save_report(f"{self.machine_id}_{timestamp}.txt")
        json_path = self.save_json(f"{self.machine_id}_{timestamp}.json")
        return txt_path, json_path
    
    def to_dict(self) -> Dict[str, Any]:
        """Export as dictionary (for JSON API)"""
        return {
            "machine_id": self.machine_id,
            "machine_type": self.machine_type,
            "port": self.port,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "statistics": {
                "total_operations": self.total_operations,
                "successful_operations": self.successful_operations,
                "failed_operations": self.failed_operations,
                "total_processing_time_seconds": self.total_processing_time,
                "average_operation_time_seconds": self.get_average_operation_time(),
                "utilization_percent": self.get_utilization(),
            },
            "position": self.current_position if self.machine_type == "movexy" else None,
            "total_distance_traveled": self.total_distance_traveled if self.machine_type == "movexy" else None,
            "total_depth_drilled": self.total_depth_drilled if self.machine_type == "drill" else None,
            "recent_operations": [
                {
                    "type": op.operation_type.value,
                    "start_time": op.start_time.isoformat(),
                    "duration_seconds": op.duration_seconds,
                    "status": op.status,
                    "parameters": op.parameters,
                    "result": op.result
                }
                for op in self.operations[-10:]
            ]
        }