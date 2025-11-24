
import json
from spade.behaviour import OneShotBehaviour
from aastype3.Core.Resource_Agent.Datamodels.CfpPubSubMessag import CfpPubSubMessage

class TimeSlotProcessingBehaviour(OneShotBehaviour):
    async def on_start(self):
        self.cfp_at_time = self.agent.bdi.get_belief_value("cfp_at_time")[0]
        self.free_time_slots = self.agent.bdi.get_belief("free_time_slots",source=True)
        self.free_time_slots  = self.agent.utils.extract_belief_payload(self.free_time_slots)
        self.free_time_slots  = json.loads(self.free_time_slots)
        self.booked_time_slots  = self.agent.bdi.get_belief("booked_time_slots",source=True)
        self.booked_time_slots  = self.agent.utils.extract_belief_payload(self.booked_time_slots)
        self.booked_time_slots  = json.loads(self.booked_time_slots)
        self.new_cfp_proposal = CfpPubSubMessage()

    async def run(self):

        if self.cfp_at_time in self.booked_time_slots:
            cfp_skill = self.agent.bdi.get_belief_value("cfp_skill")
            self.new_cfp_proposal.resource_id = str(self.agent.jid.bare)
            self.new_cfp_proposal.skills = cfp_skill[0] if isinstance(cfp_skill, (list, tuple)) else cfp_skill
            self.new_cfp_proposal.at_time = list(self.free_time_slots) if self.free_time_slots else "No Available Slot"
            self.new_cfp_proposal.Input_arguments = self.agent.bdi.get_belief_value("cfp_input_arguments")
            self.new_cfp_proposal.Input_arguments = self.agent.utils.to_dict(self.new_cfp_proposal.Input_arguments)
            message = self.new_cfp_proposal.create_message_to_publish()
            self.agent.bdi.set_belief("new_cfp_proposal", message)
            await self.agent.pubsub.publish("pubsub.localhost","counter_proposals_topic", message)
            self.agent.bdi.set_belief("is_requested_time_slot_booked", True)
        else:
            self.agent.bdi.set_belief("is_requested_time_slot_booked", False)
            