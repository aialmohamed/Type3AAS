
from spade.behaviour import OneShotBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.PublishTrackingBehv import PublishTrackingBehaviour

class MoveXYInvokerBehaviour(OneShotBehaviour):
    def __init__(self):
        super().__init__()

    async def run(self):
        # Publish: move_xy STARTED
        tracking_start = PublishTrackingBehaviour("move_xy", "running")
        self.agent.add_behaviour(tracking_start)
        
        input_arguments = self.agent.bdi.get_belief_value("cfp_input_arguments")
        input_arguments = self.agent.utils.to_dict(input_arguments)
        x = float(input_arguments.get("X", 0))
        y = float(input_arguments.get("Y", 0))
        res = await self.agent.resource_client.SubmodelElementRepositoryGetters.invoke_move_xy(x, y)
        
        try:
            self.agent.bdi.remove_belief("move_xy_operation_result")
        except Exception:
            pass
        self.agent.bdi.set_belief("move_xy_operation_result", res)
        
        # Publish: move_xy COMPLETED
        tracking_done = PublishTrackingBehaviour("move_xy", "completed")
        self.agent.add_behaviour(tracking_done)
        
        # Signal completion
        try:
            self.agent.bdi.remove_belief("move_xy_completed")
        except Exception:
            pass
        self.agent.bdi.set_belief("move_xy_completed", True)
