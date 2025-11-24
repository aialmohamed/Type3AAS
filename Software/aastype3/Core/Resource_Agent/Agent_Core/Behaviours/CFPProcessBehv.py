

from spade.behaviour import OneShotBehaviour
from aastype3.Core.Resource_Agent.Datamodels.Violation_Enum import ViolationEnum





class CFPProcessingBehaviour(OneShotBehaviour):
    async def on_start(self):
        self.agent.cfp_not_valid_message = []
        self.violation_flag = False
        self.violation_Idle_flag = False
        self.violation_skill_flag = False
        self.violation_constraint_not_found_flag = False
        self.violation_constraint_flag = False
        self.skipping_constraint_check_flag = False


    async def run(self):
        input_arguments = self.agent.bdi.get_belief("cfp_input_arguments",source=True)
        input_arguments = self.agent.utils.extract_belief_payload(input_arguments)
        input_arguments = self.agent.utils.to_dict(input_arguments)

        cfp_skills = self.agent.bdi.get_belief_value("cfp_skill")[0]

        try:
            current_state = self.agent.bdi.get_belief_value("current_state")[0]
            allowed_states = ["Idle","Free"]

            # 1 - check state :
            if current_state not in allowed_states:
                self.agent.cfp_not_valid_message.append(ViolationEnum.RESOURCE_NOT_IN_IDLE_FREE_VIOLATION.name)
                self.violation_Idle_flag = True
                
            else :
                self.violation_Idle_flag = False
            # 2- check matching skills 
            resource_skills = self.agent.bdi.get_belief_value("supported_skills")
            if cfp_skills not in resource_skills:
                self.violation_skill_flag = True
                self.agent.cfp_not_valid_message.append(ViolationEnum.SKILL_MISMATCH_VIOLATION.name)
            else :
                self.violation_skill_flag = False
            # 3 - check input arguments within constraints
            constraint_types = self.agent.bdi.get_belief_value("skills_constraints_types")[0]
            constraints = list(self.agent.bdi.get_belief_value("skills_constraints"))
            
            if not constraint_types in input_arguments.keys():
                self.violation_constraint_not_found_flag = True
                self.agent.cfp_not_valid_message.append(ViolationEnum.CONSTRAINT_NOT_FOUND_VIOLATION.name)
            else :
                self.violation_constraint_not_found_flag = False
            # check the value of the input that we match to the contraint if the constraint type found
            if  constraint_types in input_arguments.keys():
                tageted_input = input_arguments[constraint_types] 
                min_constraint, max_constraint = map(float, sorted(constraints))
                tageted_input = float(tageted_input)
                if not (min_constraint <= tageted_input <= max_constraint):
                    self.violation_constraint_flag = True
                    self.agent.cfp_not_valid_message.append(ViolationEnum.CONSTRAINT_VIOLATION.name)
                else :
                    self.violation_constraint_flag = False
            else:
                self.skipping_constraint_check_flag = True
                self.agent.cfp_not_valid_message.append(ViolationEnum.SKIPPING_CONSTRAINT_CHECK_VIOLATION.name)
            # finaly set the belief
            if (self.violation_Idle_flag or self.violation_skill_flag or 
                self.violation_constraint_not_found_flag or self.violation_constraint_flag or
                self.skipping_constraint_check_flag):
                self.violation_flag = True
            else:
                self.violation_flag = False

            self.agent.bdi.set_belief("is_cfp_valid", not self.violation_flag)

        except Exception as e:
            print(f"Error processing CFP: {e}")