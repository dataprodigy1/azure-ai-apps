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


def ask_model(client, model_name, prompt):
    """Send a prompt using the Chat Completions API."""

    result = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant that answers questions and provides information."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return result.choices[0].message.content


def main():

    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    model_name = os.getenv("MODEL_DEPLOYMENT")

    try:
        client = create_client(endpoint)

        print("Chat Completions Demo")

        while True:
            prompt = input('\nEnter a prompt (or type "quit" to exit): ')

            if prompt.lower() == "quit":
                print("Goodbye!")
                break

            if not prompt:
                print("Please enter a prompt.")
                continue

            answer = ask_model(client, model_name, prompt)

            print(f"\nAssistant: {answer}")

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()