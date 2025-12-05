from spade.behaviour import CyclicBehaviour
import json
from aastype3.Core.Report.AgentsReporter import report, EventType


class GetUserRequestBehaviour(CyclicBehaviour):
    async def run(self):
        pass  # Event-driven via handle_user_request
    
    async def handle_user_request(self, payload: str):
        """Handle incoming user request"""
        # Start the report
        #report.start_run()
        
        request_data = json.loads(payload)
        skill = request_data.get('skills_required', 'unknown')
        time_slot = request_data.get('at_time', 'unknown')
        
        report.log(EventType.CFP_RECEIVED, "UserAgent", 
                   f"New request: {skill} at {time_slot}",
                   request_data)
        
        # Publish to negotiation core
        await self.agent.pubsub.publish(
            "pubsub.localhost",
            "pa_execution_service_topic",
            payload
        )