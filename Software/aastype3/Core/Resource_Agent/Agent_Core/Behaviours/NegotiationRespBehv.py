



import asyncio
import slixmpp.stanza
from spade.behaviour import CyclicBehaviour

class NegotationResponseBehaviour(CyclicBehaviour):
    async def on_start(self):
        await self.agent.pubsub.subscribe("pubsub.localhost", "pa_negotation_responses")
        self.agent.pubsub.set_on_item_published(self.on_message)
    async def run(self):
        await asyncio.sleep(1)
        
    async def on_message(self, message: slixmpp.stanza.Message):
        try:
            event = message['pubsub_event']
            node = event['items']['node']
            payload = event['items']['substanzas'][0]['payload'].text
            if node == 'pa_negotation_responses':
                # get the new at time 
                new_time = self.agent.new_cfp_proposal.time_slot_next

                if payload.lower() == "yes":
                    try:
                        self.agent.bdi.remove_belief("cfp_at_time")
                        self.agent.bdi.set_belief("cfp_at_time", new_time)
                        self.agent.bdi.set_belief("is_negotiation_response_positive", True)
                    except Exception as e:
                        print(f"Error updating belief: {e}")
                else:
                    self.agent.bdi.set_belief("is_negotiation_response_positive", False)

            else:
                pass
        except Exception as e:
            import traceback
            print(f"Error in callback type={type(e).__name__} msg={e!r}")
            traceback.print_exc()
