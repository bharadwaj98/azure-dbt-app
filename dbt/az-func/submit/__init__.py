# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json
import azure.durable_functions as df

from azure.durable_functions import DurableOrchestrationContext, Orchestrator


def orchestrator_function(context: df.DurableOrchestrationContext):
    
    input = context.get_input()

    logging.info(f"Calling call_activity 'run' with input args: {input}")
    result = yield context.call_activity("run", input)
    logging.info("call_activity 'run' completed")
    return result


main = df.Orchestrator.create(orchestrator_function)