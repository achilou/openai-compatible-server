import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000/v1"

async def test_stream_response(client, url, payload):
    """
    Test streaming API response.
    
    Args:
        client: httpx AsyncClient
        url: API endpoint URL
        payload: Request payload
    """
    print(f"\nTesting streaming {url}:")
    async with client.stream(
        "POST",
        url,
        json=payload,
        headers={"Content-Type": "application/json"}
    ) as response:
        print(f"Status: {response.status_code}")
        print("Content-Type:", response.headers["content-type"])
        
        print("\nStreaming response chunks:")
        async for chunk in response.aiter_text():
            if chunk.strip():
                print("Chunk:", chunk.strip())

async def test_with_httpx():
    """
    Main test function using httpx.
    Tests all API endpoints including streaming.
    """
    async with httpx.AsyncClient() as client:
        print("\n=== Testing with httpx ===")
        
        # Test /v1/models endpoint
        print("\nTesting /v1/models:")
        resp = await client.get(f"{BASE_URL}/models")
        print(f"Status: {resp.status_code}")
        print("Response:", json.dumps(resp.json(), indent=2))
        
        # Test non-streaming /v1/completions
        print("\nTesting /v1/completions (non-streaming):")
        payload = {
            "model": "mock-gpt",
            "prompt": "Hello, world!",
            "max_tokens": 10
        }
        resp = await client.post(
            f"{BASE_URL}/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {resp.status_code}")
        print("Response:", json.dumps(resp.json(), indent=2))
        
        # Test streaming /v1/completions
        streaming_payload = {**payload, "stream": True}
        await test_stream_response(client, f"{BASE_URL}/completions", streaming_payload)
        
        # Test non-streaming /v1/chat/completions
        print("\nTesting /v1/chat/completions (non-streaming):")
        payload = {
            "model": "mock-gpt",
            "messages": [{"role": "user", "content": "Hello!"}],
            "max_tokens": 10
        }
        resp = await client.post(
            f"{BASE_URL}/chat/completions", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {resp.status_code}")
        print("Response:", json.dumps(resp.json(), indent=2))
        
        # Test streaming /v1/chat/completions
        streaming_payload = {**payload, "stream": True}
        await test_stream_response(client, f"{BASE_URL}/chat/completions", streaming_payload)

if __name__ == "__main__":
    asyncio.run(test_with_httpx())