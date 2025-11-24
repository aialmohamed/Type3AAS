import json
import html


class CfpPubSubMessage:
    def __init__(self, payload: str | None = None):
        self.payload = payload or ""
        self.resource_id = None
        self.skills = None
        self.at_time = None
        self.Input_arguments = {}

    def create_message_to_publish(self) -> str:
        return json.dumps(
            {
                "resource_id": self.resource_id,
                "skills_required": self.skills,
                "at_time": self.at_time,
                "input_arguments": self.Input_arguments,
            }
        )

    def parse_message(self) -> dict:
        raw = (self.payload or "").strip()
        if not raw:
            return {}
        try:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = json.loads(html.unescape(raw))

            self.resource_id = data.get("resource_id")
            self.skills = data.get("skills_required")
            self.at_time = data.get("at_time")
            self.Input_arguments = data.get("input_arguments", {})
            return data
        except Exception as exc:
            print(f"✗ Error parsing payload: {exc}")
            return {}