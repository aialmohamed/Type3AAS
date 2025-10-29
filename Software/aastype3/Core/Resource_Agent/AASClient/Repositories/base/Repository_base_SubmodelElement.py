
import base64
import json
import pathlib
import re
from typing import Any, Dict, List
import aiohttp
from aastype3.Core.Resource_Agent.AASClient.Utils.Config_loader import IdConfigLoader
from basyx.aas import model
from basyx.aas.adapter.json import json_deserialization, json_serialization 
import asyncio
import basyx.aas.model.datatypes as datatypes
from urllib.parse import quote


class SubmodelElementRepositoryBase():
  def __init__(self, session: aiohttp.ClientSession):
      self._session = session
      self.loader = IdConfigLoader()
      self.loader.load_yaml()
      self.storage_path = pathlib.Path(__file__).parent / "Storage"

# region Utilities

  def _namespace_to_list(self,ns) -> List[Any]:
    """Return a plain list for basyx NamespaceSet-like objects."""
    if ns is None:
        return []
    if hasattr(ns, "values"):
        return list(ns.values())
    return list(ns)
  async def _invoke_operation_payload(self, submodel_id: str, operation_id: str, values: Any) -> Dict[str, Any]:
    """
    Build an invoke payload for an Operation.
    - values may be:
        * dict {id_short: value}
        * list/tuple [v1, v2, ...] (ordered)
        * None -> use default values from the operation input variables (var.value)
    Returns: {"inputArguments": [ { "value": { "modelType": "...", "idShort": "...", "value": ... } }, ... ] }
    """
    # fetch operation
    operation: model.Operation = await self.get_submodel_element_by_id(submodel_id, operation_id)

    # normalize NamespaceSet -> list of input variable objects
    vars_list = self._namespace_to_list(getattr(operation, "input_variable", getattr(operation, "inputVariables", None)))

    args: List[Dict[str, Any]] = []
    for idx, var in enumerate(vars_list):
      # determine idShort for the parameter
      id_short = getattr(var, "id_short", getattr(var, "idShort", None)) or f"param_{idx}"

      # decide value: dict by name > ordered list > default on var
      if isinstance(values, dict) and id_short in values:
        val = values[id_short]
      elif isinstance(values, (list, tuple)) and idx < len(values):
        val = values[idx]
      else:
        val = getattr(var, "value", None)

      # modelType: try attribute then fallback to class name (Property/Operation/etc.)
      model_type = getattr(var, "model_type", None) or getattr(var, "modelType", None) or type(var).__name__

      # build explicit argument object (registry accepts primitives too; explicit is safer)
      arg_value = {
        "modelType": model_type,
        "idShort": id_short,
        "value": val
      }

      args.append({"value": arg_value})

    payload = {"inputArguments": args}
    return payload

  def _b64url_no_pad(self, s: str) -> str:
    return base64.urlsafe_b64encode(s.encode("utf-8")).decode("ascii").rstrip("=")
      
  async def _element_exists(self, submodel_id: str, id_short_path: str) -> bool:
    """
    Check whether a submodel element (or path) already exists.
    - If id_short_path targets a nested element (contains '.' or '/'), fetch the collection
      and inspect its 'value' list for an element with the same idShort.
    - Otherwise try a direct GET on the element path.
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    # nested path? use collection inspection (more reliable)
    if "." in id_short_path or "/" in id_short_path:
      # normalize to segments and take first as collection, last as element
      segments = [seg for seg in re.split(r"[./]", id_short_path) if seg]
      collection_id = segments[0]
      target_idshort = segments[-1]
      quoted_collection = quote(collection_id, safe="")
      url = f"{self.loader.get_base_url().rstrip('/')}/submodels/{encoded_submodel_id}/submodel-elements/{quoted_collection}"
      async with self._session.get(url, headers={"Accept":"application/json"}) as resp:
        if resp.status == 404:
          return False
        resp.raise_for_status()
        data = await resp.json()
        # collection may be returned as the collection object with 'value' list
        values = None
        if isinstance(data, dict):
          if data.get("modelType") == "SubmodelElementCollection" and isinstance(data.get("value"), list):
            values = data["value"]
          elif "value" in data and isinstance(data["value"], list):
            values = data["value"]
        if not values:
          return False
        for v in values:
          if isinstance(v, dict):
            if v.get("idShort") == target_idshort or v.get("id_short") == target_idshort:
              return True
        return False

    # fallback: direct GET of full path
    quoted = "/".join(quote(seg, safe="") for seg in id_short_path.split("."))
    url = f"{self.loader.get_base_url().rstrip('/')}/submodels/{encoded_submodel_id}/submodel-elements/{quoted}"
    async with self._session.get(url, headers={"Accept": "application/json"}) as resp:
      if resp.status == 200:
        return True
      if resp.status == 404:
        return False
      text = await resp.text()
      raise Exception(f"Unexpected response checking existence: status={resp.status}, body={text}")


# endregion

# region Get Methods for Submodel Elements
  async def get_submodel_element_by_id(self, submodel_id: str, element_id: str) -> Any:
    """
    Get a submodel element by its ID.
    Args:
        submodel_id (str): The ID of the submodel.
        element_id (str): The ID of the element.

    Returns:
        Any: The submodel element, this could be a model.SubmodelElement , model.SubmodelElementCollection, or
        a simple model.Property depending on the element type. check the printed type.
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    url_element = f"{self.loader.get_base_url()}/submodels/{encoded_submodel_id}/submodel-elements/{element_id}"
    async with self._session.get(url=url_element) as resp:
        data = await resp.json()
        json_string = json.dumps(data,cls=json_serialization.AASToJsonEncoder)
        element = json.loads(json_string,cls=json_deserialization.AASFromJsonDecoder)
        print("Submodel Element Type:", type(element))
        resp.raise_for_status()
        return element

  async def get_submodel_elements_from_collection(self, submodel_id: str, collection_id: str, element_id: str) -> Any:
    """
    Get submodel elements from a model.SubmodelElementCollection by their IDs.
    Args:
        submodel_id (str): The ID of the submodel.
        collection_id (str): The ID of the collection.
        element_id (str): The ID of the element.

    Returns:
        Any: The submodel elements, simple model.Property depending on the element type. check the printed type.
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    url_collection = f"{self.loader.get_base_url()}/submodels/{encoded_submodel_id}/submodel-elements/{collection_id}.{element_id}"
    async with self._session.get(url=url_collection) as resp:
        data = await resp.json()
        json_string = json.dumps(data,cls=json_serialization.AASToJsonEncoder)
        elements = json.loads(json_string,cls=json_deserialization.AASFromJsonDecoder)
        print("Submodel Element Collection Type:", type(elements))
        resp.raise_for_status()
        return elements
    
  async def get_submodel_element_value_by_id(self, submodel_id: str, element_id: str) -> Any:
      """
      Get the value of a submodel element by its ID.
      Args:
          submodel_id (str): The ID of the submodel.
          element_id (str): The ID of the element.

      Returns:
          Any: The value of the submodel element.
      """
      encoded_submodel_id = self._b64url_no_pad(submodel_id)
      url_element = f"{self.loader.get_base_url()}/submodels/{encoded_submodel_id}/submodel-elements/{element_id}/$value"
      async with self._session.get(url=url_element) as resp:
          data = await resp.json()
          json_string = json.dumps(data,cls=json_serialization.AASToJsonEncoder)
          element = json.loads(json_string,cls=json_deserialization.AASFromJsonDecoder)
          return element

  async def get_submodel_element_value_from_collection(self, submodel_id: str, collection_id: str, element_id: str) -> Any:
      """
      Get the value of a submodel element from a model.SubmodelElementCollection by their IDs.
      Args:
          submodel_id (str): The ID of the submodel.
          collection_id (str): The ID of the collection.
          element_id (str): The ID of the element.

      Returns:
          Any: The value of the submodel element.
      """
      encoded_submodel_id = self._b64url_no_pad(submodel_id)
      url_element = f"{self.loader.get_base_url()}/submodels/{encoded_submodel_id}/submodel-elements/{collection_id}.{element_id}/$value"
      async with self._session.get(url=url_element) as resp:
          data = await resp.json()
          json_string = json.dumps(data,cls=json_serialization.AASToJsonEncoder)
          element = json.loads(json_string,cls=json_deserialization.AASFromJsonDecoder)
          print("Submodel Element Type:", type(element))
          return element
# endregion

# region Update value of Submodel Elements
  async def update_submodel_element_value_by_id(self, submodel_id: str, element_id: str, new_value: Any) -> None:
    """
    Update the value of a submodel element by its ID.
    Args:
        submodel_id (str): The ID of the submodel.
        element_id (str): The ID of the element.
        new_value (Any): The new value to set.
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    url_element = f"{self.loader.get_base_url()}/submodels/{encoded_submodel_id}/submodel-elements/{element_id}/$value"
    async with self._session.patch(url=url_element, json=new_value) as resp:
        resp.raise_for_status()

  async def update_submodel_element_value_from_collection(self, submodel_id: str, collection_id: str, element_id: str, new_value: Any) -> None:
    """
    Update the value of a submodel element from a model.SubmodelElementCollection by their IDs.
    Args:
        submodel_id (str): The ID of the submodel.
        collection_id (str): The ID of the collection.
        element_id (str): The ID of the element.
        new_value (Any): The new value to set.
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    url_element = f"{self.loader.get_base_url()}/submodels/{encoded_submodel_id}/submodel-elements/{collection_id}.{element_id}/$value"
    async with self._session.patch(url=url_element, json=new_value) as resp:
        resp.raise_for_status()

  async def invoke_operation_on_submodel_element(self, submodel_id: str, element_id: str, input_params: Dict[str, Any], Async_flag: str) -> Any:
    """
    Invoke an operation on a submodel element by its ID.
    Args:
        submodel_id (str): The ID of the submodel.
        element_id (str): The ID of the element.
        input_params (Dict[str, Any]): The input parameters for the operation.

    Returns:
        Any: The result of the operation.
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    url_element = f"{self.loader.get_base_url()}/submodels/{encoded_submodel_id}/submodel-elements/{element_id}/invoke?async={Async_flag}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    async with self._session.post(url_element, json=input_params, headers=headers) as resp:
        text = await resp.text()
        # try to parse JSON body (may be empty)
        try:
          data = json.loads(text) if text else {}
        except Exception:
          data = None

        # success statuses: return useful part if available
        if resp.status in (200, 201, 202):
          if isinstance(data, dict) and "outputArguments" in data and isinstance(data["outputArguments"], list) and len(data["outputArguments"]) > 0:
            out = data["outputArguments"][0].get("value", {})
            # value may be a dict with inner 'value' or a direct primitive
            if isinstance(out, dict):
              return out.get("value")
            return out
          return data
                # handle delegation failure (registry indicates delegation target error)
        if resp.status == 424:
          # try to return a structured error so caller can act on it
          delegation_error = None
          try:
            delegation_error = json.loads(text)
          except Exception:
            delegation_error = text
          return {
            "success": False,
            "status": 424,
            "message" : "Either the invokation server is down or not Implemented the operation.",
            "delegation_error": delegation_error
          }

        # non-success -> raise with server body for debugging
        raise Exception(f"Invoke failed: status={resp.status}, body={text}")
