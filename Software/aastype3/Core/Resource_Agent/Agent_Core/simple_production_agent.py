import asyncio
import pathlib
import json
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade_pubsub.pubsub import PubSubMixin
from spade_bdi.bdi import BDIAgent
from aastype3.Core.Resource_Agent.Datamodels.CfpPubSubMessag import CfpPubSubMessage


class NeogotitaionPubliserBehaviour(OneShotBehaviour):
    async def run(self):
        print("Publishing negotiation message")
        cfp_message = CfpPubSubMessage()
        cfp_message.skills = "movexy_capability"
        cfp_message.at_time = "10:00-10:30"
        self.agent.last_requested_slot = cfp_message.at_time
        cfp_message.Input_arguments = {"X": 60, "Y": 50, "Depth": 5, "RPM": 1500}
        message_to_publish = cfp_message.create_message_to_publish()
        await self.agent.pubsub.publish(
            "pubsub.localhost", "production_negotiation", message_to_publish
        )


class ReceiveViolationBehaviour(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(1)

    async def handle_violation(self, payload: str):
        print(f"Handling violation with payload: {payload}")


class ReceiveJobCompletionBehaviour(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(1)

    async def handle_job_completion(self, payload: str):
        print(f"Handling job completion with payload: {payload}")

class ReciveCounterProposalBehaviour(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(1)

    async def handle_counter_proposal(self, payload: str):
        print(f"Handling counter proposal with payload: {payload}")
        cfp_message = CfpPubSubMessage(payload=payload)
        parsed = cfp_message.parse_message() or {}
        free_slots = parsed.get("at_time") or []
        requested = getattr(self.agent, "last_requested_slot", None)

        def next_after(slots, current):
            if not slots:
                return None
            if not current:
                return slots[0]
            for slot in slots:
                if slot.split("-")[0] > current.split("-")[0]:
                    return slot
            return slots[0]

        chosen = next_after(free_slots, requested)
        if not chosen:
            print("No available alternative slot.")
            return

        parsed["at_time"] = chosen
        self.agent.last_requested_slot = chosen
        await self.agent.pubsub.publish(
            "pubsub.localhost", "production_negotiation", json.dumps(parsed)
        )
        self.kill()


class SimpleProductionAgent(PubSubMixin, BDIAgent):
    def __init__(self, jid, password, asl_path):
        self.at_time = None
        self.last_requested_slot = "10:00-10:30"
        super().__init__(jid, password, asl_path)

    async def setup(self):
        self.cfp_template = Template()
        self.cfp_template.set_metadata("performative", "cfp")
        await self.pubsub.subscribe("pubsub.localhost", "violations_topic")
        await self.pubsub.subscribe("pubsub.localhost", "counter_proposals_topic")
        await self.pubsub.subscribe("pubsub.localhost", "job_completion_topic")
        self.pubsub.set_on_item_published(self._on_pubsub_event)
        print(
            "Current subscriptions:",
            await self.pubsub.get_node_subscriptions(
                "pubsub.localhost", "production_negotiation"
            ),
        )

    async def _on_pubsub_event(self, message):
        try:
            event = message["pubsub_event"]
            node = event["items"]["node"]
            payload_elem = event["items"]["substanzas"][0]["payload"]
            payload = (
                payload_elem.text if hasattr(payload_elem, "text") else str(payload_elem)
            )
        except Exception as exc:
            print(f"Failed to parse pubsub event: {exc}")
            return

        if node == "violations_topic":
            await self.receive_violation_behaviour.handle_violation(payload)
        elif node == "counter_proposals_topic":
            await self.receive_counter_proposal_behaviour.handle_counter_proposal(
                payload
            )
        elif node == "job_completion_topic":
            await self.receive_job_completion_behaviour.handle_job_completion(
                payload
            )

    def add_behaviours(self):
        self.receive_violation_behaviour = ReceiveViolationBehaviour()
        self.add_behaviour(self.receive_violation_behaviour)
        self.receive_counter_proposal_behaviour = ReciveCounterProposalBehaviour()
        self.add_behaviour(self.receive_counter_proposal_behaviour)
        self.add_behaviour(NeogotitaionPubliserBehaviour())
        self.receive_job_completion_behaviour = ReceiveJobCompletionBehaviour()
        self.add_behaviour(self.receive_job_completion_behaviour)


async def main():
    asl = pathlib.Path(__file__).parent / "simple_production_agent.asl"
    agent = SimpleProductionAgent(
        "simple_product_agent@localhost", "password123", str(asl)
    )
    agent.add_behaviours()
    await agent.start(auto_register=True)
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await agent.stop()


if __name__ == "__main__":
    import spade

    spade.run(main())