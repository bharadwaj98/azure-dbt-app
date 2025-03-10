# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

from dbt.cli.main import dbtRunner, dbtRunnerResult
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()

def main(input: str) -> str:
    try:
        logging.info(f"dbt called with input: {input}")
        payload = json.loads(input)
        schema = payload.get("schema", "default")
        commands = payload["commands"]
        
        # Set environment variables for dbt
        os.environ["DBT_PROFILES_DIR"] = "C:/Users/BharadwajRohanAnanda/projects/azure-dbt-app/dbt"
        os.environ["SNOWFLAKE_SCHEMA"] = schema

        # Split the commands into an array for dbtRunner
        dbt_commands = commands.split()

        dbt = dbtRunner()
        res: dbtRunnerResult = dbt.invoke(dbt_commands)

        run_result = {
            "success": str(res.success),
            "exception": str(res.exception),
        }

        return json.dumps(run_result)

    except Exception as e:
        logging.exception(e)
        return json.dumps({"success": "False", "exception": str(e)})



# DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://host.docker.internal:10000/devstoreaccount1;QueueEndpoint=http://host.docker.internal:10001/devstoreaccount1;TableEndpoint=http://host.docker.internal:10002/devstoreaccount1;