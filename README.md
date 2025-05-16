# OpenAI Compatible Server

An OpenAI API-compatible server implementation supporting completions, chat completions and models endpoints.

## Acknowledgments
This project was generated with [Tencent CodeBuddy Craft](https://copilot.tencent.com/).

## Features

- Supports three endpoints: `/v1/completions`, `/v1/chat/completions`, `/v1/models`
- Supports both streaming and non-streaming responses
- Allows custom LLM implementations
- Dynamically routes requests to different LLM instances based on model parameter
- Includes default MockLLM for testing

## Installation

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (Recommended package manager)

### Installation Steps

```bash
# Clone repository
git clone https://github.com/yourusername/openai-compatible-server.git
cd openai-compatible-server

# Install dependencies using uv
uv sync
```

## Usage

### Start Server

```bash
uv run main.py
```

Server starts at `http://localhost:8000` by default.

### API Endpoints

#### 1. List Models

```bash
curl http://localhost:8000/v1/models
```

#### 2. Text Completion

```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock-gpt",
    "prompt": "Hello, world!",
    "max_tokens": 50
  }'
```

#### 3. Chat Completion

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock-gpt",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Streaming Responses

Add `stream: true` parameter for streaming responses:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock-gpt",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "stream": true
  }'
```
## Custom LLM Implementation

To add custom LLM implementation:

1. Create class inheriting from `BaseLLM`
2. Implement all abstract methods
3. Register implementation using `LLMFactory.register()`

Example:

```python
from app.core.llm.base import BaseLLM
from app.core.llm.factory import LLMFactory

class CustomLLM(BaseLLM):
    # Implement abstract methods
    ...

# Register custom LLM
LLMFactory.register("custom-model", CustomLLM)
```

## Configuration

Configure via environment variables or `.env` file:

```
# API config
API_V1_STR=/v1

# Server config
HOST=0.0.0.0
PORT=8000

# CORS config
CORS_ORIGINS=*

# Logging config
LOG_LEVEL=INFO
```

## License

MIT