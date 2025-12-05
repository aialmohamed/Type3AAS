from spade.behaviour import OneShotBehaviour
from datetime import datetime
import json


class PublishTrackingBehaviour(OneShotBehaviour):
    """Publishes tracking data to the production agent"""
    
    def __init__(self, step_name: str, step_status: str, result: str = None):
        super().__init__()
        self.step_name = step_name
        self.step_status = step_status
        self.result = result
    
    async def run(self):
        tracking_data = {
            "resource_id": str(self.agent.jid.bare),
            "current_node": self.step_name,
            "step_status": self.step_status,
            "timestamp": datetime.now().isoformat(),
            "skill": self.agent.bdi.get_belief_value("cfp_skill")[0],
            "time_slot": self.agent.bdi.get_belief_value("cfp_at_time")[0]
        }
        
        if self.result:
            tracking_data["result"] = self.result
        
        message = json.dumps(tracking_data)
        await self.agent.pubsub.publish(
            "pubsub.localhost",
            "execution_tracking_topic",
            message
        )