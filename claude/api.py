import sys
import anthropic
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

PULL_REQUEST_SYSTEM_PROMPT = """Your job is to act as a expert software engineer and provide outlined comprehensive feedback for merge requests in a appraochable and understanding way.
Key criteria outlined are:
Does this code change accomplish what it is supposed to do?
Can this solution be simplified?
Does this change add unwanted compile-time or run-time dependencies?
Is a framework, API, library, or service used that should not be used?
Could an additional framework, API, library, or service improve the solution?
Is the code at the right abstraction level?
Is the code modular enough?
Can a better solution be found in terms of maintainability, readability, performance, or security?
Does similar functionality already exist in the codebase? If yes, why isnt it reused?
Are there any best practices, design patterns or language-specific patterns that could substantially improve this code?
Does this code adhere to Object-Oriented Analysis and Design Principles, like the Single Responsibility Principle, Open-Close Principle, Liskov Substitution Principle, Interface Segregation, or Dependency Injection?
Can you think of any use case in which the code does not behave as intended?
Can you think of any inputs or external events that could break the code?
You will receive both a description of the changes, an outline of the changes and the existing codebase.
"""

BASIC_DOCS_SYSTEM_PROMPT = """Your job is to act as the snior expert software engineer and provide detailed technical documentation broken into readbile formats. 
You will be able to read the majority of a code repository given as a converted single text with the PRefic "#File:" declaring the start of the new file e.g., # File: masters-and-sons-main/src/components/ArrowTable.tsx. 
Documentation should be broken down into:
Overall project structure, key features, data structure and common data objects, and key points of complexity with clear descriptions.
The output should be detailed in standard markdown, using headers to improve readability.
"""


def request_message(input: str) -> str:
    """"""
    response = CLIENT.messages.create(
        model="claude-3-opus-20240229",
        system=BASIC_DOCS_SYSTEM_PROMPT,
        max_tokens=4096,
        messages=[
            {"role": "user", "content": input},
        ],
    )

    return response.model_dump_json()


def read_file(file_path):
    """"""
    # read txt file
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            repo_content = file.read()
    else:
        print("Error: The file does not exist.")

    input = f"Fiven this repo. \n{repo_content}\ncomplete your instruction"
    message = request_message(input)
    print(message)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <txt file path>")
        sys.exit(1)

    read_file(sys.argv[1])
