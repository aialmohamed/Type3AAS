import json
from spade.behaviour import OneShotBehaviour


class PublishNegotiationResultBehaviour(OneShotBehaviour):
    """Publish the negotiation result to the Execution Core."""
    
    async def run(self):
        if not self.agent.selected_resource:
            print("No selected resource to publish.")
            return
        
        # Get all participants from the responses
        all_participants = list(self.agent.received_responses.keys())
        
        # Build the result payload
        result_payload = {
            "selected_resource": self.agent.selected_resource["resource_id"],
            "time_slot": self.agent.selected_resource["time_slot"],
            "state": self.agent.selected_resource["state"],
            "original_request": json.loads(self.agent.execution_service_template.body),
            "all_participants": all_participants  # Add all participants
        }
        
        await self.agent.pubsub.publish(
            "pubsub.localhost",
            "pa_negotation_result",
            json.dumps(result_payload)
        )
        print(f"Published negotiation result to Execution Core: {result_payload}")