import asyncio
from spade_bdi.bdi import BDIAgent


class BasicAgent(BDIAgent):
    async def setup(self):
        print(f"BDI Agent {self.jid} starting...")
        print("Agent setup complete!")


async def main():
    # Get absolute path to ASL file
    import os
    asl_path = os.path.join(os.path.dirname(__file__), "basic.asl")
    print(f"Looking for ASL file at: {asl_path}")
    
    # Create agent with known credentials
    agent = BasicAgent("agent1@localhost", "password123", asl_path)
    
    try:
        # Start the agent
        await agent.start(auto_register=True)
        print("Agent started successfully!")
        
        # Wait a moment for BDI to initialize
        await asyncio.sleep(2)
        
        # Now we can safely work with BDI beliefs
        if agent.bdi:
            print("Working with BDI beliefs...")
            
            # Set beliefs
            agent.bdi.set_belief("car", "blue")
            print("Set car belief: blue, big")
            
            # Print all beliefs
            print("Current beliefs:")
            agent.bdi.print_beliefs()
            
            # Get specific belief
            car_belief = agent.bdi.get_belief("car")
            print(f"Car belief: {car_belief}")
            
            # Wait a moment
            await asyncio.sleep(2)
            
            # Remove belief
            agent.bdi.remove_belief("car", "blue", "big")
            print("Removed car belief")
            
            # Add different car belief
            agent.bdi.set_belief("car", "yellow")
            print("Set new car belief: yellow")
            
            # Print final beliefs
            print("Final beliefs:")
            agent.bdi.print_beliefs()
            
        else:
            print("BDI not initialized - check ASL file")
        
        # Keep running for a few seconds
        await asyncio.sleep(3)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await agent.stop()
        print("Agent stopped.")


if __name__ == "__main__":
    asyncio.run(main())