# Multi-Agent Workflow: Researcher → Writer

A 2-agent collaborative workflow built with [Hermes Agent](https://github.com/NousResearch/hermes-agent) demonstrating agent handoff and long-term memory.

## Architecture

Researcher Agent (web search) → Writer Agent (file writing) ↕ ↕ Long-Term Memory (JSON file, persists across runs)

### Agents

| Agent          | Toolsets | Role                                                     |
| -------------- | -------- | -------------------------------------------------------- |
| **Researcher** | `web`    | Searches the web for information on the given topic      |
| **Writer**     | `file`   | Turns research findings into a polished markdown article |
| **Summarizer** | ``       | Summarizes findings                                      |

### Handoff

1. The Researcher agent searches the web and produces detailed findings
2. The orchestrator passes those findings to the Writer agent
3. The Writer composes a structured article and saves it to `output/`
4. Both agents' work is summarised and stored in long-term memory

### Long-Term Memory

- Stored in `memory/conversation_log.json`
- Each run saves: topic, research summary, article preview, timestamp
- On subsequent runs, the last 5 entries are injected into the Researcher's prompt
- This allows the agents to build on previous sessions

## Prerequisites

- Python 3.11+
- An Anthropic API key
- Docker & Docker Compose (for containerised run)

## Setup

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY="your-key-here"
```

## Usage

### Local

```bash
# With a topic argument
python orchestrator.py "artificial intelligence in healthcare"

# Interactive mode
python orchestrator.py

# Run again to see memory in action
python orchestrator.py "AI drug discovery"
```

### Docker

```bash
# Create a .env file with your API key
echo "OPENROUTER_API_KEY=your-key-here" > .env

# Build and run
docker compose run multi-agent python orchestrator.py "quantum computing 2025"

# Run again — memory persists via the volume mount
docker compose run multi-agent python orchestrator.py "quantum error correction"

```

## Output

Articles are saved to output/<topic>\_<timestamp>.md
Memory is persisted in mem/conversation_log.json
