# coding: utf-8
# Copyright (c) 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

##########################################################################
# cohere_generate_text_demo.py
# Supports Python 3
##########################################################################
# Info:
# Get texts from LLM model for given prompts using OCI Generative AI Service.
##########################################################################
# Application Command line(no parameter needed)
# export GENAI_REGION=us-chicago-1 && export GENAI_PROFILE=oc1 && GENAI_COMPARTMENT=compartment_ocid
# To use sesstion token
#   python test.py --st
##########################################################################
from utils import *

args = initArgs()

# Setup basic variables
# Auth Config
# TODO: Please update config profile name and use the compartmentId that has policies grant permissions for using Generative AI Service
# export GENAI_REGION=us-chicago-1 && export GENAI_STAGE=prod && export GENAI_PROFILE=oc1 && export GENAI_COMPARTMENT=compartment_ocid
region, stage, profile, compartment_id = getEnvVariables()
generative_ai_inference_client = get_generative_ai_dp_client(
    endpoint=getEndpoint(region, stage),
    profile=profile,
    use_session_token=args.st)

chat_detail = oci.generative_ai_inference.models.ChatDetails()

chat_request = oci.generative_ai_inference.models.CohereChatRequest()
chat_request.message = "Tell me something about the company's relational database."
chat_request.max_tokens = 600
chat_request.is_stream = False
chat_request.temperature = 0.75
chat_request.top_p = 0.7
chat_request.top_k = 1 # Only support topK within [0, 500]
chat_request.frequency_penalty = 1.0

previous_chat_message = oci.generative_ai_inference.models.CohereUserMessage(message="Tell me something about Oracle.")
previous_chat_reply = oci.generative_ai_inference.models.CohereChatBotMessage(message="Oracle is one of the largest vendors in the enterprise IT market and the shorthand name of its flagship product. The database software sits at the center of many corporate IT")
chat_request.chat_history = [previous_chat_message, previous_chat_reply]
chat_request.documents = [
    {
        "title": "Oracle",
        "snippet": "Oracle database services and products offer customers cost-optimized and high-performance versions of Oracle Database, the world's leading converged, multi-model database management system, as well as in-memory, NoSQL and MySQL databases. Oracle Autonomous Database, available on premises via Oracle Cloud@Customer or in the Oracle Cloud Infrastructure, enables customers to simplify relational database environments and reduce management workloads.",
        "website": "https://www.oracle.com/database"
    }
]

if "<compartment_ocid>" in compartment_id:
    print("ERROR:Please update your compartment id in target python file")
    quit()

chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="cohere.command-r-16k")
chat_detail.compartment_id = compartment_id
chat_detail.chat_request = chat_request

chat_response = generative_ai_inference_client.chat(chat_detail)

# Print result
print("**************************Chat Result**************************")
print(vars(chat_response))