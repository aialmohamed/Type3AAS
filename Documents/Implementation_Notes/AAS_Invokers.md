# Aseet Adminstartion shell Implemenation Notes


## Server
In this implemenation we used the java server provided by the Eclipse Basyx project, this server provides main moduls to use such as : 

- MongoDB usage for storage of the Assets and submodles 
- Mqtt eventing upon changes , update or delets of the data
- Dockersaiztion of the server 
- REST api end points 
- Web UI to monitor the changes of the data 

## Operation Invokers workaround 

In order to use methods inside of the AAS (or better said methods shall be delegated from the AAS to Some custom Server).

First some changes needs to be done the docker compose file of the server: 

adding this line to the ```aas-env``` and the ```aas-web-ui:```

```yaml
    extra_hosts:
      - "host.docker.internal:host-gateway"
```
after that when setting the operation in the submodel we need to add qualifiers 
```python
qualifier=[model.Qualifier(
    kind=model.QualifierKind.CONCEPT_QUALIFIER,
    type_="invocationDelegation",
    value_type=datatypes.String,
    value="http://host.docker.internal:8090/drill_invocation"
)],
```
The host name is ```http://host.docker.internal:8090/``` 

- ```host.docker.internal``` must not be changed.

- ```8090``` can be set by the user.

after that the user hast to write a simple invoker code 

```python
app = FastAPI()
@app.post("/drill_invocation")
async def invoke_operation(request: Request):
    try:
        # read body (robust)
        try:
            body = await request.json()
        except Exception:
            raw = await request.body()
            body = {"_raw_body": raw.decode("utf-8", "replace")}
        logger.info("Invocation request from=%s headers=%s", getattr(request.client, "host", None), dict(request.headers))
        logger.info("Invocation body:\n%s", json.dumps(body, indent=4, ensure_ascii=False))
        properties = _opvars_to_properties(body)
        if not properties:
            raise HTTPException(status_code=400, detail="Failed to map inputs to Properties")

        # now use basyx Property objects (value may be string; cast accordingly)
        first_prop = properties[0]
        try:
            depth = float(first_prop.value)
        except Exception:
            raise HTTPException(status_code=400, detail="First input is not numeric")

        result = depth
        await asyncio.sleep(3)  # simulate processing delay
        response_var = {
            "modelType": "OperationVariable",
            "value": {
                "modelType": "Property",
                "idShort": "Drill_Result",
                "value": str(result),
                "valueType": "xs:string",
                "category": "PARAMETER",
                "displayName": [{"language": "en", "text": "Drill Result"}],
                "description": [{"language": "en", "text": "Result of the drilling operation"}]
           }
        }
        resp_json = [response_var]
        logger.info("Returning response JSON:\n%s", json.dumps(resp_json, indent=2))
        return resp_json
    except HTTPException:
        raise
    except Exception as exc:
        # log full stacktrace for debugging
        logger.exception("Unhandled exception in invoke_operation")
        # return a 500 with a short message (do NOT leak stack traces in prod)
        raise HTTPException(status_code=500, detail=f"Invoker error: {exc}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090, log_level="info")
```