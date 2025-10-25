import asyncio
import base64
from aiohttp import ClientSession

def b64url_no_pad(s: str) -> str:
    return base64.urlsafe_b64encode(s.encode("utf-8")).decode("ascii").rstrip("=")

async def main():
    identifier = "https://THU.de/RA_1_SM_Interaction"  # change to your submodel identifier (IRI or idShort)
    encoded = b64url_no_pad(identifier)
    url = f"http://localhost:8081/submodels/{encoded}"
    print("GET", url)
    async with ClientSession() as session:
        async with session.get(url, headers={"Accept":"application/json"}) as resp:
            print("status:", resp.status)
            text = await resp.text()
            print(text)

if __name__ == "__main__":
    asyncio.run(main())