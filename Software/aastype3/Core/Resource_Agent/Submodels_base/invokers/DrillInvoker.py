import asyncio
import json
import logging
from typing import Any, Dict, List
from fastapi import FastAPI, Request, HTTPException
import uvicorn
from basyx.aas import model
import basyx.aas.model.datatypes as datatypes

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("drill_invoker")

app = FastAPI()

def _opvars_to_properties(opvars: List[Dict[str, Any]]) -> List[model.Property]:
    """
    Map OperationVariable[] payload (as dicts) into basyx.model.Property instances.
    Handles common name variants (idShort / id_short / valueType) and missing fields.
    """
    vt_map = {
        "xs:double": (datatypes.Double, float),
        "double": (datatypes.Double, float),
        "xs:int": (datatypes.Integer, int),
        "int": (datatypes.Integer, int),
        "xs:integer": (datatypes.Integer, int),
        "xs:string": (datatypes.String, str),
        "string": (datatypes.String, str),
        "xs:boolean": (datatypes.Boolean, lambda v: str(v).lower() in ("true", "1")),
        "boolean": (datatypes.Boolean, lambda v: str(v).lower() in ("true", "1"))
    }
    props: List[model.Property] = []
    for item in opvars:
        # payload can be {"value": {...Property...}} or the Property dict directly
        prop_dict = item.get("value") if isinstance(item, dict) and "value" in item else (item if isinstance(item, dict) else None)
        if not prop_dict:
            continue
        id_short = prop_dict.get("idShort") or prop_dict.get("id_short") or prop_dict.get("id")
        vt = prop_dict.get("valueType") or prop_dict.get("value_type") or prop_dict.get("valueType")
        raw_val = prop_dict.get("value")
        # determine basyx datatype class and converter
        vt_entry = vt_map.get(vt)
        if vt_entry:
            vt_cls, converter = vt_entry
            try:
                # convert raw value to appropriate python type before creating Property
                conv_val = converter(raw_val) if raw_val is not None else None
            except Exception:
                # fallback to string if conversion fails
                conv_val = raw_val
                vt_cls = datatypes.String
        else:
            # no type information -> treat as string
            vt_cls = datatypes.String
            conv_val = raw_val if raw_val is not None else ""
        try:
            # basyx Property expects a value_type argument
            p = model.Property(
                id_short or "unknown",
                vt_cls,
                conv_val,
                category=prop_dict.get("category"),
                description=prop_dict.get("description"),
                display_name=prop_dict.get("displayName")
            )
            props.append(p)
        except Exception:
            # last-resort fallback: create Property with string type
            try:
                p = model.Property(
                    id_short or "unknown",
                    datatypes.String,
                    str(raw_val) if raw_val is not None else ""
                )
                props.append(p)
            except Exception:
                # give up on this item
                continue
    return props




@app.post("/drill_invocation")
async def invoke_operation(request: Request):
    try:
        # read body (robust)
        try:
            body = await request.json()
        except Exception:
            raw = await request.body()
            body = {"_raw_body": raw.decode("utf-8", "replace")}
        logger.info("Invocation request from=%s headers=%s", getattr(request.client, "host", None), dict(request.headers))
        logger.info("Invocation body:\n%s", json.dumps(body, indent=4, ensure_ascii=False))
        properties = _opvars_to_properties(body)
        if not properties:
            raise HTTPException(status_code=400, detail="Failed to map inputs to Properties")

        # now use basyx Property objects (value may be string; cast accordingly)
        first_prop = properties[0]
        try:
            depth = float(first_prop.value)
        except Exception:
            raise HTTPException(status_code=400, detail="First input is not numeric")

        result = depth
        await asyncio.sleep(3)  # simulate processing delay
        response_var = {
            "modelType": "OperationVariable",
            "value": {
                "modelType": "Property",
                "idShort": "Drill_Result",
                "value": str(result),
                "valueType": "xs:string",
                "category": "PARAMETER",
                "displayName": [{"language": "en", "text": "Drill Result"}],
                "description": [{"language": "en", "text": "Result of the drilling operation"}]
           }
        }
        resp_json = [response_var]
        logger.info("Returning response JSON:\n%s", json.dumps(resp_json, indent=2))
        return resp_json
    except HTTPException:
        raise
    except Exception as exc:
        # log full stacktrace for debugging
        logger.exception("Unhandled exception in invoke_operation")
        # return a 500 with a short message (do NOT leak stack traces in prod)
        raise HTTPException(status_code=500, detail=f"Invoker error: {exc}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090, log_level="info")