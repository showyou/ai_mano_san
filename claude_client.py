#BedrockのAPI呼びます

import boto3
import json

from botocore.exceptions import ClientError

class ClaudeClient:
    def __init__(self):

        self.client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Set the model ID, e.g., Claude 3 Haiku.
        self.model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

    def create(self, max_tokens, temperature, messages):

        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        # Convert the native request to JSON.
        request = json.dumps(native_request)

        try:
            # Invoke the model with the request.
            response = self.client.invoke_model(modelId=self.model_id, body=request)

        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
            return None

        # Decode the response body.
        model_response = json.loads(response["body"].read())

        # Extract and print the response text.
        response_text = model_response["content"][0]["text"]
        return response_text

