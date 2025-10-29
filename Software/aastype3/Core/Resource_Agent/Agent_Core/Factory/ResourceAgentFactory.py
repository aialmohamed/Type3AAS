from typing import Type,Callable,Dict




class ResourceAgentFactory:
    """Factory with base class support."""
    
    _registry = {}
    
    @staticmethod
    def register(resource_type: str, agent_class):
        """Register an agent class."""
        ResourceAgentFactory._registry[resource_type] = agent_class
    
    @staticmethod
    async def create_agent(resource_type: str, jid: str, password: str, asl_path: str, client=None):
        """Create an agent of the specified type."""
        if resource_type not in ResourceAgentFactory._registry:
            raise ValueError(f"Unknown resource type: {resource_type}")
        
        agent_class = ResourceAgentFactory._registry[resource_type]
        agent = agent_class(jid, password, asl_path, resource_client=client)
        return agent