# Hermes Research Assistant

A single tool-using agent built with [Hermes Agent](https://github.com/NousResearch/hermes-agent) that demonstrates the fundamentals of the framework.

## What It Does

Given a research topic, the agent:

1. **Searches the web** for recent information (using Hermes's `web` toolset)
2. **Summarises findings** into a structured markdown article
3. **Saves the article** to a file (using Hermes's `file` toolset)

This demonstrates Hermes Agent's core capabilities:

- Tool-using agents via the `AIAgent` Python API
- Multi-turn conversations with `conversation_history`
- Built-in toolset management (`enabled_toolsets`)

## Prerequisites

- Python 3.11+
- An Anthropic API key

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENROUTER_API_KEY="your-key-here"
```

## Usage

### With a topic argument

python agent.py "quantum computing breakthroughs 2025"

### Interactive mode

python agent.py

## Output

The agent saves its research to output/<topic>\_<timestamp>.md.
