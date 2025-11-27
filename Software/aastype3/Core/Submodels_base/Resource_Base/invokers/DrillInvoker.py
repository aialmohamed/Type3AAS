import asyncio
import json
import logging
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from basyx.aas import model
from basyx.aas.model import datatypes

app = FastAPI()
logger = logging.getLogger("drill_invoker")
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
    props = []
    for item in opvars:
        prop = _to_property(item)
        if prop:
            props.append(prop)
    return props


@app.post("/drill_invocation_1")
async def invoke_operation(request: Request):
    try:
        body = await request.json()
    except Exception:
        raw = await request.body()
        body = json.loads(raw.decode("utf-8", "replace") or "[]")

    logger.info(
        "Invocation request from=%s headers=%s",
        getattr(request.client, "host", None),
        dict(request.headers),
    )
    logger.info("Invocation body:\n%s", json.dumps(body, indent=4, ensure_ascii=False))

    properties = _opvars_to_properties(body)
    if not properties:
        raise HTTPException(status_code=400, detail="Failed to map inputs to Properties")

    try:
        depth = float(properties[0].value)
    except Exception:
        raise HTTPException(status_code=400, detail="First input is not numeric")

    await asyncio.sleep(3)
    response = [
        {
            "modelType": "OperationVariable",
            "value": {
                "modelType": "Property",
                "idShort": "Drill_Result",
                "value": str(depth),
                "valueType": "xs:string",
                "category": "PARAMETER",
                "displayName": [{"language": "en", "text": "Drill Result"}],
                "description": [{"language": "en", "text": "Result of the drilling operation"}],
            },
        }
    ]
    logger.info("Returning response JSON:\n%s", json.dumps(response, indent=2))
    return response

@app.post("/drill_invocation_2")
async def invoke_operation(request: Request):
    try:
        body = await request.json()
    except Exception:
        raw = await request.body()
        body = json.loads(raw.decode("utf-8", "replace") or "[]")

    logger.info(
        "Invocation request from=%s headers=%s",
        getattr(request.client, "host", None),
        dict(request.headers),
    )
    logger.info("Invocation body:\n%s", json.dumps(body, indent=4, ensure_ascii=False))

    properties = _opvars_to_properties(body)
    if not properties:
        raise HTTPException(status_code=400, detail="Failed to map inputs to Properties")

    try:
        depth = float(properties[0].value)
    except Exception:
        raise HTTPException(status_code=400, detail="First input is not numeric")

    await asyncio.sleep(3)
    response = [
        {
            "modelType": "OperationVariable",
            "value": {
                "modelType": "Property",
                "idShort": "Drill_Result",
                "value": str(depth),
                "valueType": "xs:string",
                "category": "PARAMETER",
                "displayName": [{"language": "en", "text": "Drill Result"}],
                "description": [{"language": "en", "text": "Result of the drilling operation"}],
            },
        }
    ]
    logger.info("Returning response JSON:\n%s", json.dumps(response, indent=2))
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090, log_level="info")