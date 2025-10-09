import json

import basyx
from basyx.aas import model
import basyx.aas.adapter.json as json_adapter
import basyx.aas.model.datatypes as datatypes



submodel = model.Submodel(
    id_='https://acplt.org/DrillMachine_submodel',
    id_short="DrillMachine_submodel",
    submodel_element={
        model.Property(
            id_short='MaxDrillDepth',
            value_type=datatypes.Double,
            value=1000.0,
            semantic_id=model.ExternalReference((model.Key(
                    type_=model.KeyTypes.GLOBAL_REFERENCE,
                    value='http://acplt.org/Properties/MaxDrillDepth'
                ),)
            )
        )}
)


aashell = model.AssetAdministrationShell(
  id_='https://acplt.org/ResourceAAS_DrillMachine',
  id_short='ResourceAAS_DrillMachine',
  asset_information=model.AssetInformation(global_asset_id="test",asset_kind=model.AssetKind.INSTANCE),
  submodel= {model.ModelReference.from_referable(submodel)}
)



aashell.update()

aashell_json_string = json.dumps(aashell, cls=json_adapter.json_serialization.AASToJsonEncoder)


property_json_string = json.dumps(submodel.submodel_element.get_object_by_attribute("id_short", 'MaxDrillDepth'),
                                 cls=json_adapter.json_serialization.AASToJsonEncoder)
json_string = json.dumps({'the_submodel': submodel,
                          'the_aas': aashell
                          },
                         cls=json_adapter.json_serialization.AASToJsonEncoder)
#submodel_and_aas = json.loads(json_string, cls=json_adapter.json_serialization.StrippedAASToJsonEncoder)
print(json_string)
obj_store: model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
obj_store.add(submodel)
obj_store.add(aashell)

# step 4.2: Again, make sure that the data is up-to-date
submodel.update()
aashell.update()
#data = json_adapter.json_serialization.write_aas_json_file(file="data.json", stripped=True, data=obj_store)
res = json_adapter.json_serialization.object_store_to_json(data=obj_store,encoder=json_adapter.json_serialization.AASToJsonEncoder)

print(res)
