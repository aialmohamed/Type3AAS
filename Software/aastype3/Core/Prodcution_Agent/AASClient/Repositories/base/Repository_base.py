
import base64
import json
import pathlib
from typing import Any, Dict, List
import aiohttp
from aastype3.Core.Prodcution_Agent.AASClient.Utils.Config_loader import IdConfigLoader
from basyx.aas import model
from basyx.aas.adapter.json import json_deserialization, json_serialization 




class RepositoryBase():
  def __init__(self, session: aiohttp.ClientSession,prefix: str = ""):
      self._session = session
      self.prefix = prefix
      self.loader = IdConfigLoader()
      self.loader.load_yaml()
      self.storage_path = pathlib.Path(__file__).parent / "Storage"


# region Utilities
  async def add_submodel_to_shell(self,shell_id: str, submodel: model.Submodel) -> model.AssetAdministrationShell:
    """
    Add a submodel reference to an existing shell.
    Args:
        shell_id (str): The ID of the shell to update.
        submodel (model.Submodel): The submodel to add.
    Returns:
        model.AssetAdministrationShell: The updated shell with the added submodel reference.
    """
    shell = await self.get_shell_by_id(shell_id)
    # Add the submodel reference to the shell
    shell.submodel.add(model.ModelReference.from_referable(submodel))
    shell.update()
    await self._update_shell_by_id(shell)
    return shell
  
  async def get_shell_by_id(self, shell_id: str) -> model.AssetAdministrationShell:
    """
    Retrieve an Asset Administration Shell by its ID.
    Args:
        shell_id (str): The ID of the shell to retrieve.
    Returns:
        model.AssetAdministrationShell: The retrieved shell.
    """
    encoded_shell_id = self._b64url_no_pad(shell_id)
    url_shell = f"{self.loader.get_base_url()}/shells/{encoded_shell_id}"
    async with self._session.get(url=url_shell) as resp:
        data = await resp.json()
        json_string = json.dumps(data,cls=json_serialization.AASToJsonEncoder)
        shell = json.loads(json_string,cls=json_deserialization.AASFromJsonDecoder)
        resp.raise_for_status()
        return shell
      

  async def _update_shell_by_id(self, shell: model.AssetAdministrationShell) -> Any:
    """_summary_
    Update an existing Asset Administration Shell by its ID.
    Args:
        shell (model.AssetAdministrationShell): The shell to update.
    Returns:
        Any:  The response from the update operation.
    """
    encoded_shell_id = self._b64url_no_pad(shell.id)
    print(f"Shell ID: {encoded_shell_id}")
    url_shell = f"{self.loader.get_base_url()}/shells/{encoded_shell_id}"
    shell.update()
    object_store : model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
    object_store.add(shell)
    shell_as_json_raw = json_serialization.object_store_to_json(object_store,stripped=True,encoder=json_serialization.AASToJsonEncoder)
    shell_json = self.__parse_shell_for_update_create(shell_as_json_raw)
    async with self._session.put(url_shell, json=shell_json, headers={"Content-Type": "application/json", "Accept": "application/json"}) as resp:
      resp.raise_for_status()
      if resp.status == 200:
        print("Shell updated successfully.")
      else:
          print(f"Unexpected response status: {resp.status}")

  def _b64url_no_pad(self, s: str) -> str:
    return base64.urlsafe_b64encode(s.encode("utf-8")).decode("ascii").rstrip("=")
  
  def __parse_submodel_for_update_create(self, submodel_as_json_raw: Any) -> Dict[str, Any]:
    if isinstance(submodel_as_json_raw, str):
            try:
                data_dict = json.loads(submodel_as_json_raw)
            except json.JSONDecodeError:
                return {"error": "Failed to parse serialized AAS JSON"}
    else:
      data_dict = submodel_as_json_raw
    if "submodels" in data_dict:
        if len(data_dict["submodels"]) > 0:
            submodel_json = data_dict["submodels"][0]
        else:
            print({"error": "No Submodel found"})
    else:
      submodel_json = data_dict
    return submodel_json

  def __parse_shell_for_update_create(self, shell_raw: Any) -> Dict[str, Any]:
    if isinstance(shell_raw, str):
            try:
                data_dict = json.loads(shell_raw)
            except json.JSONDecodeError:
                return {"error": "Failed to parse serialized AAS JSON"}
    else:
      data_dict = shell_raw
    if "assetAdministrationShells" in data_dict:
        if len(data_dict["assetAdministrationShells"]) > 0:
            shell_json = data_dict["assetAdministrationShells"][0]
        else:
            print({"error": "No Asset Administration Shell found"})
    else:
      shell_json = data_dict
    return shell_json
