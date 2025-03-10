# This function an HTTP starter function for Durable Functions.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable activity function (default name is "Hello")
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt
 
import logging
import azure.functions as func
import azure.durable_functions as df
import json

from azure.functions import HttpRequest, HttpResponse
from azure.durable_functions import DurableOrchestrationClient
from urllib.parse import urlparse


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    
    func.HttpResponse.mimetype = "application/json"
    func.HttpResponse.charset = "utf-8"
    
    try:
        payload = req.get_json()
        function_name = req.route_params["functionName"]
        
        if not function_name:
            return func.HttpResponse(
                "Function name not provided in the route.",
                status_code=400
            )
    
        payload_str = json.dumps(payload)
        commands = payload["commands"]
        
        instance_id = await client.start_new(function_name, None, payload_str)
        logging.info(f"Started orchestration with ID = '{instance_id}'.")
        
        # Construct the base URL from the request URL
        parsed_url = urlparse(req.url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        status_uri = f"{base_url}/runtime/webhooks/durabletask/instances/{instance_id}"
        
        # Retrieve orchestration status
        status = await client.get_status(instance_id)
        
        result_payload = {
            "id": instance_id,
            "createdTime": status.created_time.isoformat() if status.created_time else None,
            "lastUpdatedTime": status.last_updated_time.isoformat() if status.last_updated_time else None,
            # "status": status.runtime_status.name if status.runtime_status else None,
            "input": payload,
            "output": status_uri
        }

        # Return the http response
        return func.HttpResponse(
            json.dumps(result_payload),
            status_code=202,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error starting orchestration: {e}")
        return func.HttpResponse(
            str(e),
            status_code=500
        )