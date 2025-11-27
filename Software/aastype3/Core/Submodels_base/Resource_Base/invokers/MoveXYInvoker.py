import asyncio
import json
import logging
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from basyx.aas import model
from basyx.aas.model import datatypes

app = FastAPI()
logger = logging.getLogger("movexy_invoker")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

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
    value = item.get("value") if isinstance(item, dict) else item
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
    props = []
    for item in opvars:
        prop = _to_property(item)
        if prop:
            props.append(prop)
    return props

@app.post("/movexy_invocation_1")
async def invoke_operation(request: Request):
    try:
        body = await request.json()
    except Exception:
        raw = await request.body()
        body = json.loads(raw.decode("utf-8", "replace") or "[]")

    logger.info("MoveXY request from=%s body=%s", getattr(request.client, "host", None), body)
    props = _opvars_to_properties(body)
    if len(props) < 2:
        raise HTTPException(status_code=400, detail="Need Target_X and Target_Y")

    def _get_value(prop: model.Property, fallback: float = 0.0) -> float:
        try:
            return float(prop.value)
        except Exception:
            return fallback

    x_target = _get_value(props[0])
    y_target = _get_value(props[1])

    await asyncio.sleep(2)

    response = [
        {
            "modelType": "OperationVariable",
            "value": {
                "modelType": "Property",
                "idShort": "Move_Result",
                "valueType": "xs:string",
                "category": "PARAMETER",
                "displayName": [{"language": "en", "text": "Move Result"}],
                "description": [{"language": "en", "text": "Result of the move operation"}],
                "value": str(x_target),
            },
        }
    ]
    logger.info("MoveXY response: %s", response)
    return response

@app.post("/movexy_invocation_2")
async def invoke_operation(request: Request):
    try:
        body = await request.json()
    except Exception:
        raw = await request.body()
        body = json.loads(raw.decode("utf-8", "replace") or "[]")

    logger.info("MoveXY request from=%s body=%s", getattr(request.client, "host", None), body)
    props = _opvars_to_properties(body)
    if len(props) < 2:
        raise HTTPException(status_code=400, detail="Need Target_X and Target_Y")

    def _get_value(prop: model.Property, fallback: float = 0.0) -> float:
        try:
            return float(prop.value)
        except Exception:
            return fallback

    x_target = _get_value(props[0])
    y_target = _get_value(props[1])

    await asyncio.sleep(2)

    response = [
        {
            "modelType": "OperationVariable",
            "value": {
                "modelType": "Property",
                "idShort": "Move_Result",
                "valueType": "xs:string",
                "category": "PARAMETER",
                "displayName": [{"language": "en", "text": "Move Result"}],
                "description": [{"language": "en", "text": "Result of the move operation"}],
                "value": str(x_target),
            },
        }
    ]
    logger.info("MoveXY response: %s", response)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8092, log_level="info")