# endregion

# region main CRUD operations

  async def get_submodel_by_identifier(self, identifier: str) -> model.Submodel:
    """
        Retrieve a submodel by its identifier.
    Args:
        identifier (str): The identifier of the submodel to retrieve.

    Returns:
        model.Submodel: The retrieved submodel.
    """
    encoded_id = self._b64url_no_pad(identifier)
    url = f"{self.loader.get_base_url()}/submodels/{encoded_id}"
    async with self._session.get(url, headers={"Accept": "application/json"}) as resp:
        data = await resp.json()
        submodel = json.loads(json.dumps(data,cls=json_serialization.AASToJsonEncoder),cls=json_deserialization.AASFromJsonDecoder)
        resp.raise_for_status()
        return submodel

  async def update_submodel_by_identifier(self, identifier: str, submodel_data: model.Submodel) -> Any:
    """
    Update a submodel by its identifier.
    Args:
        identifier (str): The identifier of the submodel to update.
        submodel_data (model.Submodel): The updated submodel data.

    Returns:
        Any: The response from the update operation.
    """
    encoded_id = self._b64url_no_pad(identifier)
    url = f"{self.loader.get_base_url()}/submodels/{encoded_id}"
    object_store : model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
    submodel_data.update()
    object_store.add(submodel_data)
    submodel_as_json_raw = json_serialization.object_store_to_json(object_store, stripped=True, indent=4, encoder=json_serialization.AASToJsonEncoder)
    submodel_json = self.__parse_submodel_for_update_create(submodel_as_json_raw)
    async with self._session.put(url, json=submodel_json, headers={"Content-Type": "application/json", "Accept": "application/json"}) as resp:
        if resp.status == 204:
            return None
        else:
           return {"error": await resp.text(), "status": resp.status, "content_type": resp.headers.get("Content-Type", "")}



  async def create_submodel_base(self, submodel_data: model.Submodel) -> Any:
    url = f"{self.loader.get_base_url()}/submodels"
    object_store : model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
    print(self._b64url_no_pad(self.loader.get_shell_id()))
    submodel_data.update()
    object_store.add(submodel_data)
    submodel_as_json_raw = json_serialization.object_store_to_json(object_store, stripped=True, indent=4, encoder=json_serialization.AASToJsonEncoder)
    submodel_json = self.__parse_submodel_for_update_create(submodel_as_json_raw)
    async with self._session.post(url, json=submodel_json, headers={"Content-Type": "application/json", "Accept": "application/json"}) as resp:
        if resp.status == 409:
            print("Submodel already exists.")
        elif resp.status == 201:
            print("Submodel created successfully.")
        else:
            print(f"Unexpected response status: {resp.status}")
            resp.raise_for_status()
        return resp.status

  async def delete_submodel_by_identifier_base(self, identifier: str) -> Any:
    """Delete a submodel by its identifier.

    Args:
        identifier (str): The identifier of the submodel to delete.

    Returns:
        Any: The response from the delete operation.
    """
    # Delete the submodel from the shell first
    target_sm = await self.get_submodel_by_identifier(identifier)
    if not target_sm:
        print(f"Submodel with identifier {identifier} not found.")
        return
    shell = await self.get_shell_by_id(self.loader.get_shell_id())
    shell.submodel.remove(model.ModelReference.from_referable(target_sm))
    shell.update()
    await self._update_shell_by_id(shell)
    encoded_id = self._b64url_no_pad(identifier)
    url = f"{self.loader.get_base_url()}/submodels/{encoded_id}"
    # Now delete the submodel itself
    async with self._session.delete(url) as resp:
        if resp.status == 200 or resp.status == 204:
            print("Submodel deleted successfully.")
            return resp.status
        else:
            print(f"Failed to delete submodel. Status code: {resp.status}")
            resp.raise_for_status()

# endregion