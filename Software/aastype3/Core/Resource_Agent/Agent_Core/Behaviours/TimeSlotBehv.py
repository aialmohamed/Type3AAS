
import json
from spade.behaviour import OneShotBehaviour
from aastype3.Core.Datamodels.CfpPubSubMessag import CfpPubSubMessage

class TimeSlotProcessingBehaviour(OneShotBehaviour):

    async def run(self):
        self.cfp_at_time = self.agent.bdi.get_belief_value("cfp_at_time")[0]
        self.free_time_slots = self.agent.bdi.get_belief("free_time_slots",source=True)
        self.free_time_slots  = self.agent.utils.extract_belief_payload(self.free_time_slots)
        self.free_time_slots  = json.loads(self.free_time_slots)
        self.booked_time_slots  = self.agent.bdi.get_belief("booked_time_slots",source=True)
        self.booked_time_slots  = self.agent.utils.extract_belief_payload(self.booked_time_slots)
        self.booked_time_slots  = json.loads(self.booked_time_slots)
        self.agent.new_cfp_proposal.update(
            free_time_slots=self.free_time_slots,
            booked_time_slots=self.booked_time_slots,
            requested_slot=self.cfp_at_time,
        )
            