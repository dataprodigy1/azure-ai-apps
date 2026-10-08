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


def get_chat_response(client, model_name, conversation):
    """Send the conversation to the model using Chat Completions."""

    result = client.chat.completions.create(
        model=model_name,
        messages=conversation
    )

    return result.choices[0].message.content


def main():

    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    model_name = os.getenv("MODEL_DEPLOYMENT")

    try:
        client = create_client(endpoint)

        # Start the conversation with a system instruction
        conversation = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant that answers questions and provides information."
            }
        ]

        print("Chat Completions - Conversation Demo")

        while True:
            prompt = input('\nEnter a prompt (or type "quit" to exit): ')

            if prompt.lower() == "quit":
                print("Goodbye!")
                break

            if not prompt:
                print("Please enter a prompt.")
                continue

            # Add the user's message to the conversation
            conversation.append({
                "role": "user",
                "content": prompt
            })

            # Send the complete conversation to the model
            answer = get_chat_response(
                client,
                model_name,
                conversation
            )

            print(f"\nAssistant: {answer}")

            # Add the model's response to the conversation
            conversation.append({
                "role": "assistant",
                "content": answer
            })

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()