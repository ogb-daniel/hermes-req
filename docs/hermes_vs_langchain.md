# Hermes Agents vs LangChain Agents: A Comparison

## Overview

|                       | Hermes Agent                        | LangChain/LangGraph            |
| --------------------- | ----------------------------------- | ------------------------------ |
| **Created by**        | Nous Research                       | LangChain Inc.                 |
| **Primary interface** | CLI + Python library                | Python library                 |
| **Philosophy**        | Batteries-included, terminal-native | Modular, composable primitives |

---

## Architecture

**Hermes Agent** uses a monolithic `AIAgent` class that encapsulates the entire agent loop — model calls, tool execution, retries, and output formatting. You instantiate one object and call `chat()` or `run_conversation()`. The agent loop handles tool calls internally and returns the final result.

```python
from run_agent import AIAgent
agent = AIAgent(model="anthropic/claude-sonnet-4.6", quiet_mode=True)
response = agent.chat("Research quantum computing")
```

**LangChain** uses a modular architecture where components (models, prompts, tools, memory) are composed via LangChain Expression Language (LCEL) or, for agents, via **LangGraph** — a state machine where each node is a processing step and edges define the flow.

```python
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(model, tools)
result = agent.invoke({"messages": [("user", "Research quantum computing")]})
```

**Key difference**: Hermes is opinionated and handles the agent loop for you. LangChain gives you the building blocks to construct your own loop.

---

## Tool Definition

| Aspect             | Hermes                                                                                                                | LangChain                                                     |
| ------------------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Built-in tools** | Rich set: `web`, `file`, `terminal`, `browser`, `vision`, `image_generation` — enabled via `enabled_toolsets=["web"]` | Minimal built-ins. Community tools via `langchain-community`  |
| **Custom tools**   | Plugin system with `SKILL.md` files, or dynamically via the agent's skill creation                                    | `@tool` decorator on Python functions, or subclass `BaseTool` |
| **Tool selection** | Whitelist/blacklist via `enabled_toolsets` / `disabled_toolsets`                                                      | Explicit list passed to `bind_tools()` or agent constructor   |
| **MCP support**    | Native via config file                                                                                                | Via `langchain-mcp-adapters` package                          |

---

## State Management

### Hermes

Hermes manages state automatically:

- **Within a session**: `MEMORY.md` file auto-updated by the agent
- **Across turns**: Pass `conversation_history` from one `run_conversation()` call to the next
- **Across sessions**: Automatic session persistence + search. External providers (Honcho, Mem0, etc.) via plugins
- **Cross-agent**: Kanban board (SQLite-backed) for multi-agent coordination

### LangChain

LangChain requires manual state management:

- **Within a session**: `ConversationBufferMemory` or `RunnableWithMessageHistory`
- **Across turns**: Manually maintain and pass a messages list
- **Across sessions**: Bring your own persistence (Redis, PostgreSQL, etc.)
- **Cross-agent**: Shared state dict in LangGraph, or external store

**Key difference**: Hermes gives you memory "for free." LangChain requires you to choose and configure your memory strategy.

---

## Multi-Agent Patterns

| Pattern                | Hermes                                                                   | LangChain                                           |
| ---------------------- | ------------------------------------------------------------------------ | --------------------------------------------------- |
| **Agent spawning**     | `delegate_task(goal=..., toolsets=[...])` — built-in subagent delegation | Define multiple nodes in LangGraph, wire with edges |
| **Parallel execution** | Up to 3 concurrent subagents (configurable)                              | Parallel branches in LangGraph                      |
| **Coordination**       | Kanban board with SQLite, or parent-child via `delegate_task`            | Shared state dict, or external message queue        |
| **Isolation**          | Subagents get fresh context — only goal/context passed in                | Nodes share the full graph state by default         |

---

## Provider Flexibility

### Hermes

- 30+ providers out of the box
- Hot-swap at any time with `hermes model`
- Supports Ollama, vLLM, and OpenAI-compatible endpoints
- Fallback provider chains
- Credential pools for load distribution

### LangChain

- One class per provider (`ChatOpenAI`, `ChatAnthropic`, `ChatOllama`)
- Universal `init_chat_model()` constructor available
- Switching providers generally requires code changes unless using `configurable_alternatives`

---

## Summary: When to Use Which

| Use Case                                      | Better Choice | Why                                                 |
| --------------------------------------------- | ------------- | --------------------------------------------------- |
| Quick autonomous agent with tools             | **Hermes**    | Zero-config tools, single `AIAgent` class           |
| Complex custom workflows with branching logic | **LangChain** | LangGraph gives fine-grained control over flow      |
| Terminal/CLI automation                       | **Hermes**    | Built for terminal-native workflows                 |
| Multi-platform bot (Telegram, Discord, Slack) | **Hermes**    | 21+ messaging platforms built in                    |
| Production pipeline with observability        | **LangChain** | LangSmith tracing and LangGraph Studio              |
| Local/self-hosted models                      | **Both**      | Hermes: Ollama/vLLM natively. LangChain: ChatOllama |
| Rapid prototyping                             | **Hermes**    | Less boilerplate to get a working agent             |
| Enterprise integration                        | **LangChain** | Larger ecosystem, more connectors                   |

---

## Conclusion

Hermes and LangChain address similar problems but with different philosophies:

- **Hermes** prioritizes simplicity, built-in capabilities, and rapid development.
- **LangChain** prioritizes flexibility, composability, and enterprise-grade workflow customization.

Choose **Hermes** when you want a working autonomous agent quickly with minimal setup. Choose **LangChain** when you need complex orchestration, extensive integrations, or highly customized agent workflows.
