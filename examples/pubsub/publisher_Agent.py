from spade_pubsub import PubSubMixin
from spade_bdi.bdi import BDIAgent
import os
import asyncio


class PublisherAgent(PubSubMixin, BDIAgent):
    async def setup(self):
        print(f"Publisher Agent {self.jid} starting...")
        print("Publisher Agent setup complete!")
        



async def main():
    asl_path = os.path.join(os.path.dirname(__file__), "publisher.asl")
    agent = PublisherAgent("publisher@localhost", "password123", asl_path)
    await agent.start(auto_register=True)
    
    # Create a pubsub node
    try:
        nodes = await agent.pubsub.get_nodes("pubsub.localhost")
        print(f"Existing pubsub nodes: {nodes}")
        # Extract node names from the list of dicts
        node_names = [node_dict["node"] for node_dict in nodes if "node" in node_dict]
        print(f"Node names: {node_names}")
        
        if "sensor_data_topic" not in node_names:
          await agent.pubsub.create("pubsub.localhost", "sensor_data_topic")
          print("Created pubsub node: sensor_data_topic")
        else:
          print("Pubsub node already exists: sensor_data_topic")
        
        for i in range(5):
          # Publish some test data
          await agent.pubsub.publish("pubsub.localhost", "sensor_data_topic", f"Temperature: {20 + i}°C")
          print("Published temperature data")
          await asyncio.sleep(2)  # Simulate time between readings
          await agent.pubsub.publish("pubsub.localhost", "sensor_data_topic", f"Humidity: {60 + i}%")
          print("Published humidity data")
          await asyncio.sleep(2)  # Simulate time between readings

        
    except Exception as e:
        print(f"Error in pubsub operations: {e}")
    
    print("Publisher Agent operations complete!")
    await asyncio.sleep(2)  # Give time for messages to be processed
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
