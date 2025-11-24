
from spade.behaviour import OneShotBehaviour

class DrillInvokerBehaviour(OneShotBehaviour):
    def __init__(self):
        super().__init__()

    async def run(self):
        # grab depth and rpm from beliefs from input arguments
        input_arguments = self.agent.bdi.get_belief_value("cfp_input_arguments")
        input_arguments = self.agent.utils.to_dict(input_arguments)
        depth = float(input_arguments.get("Depth", 0))
        rpm = float(input_arguments.get("RPM", 0))
        res = await self.agent.resource_client.SubmodelElementRepositoryGetters.invoke_drill( depth, rpm)
        # update the resulte belief
        try:
            self.agent.bdi.remove_belief("drill_operation_result")
        except Exception:
            pass
        self.agent.bdi.set_belief("drill_operation_result", res)