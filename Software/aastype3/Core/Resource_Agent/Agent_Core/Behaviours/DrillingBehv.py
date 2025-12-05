from spade.behaviour import OneShotBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.PublishTrackingBehv import PublishTrackingBehaviour


class DrillInvokerBehaviour(OneShotBehaviour):
    def __init__(self):
        super().__init__()

    async def run(self):
        # Publish: drill STARTED
        tracking_start = PublishTrackingBehaviour("drill", "running")
        self.agent.add_behaviour(tracking_start)
        
        input_arguments = self.agent.bdi.get_belief_value("cfp_input_arguments")
        input_arguments = self.agent.utils.to_dict(input_arguments)
        depth = float(input_arguments.get("Depth", 0))
        rpm = float(input_arguments.get("RPM", 0))
        res = await self.agent.resource_client.SubmodelElementRepositoryGetters.invoke_drill(depth, rpm)
        
        try:
            self.agent.bdi.remove_belief("drill_operation_result")
        except Exception:
            pass
        self.agent.bdi.set_belief("drill_operation_result", res)
        
        # Publish: drill COMPLETED
        tracking_done = PublishTrackingBehaviour("drill", "completed")
        self.agent.add_behaviour(tracking_done)
        
        # Signal completion
        try:
            self.agent.bdi.remove_belief("drill_completed")
        except Exception:
            pass
        self.agent.bdi.set_belief("drill_completed", True)