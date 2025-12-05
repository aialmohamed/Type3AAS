import json
from spade.behaviour import  OneShotBehaviour


class SendNegotiationDecisionsBehaviour(OneShotBehaviour):
    """Send 'yes' to selected resource, 'no' to others."""
    async def run(self):
        if not self.agent.negotiation_result:
            print("No negotiation result to process.")
            return
        selected_resource = self.agent.negotiation_result.get("selected_resource", "")
        # Get all subscribers to production_negotiation
        subscribers = await self.agent.pubsub_owner.get_node_subscribers("production_negotiation")
        if not subscribers:
            print("No subscribers found.")
            return
        # Normalize subscriber names
        subscribers = [s.split("@")[0] for s in subscribers]
        print(f"Sending decisions to resources. Selected: {selected_resource}")
        for resource_id in subscribers:
            decision = "yes" if resource_id == selected_resource else "no"
            payload = json.dumps({"target": resource_id, "decision": decision})
            await self.agent.pubsub.publish(
                "pubsub.localhost",
                "pa_negotation_responses",
                payload
            )
            print(f"Sent '{decision}' to {resource_id}")
