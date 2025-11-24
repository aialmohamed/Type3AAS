
import ast
import json

class Utils:
    def __init__(self):
        pass
    def to_dict(self,value):
        if isinstance(value, dict):
            return value
        if isinstance(value, (list, tuple)):
            s = ",".join(str(x) for x in value)
        else:
            s = str(value)
        s = s.strip()
        # try JSON (double quotes) then Python literal (single quotes)
        try:
            return json.loads(s)
        except Exception:
            pass
        try:
            return ast.literal_eval(s)
        except Exception:
            return {}
    def extract_belief_payload(self,raw: str) -> str:
        if not raw:
            return ""
        # remove trailing source annotation
        if ")[source" in raw:
            raw = raw[: raw.find(")[source") + 1]
        # drop predicate name + parentheses
        start = raw.find("(")
        end = raw.rfind(")")
        return raw[start + 1 : end] if start != -1 and end != -1 and end > start else raw