# endregion

# region Create a new Submodel Element
  async def create_submodel_element(self, submodel_id: str, submodel_element: Any) -> None:
    """
    Create a new submodel element.
    Args:
        submodel_id (str): The ID of the submodel.
        submodel_element (Any): The submodel element to create. this could be a model.SubmodelElement , model.SubmodelElementCollection, or
        a simple model.Property depending on the element type.
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    url_elements = f"{self.loader.get_base_url()}/submodels/{encoded_submodel_id}/submodel-elements"
    data = json.loads(json.dumps(submodel_element, cls=json_serialization.AASToJsonEncoder))
        # extract idShort to check existence (registry uses 'idShort')
    id_short = data.get("idShort") or data.get("id_short") or None
    if id_short:
      # if element is a collection or deep element, use idShort directly; for nested you can pass "Collection.Element"
      exists = await self._element_exists(submodel_id, id_short)
      if exists:
        print(f"Element with idShort '{id_short}' already exists in submodel '{submodel_id}', skipping creation.")
        return
    async with self._session.post(url=url_elements, json=data, headers={"Content-Type": "application/json", "Accept": "application/json"}) as resp:
        resp.raise_for_status()


  async def create_submodel_element_in_collection(self, submodel_id: str, collection_id: str, submodel_element: Any) -> None:
    """
    Create a new submodel element inside a model.SubmodelElementCollection (idempotent).
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    quoted_collection = quote(collection_id, safe="")
    url_elements = f"{self.loader.get_base_url().rstrip('/')}/submodels/{encoded_submodel_id}/submodel-elements/{quoted_collection}"

    # convert basyx object -> plain dict suitable for json=
    if not isinstance(submodel_element, dict):
      data = json.loads(json.dumps(submodel_element, cls=json_serialization.AASToJsonEncoder))
    else:
      data = submodel_element

    # extract idShort of the element to add
    id_short = data.get("idShort") or data.get("id_short") or None
    if id_short:
      exists = await self._element_exists(submodel_id, f"{collection_id}.{id_short}")
      if exists:
        print(f"Element with idShort '{id_short}' already exists in collection '{collection_id}' of submodel '{submodel_id}', skipping creation.")
        return

    print("POST payload to collection:", json.dumps(data, indent=2))
    async with self._session.post(url=url_elements, json=data, headers={"Content-Type": "application/json", "Accept": "application/json"}) as resp:
      # treat 200/201/204 as success
      if resp.status in (200, 201, 204):
        print(f"Created element '{id_short or '<unknown>'}' in collection '{collection_id}' (status {resp.status}).")
        return
      text = await resp.text()
      raise Exception(f"Failed to create submodel element in collection: status={resp.status}, body={text}")
