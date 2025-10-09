import aiohttp
import asyncio
import json
import base64
from typing import Dict,List,Optional
import pathlib

class AASClient:
    def __init__(self, aas_base_url="http://localhost:8081"):
        self.aas_base_url = aas_base_url

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def create_aas_from_file(self, aas_path: str):
        """Create AAS from BaSyx JSON file (extracts from container format)"""
        try: 
            with open(aas_path, "r", encoding="utf-8") as f:
                file_data = json.load(f)
        except Exception as e:
            return {"error": str(e)}
        
        # Extract AAS from BaSyx container format
        if "assetAdministrationShells" in file_data:
            if len(file_data["assetAdministrationShells"]) > 0:
                aas_data = file_data["assetAdministrationShells"][0]
            else:
                return {"error": "No AAS found"}
        else:
            aas_data = file_data
        
        async with self.session.post(
            f"{self.aas_base_url}/shells",
            json=aas_data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        ) as response:
            if response.status == 201:
                return await response.json()
            else:
                response_text = await response.text()
                return {"error": response_text, "status": response.status}

    async def create_submodel_from_file(self, sm_base_url: str, file_path: str):
        """Create submodel from BaSyx JSON file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_data = json.load(f)
        except Exception as e:
            return {"error": str(e)}
        
        # Extract submodel from BaSyx container format
        if "submodels" in file_data:
            if len(file_data["submodels"]) > 0:
                submodel_data = file_data["submodels"][0]
            else:
                return {"error": "No submodels found"}
        else:
            submodel_data = file_data
        
        async with self.session.post(
            f"{sm_base_url}/submodels",
            json=submodel_data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        ) as response:
            if response.status == 201:
                return await response.json()
            else:
                response_text = await response.text()
                return {"error": response_text, "status": response.status}

    async def get_aas_shells(self):
        async with self.session.get(f"{self.aas_base_url}/shells") as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": f"Failed to fetch AAS shells: {response.status}"}

async def main():
    async with AASClient() as client:
        file_path = pathlib.Path(__file__).parent / "AAS_Drilling_Machine.json"
        
        sm_result = await client.create_submodel_from_file("http://localhost:8081", file_path)
        aas_result = await client.create_aas_from_file(file_path)
        shells = await client.get_aas_shells()
        
        print("Results:")
        print(f"Submodel: {'✅' if 'error' not in sm_result else '❌'}")
        print(f"AAS: {'✅' if 'error' not in aas_result else '❌'}")
        if isinstance(shells, dict) and "result" in shells:
            print(f"Total AAS: {len(shells['result'])}")

if __name__ == "__main__":
    asyncio.run(main())