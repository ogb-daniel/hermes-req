import sys
import os
import time
from datetime import datetime
from run_agent import AIAgent

MODELS = {
    "Llama 3.2 3B (Ollama)": {
        "model": "ollama/llama3.2:3b",
     "provider": "ollama",
        "requires_key": False,    },
    "Qwen 2.5 3B (Ollama)": {
        "model": "ollama/qwen2.5:3b",
     "provider": "ollama",
        "requires_key": False,    },
    "Nvidia Neomotron 3 Super 120B (OpenRouter)": {
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
"provider": "openrouter",
        "requires_key": True,    },

}

def banner(text):
    width = 60
    print(f"\n{'═' * width}")
    print(f"  {text}")
    print(f"{'═' * width}\n")

def run_model(model_name, model_config, prompt):
    print(f" Running: {model_name}...")
    if model_config["requires_key"] and not os.environ.get("OPENROUTER_API_KEY"):
        print(f" Skipped (no OPENROUTER_API_KEY set)")
        return None
    try:
        agent = AIAgent(
            model=model_config["model"],
            quiet_mode=True,
            enabled_toolsets=["web"],  # Pure reasoning — no tools for fair comparison
        )
        start_time = time.time()
        result = agent.run_conversation(user_message=prompt)
        elapsed = time.time() - start_time
        response = result["final_response"]
        print(f"  ✅ Done in {elapsed:.1f}s ({len(response)} chars)")
        return {
            "model": model_name,
            "provider": model_config["provider"],
            "time_seconds": round(elapsed, 1),
            "response_length": len(response),
            "response": response,
        }
    except Exception as e:
        print(f" Failed: {e}")
        return {
            "model": model_name,
            "provider": model_config["provider"],
            "time_seconds": -1,
            "response_length": 0,
            "response": f"ERROR: {e}",
        }

def format_comparison_table(results):
    lines = [
        "| Model | Provider | Time (s) | Response Length | Status |",
        "|-------|----------|----------|----------------|--------|",
    ]
    for r in results:
        if r is None:
            continue
        status = "✅" if r["time_seconds"] > 0 else "❌"
        lines.append(
            f"| {r['model']} | {r['provider']} | {r['time_seconds']} | {r['response_length']} | {status} |"
        )
    return "\n".join(lines)

def save_comparison(results, topic, output_path="output/comparison.md"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(f"# Open-Weight Model Comparison\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Topic:** {topic}\n\n")
        f.write("## Performance Summary\n\n")
        f.write(format_comparison_table(results))
        f.write("\n\n")
        f.write("## Detailed Responses\n\n")
        for r in results:
            if r is None:
                continue
            f.write(f"### {r['model']} ({r['provider']})\n\n")
            f.write(f"**Time:** {r['time_seconds']}s | **Length:** {r['response_length']} chars\n\n")
            f.write(r["response"])
            f.write("\n\n---\n\n")
    print(f" Comparison saved to: {output_path}")

def main():
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "Explain the key differences between transformer and mamba architectures for language models"
    prompt = f"""Research and explain the following topic in detail:
{topic}
Provide:
1. A clear explanation of the core concepts
2. Key advantages and disadvantages
3. Real-world applications and examples
4. Recent developments
5. Your assessment of future trends
Be thorough and include specific technical details."""
    banner("OPEN-WEIGHT MODEL COMPARISON")
    print(f"  Topic: {topic}")
    print(f"  Models: {len(MODELS)}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    results = []
    for name, config in MODELS.items():
        banner(f"TESTING: {name}")
        result = run_model(name, config, prompt)
        results.append(result)
    valid_results = [r for r in results if r is not None]
    banner("COMPARISON RESULTS")
    print(format_comparison_table(valid_results))
    successful = [r for r in valid_results if r["time_seconds"] > 0]
    if successful:
        fastest = min(successful, key=lambda r: r["time_seconds"])
        longest = max(successful, key=lambda r: r["response_length"])
        print(f"\n  🏆 Fastest: {fastest['model']} ({fastest['time_seconds']}s)")
        print(f"  📝 Most detailed: {longest['model']} ({longest['response_length']} chars)")
    save_comparison(valid_results, topic)
    banner("DONE")

if __name__ == "__main__":
    main()
