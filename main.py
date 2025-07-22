# main.py
from agent import AIResearchAgent

def main():
    """
    Main function to run the AI Research Assistant.
    """
    # Point the agent to its knowledge source
    knowledge_file = "knowledge_base.txt"
    agent = AIResearchAgent(knowledge_base_path=knowledge_file)

    # --- Ask some questions to test the agent ---

    # Example 1: A question that can be answered from the knowledge base
    agent.answer_question("What is Mars also known as and why?")

    # Example 2: Another question that can be answered
    agent.answer_question("What are the names of the moons of Mars?")

    # Example 3: A question about something not in the knowledge base
    agent.answer_question("What is the distance between Mars and Jupiter?")

if __name__ == "__main__":
    main()
