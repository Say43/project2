from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()


@tool
def calculate(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with numbers."""
    print("Tool has been called")
    return f"The result of {a} + {b} is {a + b}."


def main():
    model = ChatOpenAI(temperature=0)

    tools = []
    agent_executor = create_react_agent(model, tools)

    print("Hello! I am a ReAct agent. How can I assist you today?")
    print("You can ask me anything, and I will try to help you with my reasoning and actions.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "quit":
            break

        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
                print()


if __name__ == "__main__":
    main()
