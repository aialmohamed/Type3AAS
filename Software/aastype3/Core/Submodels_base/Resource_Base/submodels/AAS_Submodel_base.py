from abc import ABC, abstractmethod
from typing import Any, Dict, List
from aastype3.Core.Submodels_base.Utils import Shell_utills
import aiohttp
from basyx.aas import model
from basyx.aas.adapter.json import json_serialization
import json 


class AASSubmodelBase(ABC):
    """
    Abstract base class for AAS Submodels.
    Defines the interface and common functionality for all Submodel implementations.
    """
    def __init__(self):
        super().__init__()
        self.__shell_utils = Shell_utills()
        self.__configs = self.__shell_utils.load_shell_config(self.__shell_utils.path)
        self.__submodels_url = self.__shell_utils.get_submodels_endpoint(self.__configs)
        self.__root_url = self.__shell_utils.get_root_url(self.__configs)
        self.__full_url = f"{self.__root_url.rstrip('/')}/{self.__submodels_url.strip('/')}"
        self.__post_header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        self._object_store : model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
        self._submodel: model.Submodel = None
        self._submodel_elements: List[model.SubmodelElement] = []
        self.create_submodel()

    @abstractmethod
    def create_submodel_elements(self):
      """
      Abstract method to create submodel elements.
      Uses self.__submodel_elements to store created elements.
      example: self.get_submodel_elements().append(your_element)
      Must be implemented by subclasses.
      """
      pass
    @abstractmethod
    def create_submodel(self):
        """
        Abstract method to create the submodel.
        Use the self.__submodel to assign the created submodel.
        example: self._submodel = model.Submodel( ... )
        Must be implemented by subclasses.
        """
        pass
    def get_submodel(self) -> model.Submodel:
        """
        Returns the created submodel.
        """
        return self._submodel
    def get_submodel_elements(self) -> List[model.SubmodelElement]:
        """
        Returns the created submodel elements.
        """
        return self._submodel_elements
    def get_full_url(self) -> str:
        """
        Returns the full URL for the submodel.
        """
        return self.full_url
    def _create_object_store(self) -> model.DictObjectStore[model.Identifiable]:
        """
        Returns the object store for the submodel.
        """
        self._submodel.update()
        self._object_store.add(self._submodel)
        return self._object_store

    async def publish_submodel(self) -> Any:
        """
        Publishes the submodel to the configured endpoint.
        """
        self._create_object_store()
        data = json_serialization.object_store_to_json(self._object_store, stripped=True, indent=4, encoder=json_serialization.AASToJsonEncoder)
        if isinstance(data, str):
            try:
                data_dict = json.loads(data)
            except json.JSONDecodeError:
                return {"error": "Failed to parse serialized AAS JSON"}
        else:
            data_dict = data
        if "submodels" in data_dict:
            if len(data_dict["submodels"]) > 0:
                submodel_data = data_dict["submodels"][0]
            else:
                return {"error": "No Submodel found"}
        else:
            submodel_data = data_dict
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.__full_url,
                json=submodel_data,
                headers=self.__post_header
            ) as response:
                if response.status == 200:
                  print("Submodel updated successfully.")
                  response = await response.json()
                  return response
                elif response.status == 409:
                  print("Submodel already exists!!")
                  response = await response.json()
                  return response
                else:
                  response_text = await response.text()
                  return {"error": response_text, "status": response.status}