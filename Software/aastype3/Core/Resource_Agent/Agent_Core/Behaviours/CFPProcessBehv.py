

from aastype3.Core.Datamodels.NegotiationMessage import NegotiationMessage
from spade.behaviour import OneShotBehaviour
from aastype3.Core.Datamodels.Violation_Enum import ViolationEnum





class CFPProcessingBehaviour(OneShotBehaviour):
    async def on_start(self):
        self.agent.cfp_not_valid_message = []

    async def run(self):
        input_arguments = self.agent.bdi.get_belief("cfp_input_arguments", source=True)
        input_arguments = self.agent.utils.extract_belief_payload(input_arguments)
        input_arguments = self.agent.utils.to_dict(input_arguments)

        cfp_skills = self.agent.bdi.get_belief_value("cfp_skill")[0]

        try:
            current_state = self.agent.bdi.get_belief_value("current_state")[0]
            allowed_states = ["Idle", "Free"]

            if current_state not in allowed_states:
                self.agent.cfp_not_valid_message.append(ViolationEnum.RESOURCE_NOT_IN_IDLE_FREE_VIOLATION.name)

            resource_skills = self.agent.bdi.get_belief_value("supported_skills")
            if cfp_skills not in resource_skills:
                self.agent.cfp_not_valid_message.append(ViolationEnum.SKILL_MISMATCH_VIOLATION.name)

            constraint_types = self.agent.bdi.get_belief_value("skills_constraints_types")[0]
            constraints = list(self.agent.bdi.get_belief_value("skills_constraints"))

            if constraint_types not in input_arguments:
                self.agent.cfp_not_valid_message.append(ViolationEnum.CONSTRAINT_NOT_FOUND_VIOLATION.name)
            else:
                targeted_input = float(input_arguments[constraint_types])
                min_constraint, max_constraint = map(float, sorted(constraints))
                if not (min_constraint <= targeted_input <= max_constraint):
                    self.agent.cfp_not_valid_message.append(ViolationEnum.CONSTRAINT_VIOLATION.name)
            if constraint_types not in input_arguments:
                self.agent.cfp_not_valid_message.append(ViolationEnum.SKIPPING_CONSTRAINT_CHECK_VIOLATION.name)

            violations = self.agent.cfp_not_valid_message
            self.agent.new_cfp_proposal.violations = violations
            print(f"CFP Processing Violations: {self.agent.new_cfp_proposal.create_message_to_publish()}")
            self.agent.bdi.set_belief("is_negotiation_message_ready", True)

        except Exception as e:
            print(f"Error processing CFP: {e}")