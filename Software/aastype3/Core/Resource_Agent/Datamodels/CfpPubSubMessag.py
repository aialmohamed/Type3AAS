

import json
import slixmpp.stanza
import re 
import html
class CfpPubSubMessage:
    def __init__(self,message: slixmpp.stanza.Message = None):
        self.message = message
        self.skills = None
        self.at_time = None
        self.Input_arguments = {}

    def create_message_to_publish(self) -> str:
        cfp_dict = {
            "skills_required": self.skills,
            "at_time": self.at_time,
            "input_arguments": self.Input_arguments
        }
        return json.dumps(cfp_dict)
    
    def parse_message(self) -> dict:
        """Parse any JSON message (with or without HTML encoding)."""
        message_text = str(self.message)
        match = re.search(r'<payload[^>]*>(.*?)</payload>', message_text)
        raw_message = match.group(1) if match else message_text
        try:
            # Try direct parsing first
            try:
                data = json.loads(raw_message)
            except json.JSONDecodeError:
                # If that fails, try HTML decoding first
                decoded = html.unescape(raw_message)
                data = json.loads(decoded)
            
            # Set attributes
            self.skills = data.get("skills_required")
            self.at_time = data.get("at_time")
            self.Input_arguments = data.get("input_arguments", {})
            
            return data
            
        except Exception as e:
            print(f"✗ Error parsing: {e}")
            return {}
    
    def parse_message_raw(self) -> str:
        """Parse any JSON message (with or without HTML encoding)."""
        try:
            message_text = str(self.message)
            match = re.search(r'<payload[^>]*>(.*?)</payload>', message_text)
            raw_message = match.group(1) if match else message_text
            return raw_message
        except Exception as e:
            print(f"✗ Error parsing: {e}")
            return ""

