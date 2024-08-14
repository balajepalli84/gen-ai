import io
import json
from datetime import datetime, timedelta
import logging
import oci
from fdk import response

def handler(ctx, data: io.BytesIO=None):
    raw_data = data.getvalue()
    print(f"Raw data received: {raw_data}", flush=True)
    try:
        logs = json.loads(raw_data)
        print(f"Values are {logs}", flush=True)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}", flush=True)
        logs = None
    
    compartment_id = "ocid1.compartment.oc1..aaaaaaaafklcekq7wnwrt4zxeizcrmvhltz6wxaqzwksbhbs73yz6mtpi5za"
    CONFIG_PROFILE = "DEFAULT"
    config = {}
    input="Hello, How are you?"
    signer = oci.auth.signers.get_resource_principals_signer()
    # Service endpoint
    endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"

    generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config,signer=signer, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
    chat_detail = oci.generative_ai_inference.models.ChatDetails()

    chat_request = oci.generative_ai_inference.models.CohereChatRequest()
    chat_request.message = "{input}"
    chat_request.max_tokens = 600
    chat_request.temperature = 1
    chat_request.frequency_penalty = 0
    chat_request.top_p = 0.75
    chat_request.top_k = 0


    chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyawk6mgunzodenakhkuwxanvt6wo3jcpf72ln52dymk4wq")
    chat_detail.chat_request = chat_request
    chat_detail.compartment_id = compartment_id
    chat_response = generative_ai_inference_client.chat(chat_detail)
    # Print result
    print("**************************Chat Result**************************",flush=True)
    print(vars(chat_response,flush=True))
