# Open-Weight Model Migration

This deliverable demonstrates running Hermes Agent workflows using **open-weight, self-hostable models** instead of Anthropic/Claude or any other closed-model API.

## Models Tested

| Model                     | Parameters             | Context Window | Backend            | Self-Hostable                  |
| ------------------------- | ---------------------- | -------------- | ------------------ | ------------------------------ |
| **Llama 3.2 3B**          | 3B                     | 128K tokens    | Ollama (local)     | ✅ Yes                         |
| **Phi-4 Mini**            | 3.8B                   | 128K tokens    | Ollama (local)     | ✅ Yes                         |
| **Nemotron 3 Super 120B** | 120B (12B active, MoE) | 128K tokens    | OpenRouter (cloud) | ✅ Yes (via vLLM/TensorRT-LLM) |

All three models are open-weight and can be self-hosted. The local models run via Ollama on a consumer GPU; the cloud model runs via OpenRouter for comparison but could equally be served with vLLM or TensorRT-LLM on your own infrastructure.

## Quick Start

### Local (Ollama)

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull models
./ollama_setup.sh

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run comparison
python run_comparison.py
```

### Docker

```bash
# Create .env file (optional — for OpenRouter cloud comparison)
echo "OPENROUTER_API_KEY=your-key-here" > .env

# Run everything (Ollama + models + comparison)
docker compose up --build
```

## Benchmark Results

**Test topic:** "SSM vs Encoder-Decoder architectures"  
**Hardware:** NVIDIA Quadro T2000 (4 GB VRAM) for local models  
**Date:** 2026-06-15

| Model                 | Backend            | Time (s) | Response Length | Status |
| --------------------- | ------------------ | -------- | --------------- | ------ |
| Llama 3.2 3B          | Ollama (local)     | 41.5     | 3,641 chars     | ✅     |
| Phi-4 Mini            | Ollama (local)     | 73.2     | 5,345 chars     | ✅     |
| Nemotron 3 Super 120B | OpenRouter (cloud) | 102.1    | 16,516 chars    | ✅     |

- 🏆 **Fastest:** Llama 3.2 3B (Ollama) — 41.5s
- 📝 **Most detailed:** Nemotron 3 Super 120B (OpenRouter) — 16,516 chars

## Performance Analysis

### Response Quality

| Dimension                  | Llama 3.2 3B                                                                                                                 | Phi-4 Mini                                                                                                             | Nemotron 3 Super 120B                                                                                                  |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Factual accuracy**       | ⚠️ Misinterpreted "SSM" as "Speech Synthesis Model" instead of "State Space Model" — significant factual error for the topic | ⚠️ Understood SSM correctly but explanations were somewhat garbled with formatting issues and inconsistent terminology | ✅ Highly accurate — correctly identified SSM as State Space Models, referenced S4, Mamba, Hyena, HiPPO initialisation |
| **Depth of analysis**      | Surface-level; generic advantages/disadvantages without specific technical details                                           | Moderate; attempted structured comparison but lacked specificity                                                       | Excellent; included mathematical formulations, complexity analysis (O(T) vs O(T²)), named specific papers and years    |
| **Structure & formatting** | Clean markdown, well-organised sections                                                                                      | Attempted tables but messy formatting; some markdown issues                                                            | Professional-grade markdown with rich tables, timeline, and TL;DR summary                                              |
| **Technical references**   | Mentioned Wav2Vec, GPT vaguely — no papers or dates                                                                          | Mentioned GPT-NeoX, Transformer XL — limited context                                                                   | Referenced 8+ specific papers with years (Gu et al. ICML 2022, Mamba ICML 2023, etc.)                                  |
| **Actionable insights**    | Generic future trends                                                                                                        | Generic future trends                                                                                                  | Detailed roadmap: short-term (1-2 yr), mid-term (3-5 yr), long-term (5+ yr) predictions                                |

### Speed vs Quality Tradeoff

```
Quality  ▲
         │                              ★ Nemotron 120B (cloud)
         │                                102.1s, 16,516 chars
         │
         │
         │          ★ Phi-4 Mini (local)
         │            73.2s, 5,345 chars
         │
         │  ★ Llama 3.2 3B (local)
         │    41.5s, 3,641 chars
         │
         └──────────────────────────────────────► Time
              40s        70s        100s
```

### Local (Ollama) vs Cloud (OpenRouter)

| Dimension           | Ollama (Local)                                                     | OpenRouter (Cloud)                                               |
| ------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------- |
| **Latency**         | 41-73s (GPU-bound)                                                 | 102s (network + inference)                                       |
| **Cost**            | Free (electricity only)                                            | Free tier used (Nemotron :free); paid tiers ~$0.05-0.20/M tokens |
| **Privacy**         | ✅ Data never leaves your machine                                  | ⚠️ Data sent to third-party API                                  |
| **Model size**      | Limited by local VRAM (3-4B params on 4GB GPU)                     | No limit — can run 120B+ parameter models                        |
| **Quality**         | Adequate for simple tasks; struggles with nuanced technical topics | Significantly better reasoning, accuracy, and depth              |
| **Reliability**     | Depends on your hardware                                           | 99.9% uptime SLA                                                 |
| **Setup**           | Install Ollama + pull models (~2-5 GB each)                        | Just set an API key                                              |
| **Offline capable** | ✅ Yes                                                             | ❌ No                                                            |

### Key Takeaways

1. **Model size matters more than speed.** The 120B model took 2.5× longer but produced 4.5× more content with dramatically better accuracy and depth.

2. **Small local models can hallucinate on technical topics.** Llama 3.2 3B misidentified "SSM" entirely — a critical factual error that would be unacceptable in production. Larger models are much more reliable for domain-specific knowledge.

3. **Local models are viable for simple tasks.** For straightforward questions, summarisation, or tasks where you can verify the output, 3B models running locally are fast, free, and private.

4. **Hybrid approach is recommended.** Use local models for development/testing and privacy-sensitive tasks; use cloud endpoints for production quality and complex reasoning.

## Architecture

Hermes Agent makes model switching trivial — just change the model string:

```python
# Ollama (local)
agent = AIAgent(model="ollama/llama3.2:3b", quiet_mode=True)

# OpenRouter (cloud)
agent = AIAgent(model="nvidia/nemotron-3-super-120b-a12b:free", quiet_mode=True)
```

No other code changes needed — Hermes handles provider routing, API format differences, and authentication automatically.

## When to Use Which

| Use Case                     | Recommended Model                | Why                                                  |
| ---------------------------- | -------------------------------- | ---------------------------------------------------- |
| Local development & testing  | Llama 3.2 3B (Ollama)            | Fastest, free, good enough for iteration             |
| Code-related tasks           | Phi-4 Mini (Ollama)              | Microsoft's model has strong code training data      |
| Complex research & reasoning | Nemotron 120B (OpenRouter)       | Best quality, worth the latency for important output |
| Privacy-sensitive workloads  | Either Ollama model              | Data stays on your machine                           |
| Production deployment        | Cloud endpoint (OpenRouter/vLLM) | Reliable, scalable, best quality                     |

## File Structure

```
03-open-weight-models/
├── README.md                  # This file
├── requirements.txt           # Hermes Agent dependency
├── ollama_setup.sh            # Pull local models
├── run_comparison.py          # Benchmark script
├── Dockerfile                 # Container image
├── docker-compose.yml         # Ollama + agent orchestration
└── output/
    └── comparison.md          # Full benchmark results with detailed responses
```
