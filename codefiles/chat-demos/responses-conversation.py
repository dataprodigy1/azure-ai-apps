import os

from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def create_client(endpoint):
    """Create an authenticated OpenAI client."""

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default"
    )

    return OpenAI(
        base_url=endpoint,
        api_key=token_provider
    )


def get_response(client, model_name, prompt, previous_response_id=None):
    """Send a prompt using the Responses API."""

    result = client.responses.create(
        model=model_name,
        instructions="You are a helpful AI assistant that answers questions and provides information.",
        input=prompt,
        previous_response_id=previous_response_id
    )

    return result


def main():

    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    model_name = os.getenv("MODEL_DEPLOYMENT")

    try:
        client = create_client(endpoint)

        print("Responses API - Conversation Demo")
        print("Type 'quit' to exit.")

        previous_response_id = None

        while True:
            prompt = input('\nEnter a prompt (or type "quit" to exit): ')

            if prompt.lower() == "quit":
                print("Goodbye!")
                break

            if not prompt:
                print("Please enter a prompt.")
                continue

            response = get_response(
                client,
                model_name,
                prompt,
                previous_response_id
            )

            print(f"\nAssistant: {response.output_text}")

            # Save the response ID for the next turn
            previous_response_id = response.id

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()