
import pathlib
import aiohttp
import asyncio
import yaml



async def load_sm_ids_https():
    file_data = {}
    url = "http://localhost:8083/submodel-descriptors"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data.get('result', []):
                    file_data[item["displayName"][0]["text"]] = item['id']
                return file_data
            return {}

def create_yaml_file(file_data, filename="submodel_ids.yaml"):
    
    
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    config_dir = base_dir / "Config"
    config_dir.mkdir(parents=True, exist_ok=True)
    filename = str(config_dir / filename)


    with open(filename, "w", encoding="utf-8") as f:
        yaml.safe_dump({"submodel_ids": dict(file_data)}, f)

async def main():
    file_data = await load_sm_ids_https()
    print("Loaded Submodel IDs:")
    for item in file_data:
        print(item)
    create_yaml_file(file_data)
if __name__ == "__main__":
    asyncio.run(main())