# endregion

# region delete Submodel Element
  async def delete_submodel_element_by_id(self, submodel_id: str, element_id: str) -> None:
    """
    Delete a submodel element by its ID.
    Args:
        submodel_id (str): The ID of the submodel.
        element_id (str): The ID of the element to delete.
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    url_elements = f"{self.loader.get_base_url().rstrip('/')}/submodels/{encoded_submodel_id}/submodel-elements/{element_id}"
    async with self._session.delete(url=url_elements, headers={"Accept": "application/json"}) as resp:
      resp.raise_for_status()

  async def delete_submodel_element_from_collection(self, submodel_id: str, collection_id: str, element_id: str) -> None:
    """
    Delete a submodel element from a model.SubmodelElementCollection by their IDs.
    Args:
        submodel_id (str): The ID of the submodel.
        collection_id (str): The ID of the collection.
        element_id (str): The ID of the element to delete.
    """
    encoded_submodel_id = self._b64url_no_pad(submodel_id)
    url_elements = f"{self.loader.get_base_url().rstrip('/')}/submodels/{encoded_submodel_id}/submodel-elements/{collection_id}.{element_id}"
    async with self._session.delete(url=url_elements, headers={"Accept": "application/json"}) as resp:
      resp.raise_for_status()

# region Example Usage

""" 

