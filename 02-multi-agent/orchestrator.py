import sys
import os
from datetime import datetime
from run_agent import AIAgent
from mem.store import get_memory_context, add_memory_entry

def banner(text):
    width = 60
    print(f"\n{'═' * width}")
    print(f"  {text}")
    print(f"{'═' * width}\n")

def step_log(icon, message):
    print(f"  {icon} {message}")

def create_researcher():
    return AIAgent(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        quiet_mode=True,
        enabled_toolsets=["web"],
    )

def create_writer():
    return AIAgent(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        quiet_mode=True,
        enabled_toolsets=["file"],
    )

def create_summarizer():
    return AIAgent(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        quiet_mode=True,
        enabled_toolsets=[],  
    )


def run_workflow(topic):
    banner("MULTI-AGENT WORKFLOW STARTING")
    print(f"  Topic: {topic}")
    print(f"  Time:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    banner("LOADING LONG-TERM MEMORY")
    memory_context = get_memory_context(max_entries=5)
    if memory_context:
        print(f"  Found prior knowledge:\n")
        for line in memory_context.split("\n"):
            print(f"    {line}")
    else:
        step_log("📭", "No prior memory found. This is the first run.")

    banner("RESEARCHER AGENT STARTING")
    step_log("🔬", "Creating Researcher agent (toolsets: [web])...")
    researcher = create_researcher()
    research_prompt = f"""You are a research assistant. A user wants to research: {topic}
Here is your knowledge base from previous research sessions:
{memory_context}

Search the web for:
- Recent developments and news
- Key facts and statistics
- Expert opinions and analysis
- Relevant sources and references
Provide comprehensive, detailed findings. Include specific data points and source URLs where possible.

Rules:
- If the knowledge base contains sufficient, relevant information to write 
  a thorough response, provide that response now.
- Only search the web if the knowledge base is empty, irrelevant, or lacks enough detail.
"""
    step_log("🔍", "Researching...")
    research_result = researcher.run_conversation(user_message=research_prompt)
    research_text = research_result["final_response"]
    step_log("✅", f"Research complete! ({len(research_text)} characters)")
    print(f"\n  --- Research Preview (first 300 chars) ---")
    print(f"  {research_text[:300]}...")

    banner("RESEARCHER → WRITER HANDOFF")
    step_log("📤", f"Passing {len(research_text)} chars of research to Writer agent")
    step_log("🔄", "Researcher agent context released")
    step_log("📥", "Writer agent will receive research as input")

    banner("WRITER AGENT STARTING")
    step_log("✍️ ", "Creating Writer agent (toolsets: [file])...")
    writer = create_writer()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.lower().replace(" ", "_")[:40]
    output_file = f"output/{safe_topic}_{timestamp}.md"
    write_prompt = f"""You are a professional technical writer. Based on the following research,
write a well-structured, polished article in markdown format.
## Research Findings
{research_text}
## Instructions
1. Write an engaging title
2. Start with an executive summary (2-3 sentences)
3. Organize findings into clear sections with headers
4. Include key statistics and data points
5. Add a "Sources" section at the end
6. Save the article to the file: {output_file}
7. Create the output/ directory if it doesn't exist
Make the article informative, well-organized, and ready to publish."""
    step_log("📝", "Writer is composing the article...")
    write_result = writer.run_conversation(user_message=write_prompt)
    article_text = write_result["final_response"]
    step_log("✅", f"Article complete! ({len(article_text)} characters)")
    step_log("💾", f"Saved to: {output_file}")

    banner("SUMMARIZER AGENT STARTING")
    step_log("🧠", "Creating Summarizer agent (no tools — pure reasoning)...")

    summarizer = create_summarizer()

    summarize_prompt = f"""You are a knowledge management agent. Your job is to distil
the following research and article into a structured memory entry that will be
useful for future research sessions on related topics.

## Original Research
{research_text}

## Written Article
{article_text}

## Instructions
Produce a structured summary with:
1. **Key Findings** — the 3-5 most important facts/insights discovered
2. **Data Points** — any specific numbers, statistics, dates, or metrics
3. **Sources** — key sources or references found
4. **Connections** — how this topic relates to broader themes
5. **Open Questions** — what wasn't fully answered or needs follow-up

Keep it concise but information-dense. This will be injected into future
research prompts to avoid re-discovering the same information."""

    step_log("📊", "Summarizer is distilling key insights...")
    summary_result = summarizer.run_conversation(user_message=summarize_prompt)
    memory_summary = summary_result["final_response"]

    step_log("✅", f"Summary complete! ({len(memory_summary)} characters)")


    banner("UPDATING LONG-TERM MEMORY")
    entry = add_memory_entry(
        topic=topic,
        summary=memory_summary
    )
    step_log("🧠", f"Memory entry added: {entry['topic']}")
    step_log("📊", f"Total memory entries: {len(__import__('mem.store', fromlist=['load_memory']).load_memory())}")

    banner("WORKFLOW COMPLETE")
    step_log("📄", f"Article saved to: {output_file}")
    step_log("🧠", "Long-term memory updated")
    step_log("✅", "Both agents completed successfully")
    print(f"\n{'─' * 60}")
    print(f"  ARTICLE PREVIEW")
    print(f"{'─' * 60}\n")
    print(article_text[:500])
    if len(article_text) > 500:
        print(f"\n  ... ({len(article_text) - 500} more characters)")
    print(f"\n{'─' * 60}\n")
    return research_text, article_text

def main():
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter a research topic: ").strip()
        if not topic:
            print("Error: Please provide a topic.")
            sys.exit(1)
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable not set.")
        print("Run: export OPENROUTER_API_KEY='your-key-here'")
        sys.exit(1)
    run_workflow(topic)


if __name__ == "__main__":
    main()