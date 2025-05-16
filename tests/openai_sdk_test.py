import openai
import json

# Configure OpenAI SDK to use our local server
client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="fake-key"  # API key not required for local testing
)

def test_streaming_response(response):
    """
    Process and print streaming API response chunks.
    
    Args:
        response: Streaming response from OpenAI SDK
    """
    print("\nStreaming response chunks:")
    for chunk in response:
        print("Chunk:", json.dumps(chunk.model_dump(), indent=2))

def test_with_openai_sdk():
    """
    Main test function using OpenAI SDK.
    Tests all API endpoints including streaming.
    """
    print("\n=== Testing with OpenAI SDK ===")
    
    # Test /v1/models endpoint
    print("\nTesting /v1/models:")
    models = client.models.list()
    print("Models:", json.dumps(models.model_dump(), indent=2))
    
    # Test non-streaming /v1/completions
    print("\nTesting /v1/completions (non-streaming):")
    completion = client.completions.create(
        model="mock-gpt",
        prompt="Hello, world!",
        max_tokens=10
    )
    print("Completion:", json.dumps(completion.model_dump(), indent=2))
    
    # Test streaming /v1/completions
    print("\nTesting /v1/completions (streaming):")
    streaming_completion = client.completions.create(
        model="mock-gpt",
        prompt="Hello, world!",
        max_tokens=10,
        stream=True
    )
    test_streaming_response(streaming_completion)
    
    # Test non-streaming /v1/chat/completions
    print("\nTesting /v1/chat/completions (non-streaming):")
    chat_completion = client.chat.completions.create(
        model="mock-gpt",
        messages=[{"role": "user", "content": "Hello!"}],
        max_tokens=10
    )
    print("Chat Completion:", json.dumps(chat_completion.model_dump(), indent=2))
    
    # Test streaming /v1/chat/completions
    print("\nTesting /v1/chat/completions (streaming):")
    streaming_chat_completion = client.chat.completions.create(
        model="mock-gpt",
        messages=[{"role": "user", "content": "Hello!"}],
        max_tokens=10,
        stream=True
    )
    test_streaming_response(streaming_chat_completion)

if __name__ == "__main__":
    test_with_openai_sdk()