def create_test_submodel_element() -> model.SubmodelElement:
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Properties/test_element'
            ),)
        )
        test_element = model.Property(
          id_short="Test_Element",
          value_type=datatypes.String,
          category="VARIABLE",
          value="Idle",  # Initial state could also be "Idle" , "Running" , "Error", "Done"
          semantic_id=semantic_reference
        )
        return test_element
def create_test_submodel_element_collection() -> model.SubmodelElementCollection:
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Collections/test_collection'
            ),)
        )
        test_collection = model.SubmodelElementCollection(
          id_short="Test_Collection",
          semantic_id=semantic_reference,
          value=[
              model.Property(
                  id_short="Test_Property",
                  value_type=datatypes.String,
                  category="VARIABLE",
                  value="Test Value",
                  semantic_id=semantic_reference
              ),
              model.Property(
                  id_short="Test_Property_2",
                  value_type=datatypes.String,
                  category="VARIABLE",
                  value="Test Value 2",
                  semantic_id=semantic_reference
              )
          ]
        )
        return test_collection


async def main():
    async with aiohttp.ClientSession() as session:
        repo = SubmodelElementRepositoryBase(session)
        cap_id = repo.loader.get_Capabilities_submodel_id()
        drill_method_id = repo.loader.get_Capabilities_submodel_elements()[0]
        print(drill_method_id)
        payload = await repo._invoke_operation_payload(cap_id, drill_method_id, {"Drill_Depth": 3, "Drill_Speed": 55})
        print("Invoke payload:", json.dumps(payload, indent=2))
        result = await repo.invoke_operation_on_submodel_element(cap_id, drill_method_id, payload, "false")
        # result typically contains outputArguments or a correlation id for async
        #
        #names = _namespace_to_list(result.input_variable)
        print("invoke result:", result)

        submodel_id = repo.loader.get_Interaction_submodel_id()
        # Endpoints is a model.SubmodelElementCollection
        collection_id = repo.loader.get_Interaction_submodel_elements()[0]
        # Machine_OPCUA_Endpoint is a model.Property inside the Endpoints collection
        element_id = repo.loader.get_Interaction_submodel_elements()[1]
        # replace with actual element ID
        # print(element_id)
        collection = await repo.get_submodel_element_by_id(submodel_id, collection_id)
        element = await repo.get_submodel_elements_from_collection(submodel_id, collection_id, element_id)

        operational_state_submodel_id = repo.loader.get_Operational_State_submodel_id()
        current_state_element_id = repo.loader.get_Operational_State_submodel_elements()[0]

        await repo.update_submodel_element_value_by_id(operational_state_submodel_id, current_state_element_id, "RUNNING")
        await repo.update_submodel_element_value_from_collection(submodel_id, collection_id, element_id, "opc.tcp://My:4840/freeopcua/server/")
        new_element = create_test_submodel_element()
        await repo.create_submodel_element(operational_state_submodel_id, new_element)
        new_collection = create_test_submodel_element_collection()
        await repo.create_submodel_element(operational_state_submodel_id, new_collection)
        await repo.create_submodel_element_in_collection(submodel_id, collection_id, new_element)
        await repo.delete_submodel_element_by_id(operational_state_submodel_id, "Test_Element")
        await repo.delete_submodel_element_from_collection(submodel_id, collection_id, "Test_Element")


if __name__ == "__main__":

    asyncio.run(main()) """

# endregion