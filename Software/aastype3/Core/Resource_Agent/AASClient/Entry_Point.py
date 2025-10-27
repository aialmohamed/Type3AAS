import asyncio
import base64
from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
from aiohttp import ClientSession


async def main():
    async with ResourceAASClient() as client:
        mqtt_val = await client.SubmodelElementRepositoryGetters.getvalue_Interaction_MQTT_Endpoint()
        print(f"Current mqtt_val: {mqtt_val}")
        new_mqtt_val = "tcp://MyBroker.hivemq.com:1883"
        await client.SubmodelElementRepositoryUpdate.update_Interaction_MQTT_Endpoint(new_mqtt_val)
        updated_mqtt_val = await client.SubmodelElementRepositoryGetters.getvalue_Interaction_MQTT_Endpoint()
        print(f"Updated mqtt_val: {updated_mqtt_val}")
        result = await client.SubmodelElementRepositoryGetters.invoke_drill(6.0,50.0,"true")
        print(f"Drill invocation result: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 
