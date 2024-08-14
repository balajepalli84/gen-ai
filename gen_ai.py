import io
import json
from datetime import datetime, timedelta
import logging
import oci

compartment_id = "ocid1.compartment.oc1..aaaaaaaafklcekq7wnwrt4zxeizcrmvhltz6wxaqzwksbhbs73yz6mtpi5za"
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file("~/.oci/config")
input = "tell me about oci gen 2"

# Service endpoint
endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"

generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
chat_detail = oci.generative_ai_inference.models.ChatDetails()

chat_request = oci.generative_ai_inference.models.CohereChatRequest()
chat_request.message = input
chat_request.max_tokens = 600
chat_request.temperature = 1
chat_request.frequency_penalty = 0
chat_request.top_p = 0.75
chat_request.top_k = 0

# Initialize chat history
chat_history = []

# Add first interaction to chat history
previous_chat_message_1 = oci.generative_ai_inference.models.CohereUserMessage(message="Tell me something about Oracle.")
previous_chat_reply_1 = oci.generative_ai_inference.models.CohereChatBotMessage(message="Oracle is one of the largest vendors in the enterprise IT market and the shorthand name of its flagship product. The database software sits at the center of many corporate IT")
chat_history.extend([previous_chat_message_1, previous_chat_reply_1])

# Add second interaction to chat history
previous_chat_message_2 = oci.generative_ai_inference.models.CohereUserMessage(message="Good to hear that, I want to know about Cohere Gen AI")
previous_chat_reply_2 = oci.generative_ai_inference.models.CohereChatBotMessage(message="Cohere's Generative AI, also known as Cohere Gen AI, is a cutting-edge technology that enables machines to generate human-like responses, creative content, and various forms of textual output...")
chat_history.extend([previous_chat_message_2, previous_chat_reply_2])

# Assign the accumulated chat history to the chat request
chat_request.chat_history = chat_history

# Set chat details and make the request
chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyawk6mgunzodenakhkuwxanvt6wo3jcpf72ln52dymk4wq")
chat_detail.chat_request = chat_request
chat_detail.compartment_id = compartment_id

chat_response = generative_ai_inference_client.chat(chat_detail)

# Write the response to a file
with open(r'C:\Security\Blogs\gen-ai\logs\chat_response.txt', "a") as file:
    file.write("response:" + str(chat_response.data) + "\n")

# Print result
print("**************************Chat Result**************************", flush=True)
print(chat_response.data)
