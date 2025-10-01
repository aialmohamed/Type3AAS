from spade_pubsub import PubSubMixin
import slixmpp.stanza
from spade_bdi.bdi import BDIAgent
import re
import os
import asyncio


class SubscriberAgent(PubSubMixin, BDIAgent):
    async def setup(self):
        print(f"Subscriber Agent {self.jid} starting...")
        print("Subscriber Agent setup complete!")

    def my_callback(self,message):
        sender,node,content=self._filter(message)
        if self.bdi:
            print(f"📨 Received from {sender} on node '{node}': {content}")
            self.bdi.set_belief(node, content)
            print("Updated BDI belief with the latest sensor data.")
    
    def _filter(self,message):
        try:
            # Extract the sender JID
            sender = str(message['from'])
            
            # Simple approach: extract from the XML string
            message_str = str(message)
            
            # Look for the payload content

            payload_pattern = r'<payload xmlns="spade\.pubsub">([^<]+)</payload>'
            node_pattern = r'<items node="([^"]+)">'
            
            payload_match = re.search(payload_pattern, message_str)
            node_match = re.search(node_pattern, message_str)
            
            if payload_match and node_match:
                content = payload_match.group(1)
                node = node_match.group(1)
                return [sender,node,content]
            else:
                raise Exception("Could not parse payload")
        except Exception as e:
            print(f"❌ Error parsing pubsub message: {e}")
            print(f"   Raw message: {message}")
            

async def main():
    asl_path = os.path.join(os.path.dirname(__file__), "subscriber.asl")
    agent = SubscriberAgent("subscriber@localhost", "password123", asl_path)
    await agent.start(auto_register=True)
    
    try:
        # Subscribe to the sensor_data_topic
        await agent.pubsub.subscribe("pubsub.localhost", "sensor_data_topic")
        print("✅ Subscribed to sensor_data_topic")
        
        # Set the callback function
        agent.pubsub.set_on_item_published(agent.my_callback)
        print("👂 Subscriber Agent listening for messages...")
        
        await asyncio.sleep(15)  # Keep the agent running to receive messages
        
    except Exception as e:
        print(f"❌ Error in subscription: {e}")
    
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())