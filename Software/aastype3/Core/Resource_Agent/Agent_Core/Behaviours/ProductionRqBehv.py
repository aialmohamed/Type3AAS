
from spade.behaviour import CyclicBehaviour
import asyncio
import slixmpp.stanza
from aastype3.Core.Resource_Agent.Datamodels.CfpPubSubMessag import CfpPubSubMessage



class ProductionRequestBehaviour(CyclicBehaviour):
    async def on_start(self):
        await self.agent.pubsub.subscribe("pubsub.localhost", "production_negotiation")
        self.agent.pubsub.set_on_item_published(self.on_message)

    async def run(self):
        await asyncio.sleep(1)
        
    async def on_message(self, message: slixmpp.stanza.Message):
        try:
            event = message['pubsub_event']
            node = event['items']['node']
            payload = event['items']['substanzas'][0]['payload'].text
            if node == 'production_negotiation':
                cfp_message = CfpPubSubMessage(payload)
                self.agent.received_cfp = cfp_message.parse_message()
                data = self.agent.received_cfp
                cfp_skills = data.get("skills_required")
                cfp_at_time = data.get("at_time")
                input_arguments = data.get("input_arguments")


                try: self.agent.bdi.remove_belief("cfp_skill")
                except Exception: pass
                self.agent.bdi.set_belief("cfp_skill", cfp_skills)

                try: self.agent.bdi.remove_belief("cfp_at_time")
                except Exception: pass
                self.agent.bdi.set_belief("cfp_at_time", cfp_at_time)

                try: self.agent.bdi.remove_belief("cfp_input_arguments")
                except Exception: pass
                self.agent.bdi.set_belief("cfp_input_arguments", str(input_arguments))
                self.agent.bdi.set_belief("is_cfp_received", True)
        except Exception as e:
            import traceback
            print(f"Error in callback type={type(e).__name__} msg={e!r}")
            traceback.print_exc()