import sys
import os
from datetime import datetime


def create_agent():
    from run_agent import AIAgent

    agent = AIAgent(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        quiet_mode=True,
        enabled_toolsets=["web", "file"],
    )
    return agent

def run_research(agent, topic):
    print(f"\n{'═' * 60}")
    print(f"  HERMES RESEARCH ASSISTANT")
    print(f"  Topic: {topic}")
    print(f"{'═' * 60}\n")

    print("Step 1/3: Researching topic...\n")
    research_result = agent.run_conversation(
        user_message=(
             f"Research the following topic thoroughly using web search: {topic}\n\n"
            f"Search for recent information, key developments, and expert opinions. "
            f"Provide detailed findings with sources."
        )
    )
    research_text = research_result['final_response']
    history = research_result["messages"]
    print(f"Research complete ({len(research_text)} chars)\n")

    print("Step 2/3: Summarising findings...\n")
    summary_result = agent.run_conversation(
          user_message=(
            "Now summarise your research into a well-structured article with:\n"
            "1. An executive summary (2-3 sentences)\n"
            "2. Key findings (bullet points)\n"
            "3. Analysis and implications\n"
            "4. Sources referenced\n\n"
            "Format it as clean markdown."
        ),
        conversation_history=history,
    )

    article = summary_result["final_response"]
    history = summary_result["messages"]
    print(f"Summary complete ({len(article)} chars)\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.lower().replace(" ", "_")[:40]
    filename = f"output/{safe_topic}_{timestamp}.md"

    print(f"Step 3/3: Saving to {filename}...\n")
    save_result = agent.run_conversation(
        user_message=(
            f"Save the article you just wrote to the file in the projects root directory: {filename}\n"
            f"Create the output/ directory if it doesn't exist.\n"
            f"Add a header with the topic and today's date."
        ),
        conversation_history=history,
    )
    
    print(f"Saved!\n")

    print(f"{'═' * 60}")
    print(f"  RESULTS")
    print(f"{'═' * 60}\n")
    print(article)
    print(f"\n{'═' * 60}")
    print(f"  File saved to: {filename}")
    print(f"{'═' * 60}\n")
    return article

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

    agent = create_agent()
    run_research(agent, topic)

if __name__ == "__main__":
    main()
