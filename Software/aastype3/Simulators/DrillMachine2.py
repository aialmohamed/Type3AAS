"""
SimPy-based Drill Machine 2 Simulator
Same as Machine 1 but with slightly different characteristics:
- Different processing speeds (simulating different machine capabilities)
- Runs on a different port
"""

import asyncio
import json
import logging
from typing import Any, Dict, List
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from contextlib import asynccontextmanager

import simpy
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from basyx.aas import model
from basyx.aas.model import datatypes

from aastype3.Core.Report.SimulatorReport import SimulatorReport, OperationType

# ============== Configuration ==============
MACHINE_ID = "DrillMachine_2"
DRILL_SPEED_FACTOR = 0.6   # slightly slower than machine 1
BASE_SETUP_TIME = 0.6      # slightly longer setup
PORT = 8091

# ============== Setup ==============
logger = logging.getLogger(MACHINE_ID.lower())
logging.basicConfig(
    level=logging.INFO, 
    format=f"%(asctime)s [{MACHINE_ID}] %(levelname)s %(message)s"
)

# Report instance
sim_report = SimulatorReport(
    machine_id=MACHINE_ID,
    machine_type="drill",
    port=PORT
)


class MachineState(Enum):
    IDLE = "idle"
    DRILLING = "drilling"


@dataclass
class MachineStatus:
    state: MachineState = MachineState.IDLE
    current_depth: float = 0.0
    jobs_completed: int = 0
    total_drill_time: float = 0.0


# Global SimPy environment and machine resource
sim_env: simpy.Environment = None
machine_resource: simpy.Resource = None
machine_status = MachineStatus()


def init_simulation():
    """Initialize or reset the SimPy simulation environment"""
    global sim_env, machine_resource
    sim_env = simpy.Environment()
    machine_resource = simpy.Resource(sim_env, capacity=1)
    sim_report.reset()
    logger.info(f"SimPy environment initialized for {MACHINE_ID}")


# ============== Helper Functions ==============
VT_SCALE = {
    "xs:double": (datatypes.Double, float),
    "double": (datatypes.Double, float),
    "xs:int": (datatypes.Integer, int),
    "int": (datatypes.Integer, int),
    "xs:integer": (datatypes.Integer, int),
    "xs:string": (datatypes.String, str),
    "string": (datatypes.String, str),
    "xs:boolean": (datatypes.Boolean, lambda v: str(v).lower() in {"true", "1"}),
    "boolean": (datatypes.Boolean, lambda v: str(v).lower() in {"true", "1"}),
}


def _to_property(item: Dict[str, Any]) -> model.Property | None:
    value = item.get("value") if "value" in item else item
    if not isinstance(value, dict):
        return None
    id_short = value.get("idShort") or value.get("id_short") or value.get("id")
    vt_key = value.get("valueType") or value.get("value_type") or ""
    raw_val = value.get("value")
    vt_cls, caster = VT_SCALE.get(vt_key, (datatypes.String, str))
    try:
        cast_val = caster(raw_val) if raw_val is not None else None
    except Exception:
        vt_cls, cast_val = datatypes.String, str(raw_val)
    try:
        return model.Property(
            id_short or "unknown",
            vt_cls,
            cast_val,
            category=value.get("category"),
            description=value.get("description"),
            display_name=value.get("displayName"),
        )
    except Exception:
        return None


def _opvars_to_properties(opvars: List[Dict[str, Any]]) -> List[model.Property]:
    return [p for item in opvars if (p := _to_property(item))]


# ============== SimPy Processes ==============
def drill_process(env: simpy.Environment, depth: float, rpm: float):
    """SimPy process for drilling operation"""
    global machine_status
    
    rpm_factor = 1500 / max(rpm, 100)
    drill_time = BASE_SETUP_TIME + (depth * DRILL_SPEED_FACTOR * rpm_factor)
    
    machine_status.state = MachineState.DRILLING
    logger.info(f"🔩 Drilling: depth={depth}mm, rpm={rpm}, time={drill_time:.2f}s")
    
    yield env.timeout(drill_time)
    
    machine_status.current_depth = depth
    machine_status.total_drill_time += drill_time
    machine_status.jobs_completed += 1
    machine_status.state = MachineState.IDLE
    
    logger.info(f"✅ Drill complete")
    return (depth, drill_time)


async def run_simpy_process(process_generator):
    """Run a SimPy process and wait for completion using asyncio"""
    global sim_env, machine_resource
    
    result = None
    
    def process_wrapper(env):
        nonlocal result
        with machine_resource.request() as req:
            yield req
            result = yield from process_generator
    
    sim_env.process(process_wrapper(sim_env))
    
    while sim_env.peek() < float('inf'):
        next_time = sim_env.peek()
        current_time = sim_env.now
        delay = next_time - current_time
        if delay > 0:
            await asyncio.sleep(delay)
        sim_env.step()
    
    return result


# ============== API Endpoints ==============
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_simulation()
    logger.info(f"🏭 {MACHINE_ID} started on port {PORT}")
    yield
    # Save reports to files on shutdown
    sim_report.save_all()
    logger.info(f"🏭 {MACHINE_ID} shutting down")

app = FastAPI(title=f"{MACHINE_ID} Simulator", lifespan=lifespan)


@app.get("/status")
async def get_status():
    """Get current machine status"""
    return {
        "machine_id": MACHINE_ID,
        "state": machine_status.state.value,
        "last_depth": machine_status.current_depth,
        "jobs_completed": machine_status.jobs_completed,
        "total_drill_time": machine_status.total_drill_time,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/report")
async def get_report():
    """Get simulation report as JSON"""
    return sim_report.to_dict()


@app.get("/report/text")
async def get_report_text():
    """Get simulation report as formatted text"""
    return {"report": sim_report.generate_report()}


@app.post("/drill_invocation_2")
async def invoke_drill(request: Request):
    """Drill operation endpoint for Machine 2"""
    try:
        body = await request.json()
    except Exception:
        raw = await request.body()
        body = json.loads(raw.decode("utf-8", "replace") or "[]")

    properties = _opvars_to_properties(body)
    if not properties:
        raise HTTPException(status_code=400, detail="Failed to map inputs to Properties")

    try:
        depth = float(properties[0].value)
        rpm = float(properties[1].value) if len(properties) > 1 else 1500.0
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid input parameters")

    # Start tracking
    op_record = sim_report.start_operation(
        OperationType.DRILL,
        {"depth": depth, "rpm": rpm}
    )

    result, duration = await run_simpy_process(drill_process(sim_env, depth, rpm))

    # Complete tracking
    sim_report.complete_operation(op_record, result, duration, success=True)
    sim_report.save_all()
    response = [
        {
            "modelType": "OperationVariable",
            "value": {
                "modelType": "Property",
                "idShort": "Drill_Result",
                "value": str(result),
                "valueType": "xs:string",
                "category": "PARAMETER",
                "displayName": [{"language": "en", "text": "Drill Result"}],
                "description": [{"language": "en", "text": "Result of the drilling operation"}],
            },
        }
    ]
    return response


@app.post("/reset")
async def reset_machine():
    """Reset machine state and simulation"""
    global machine_status
    init_simulation()
    machine_status = MachineStatus()
    logger.info(f"🔄 {MACHINE_ID} reset to initial state")
    return {"status": "reset", "machine_id": MACHINE_ID}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")