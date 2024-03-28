import sys
import anthropic
import os
from dotenv import load_dotenv, find_dotenv
from transformers import GPT2Tokenizer

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
You will be able to read the majority of a code repository given as a converted single text with the Prefix "#File:" declaring the start of the new file e.g., # File: masters-and-sons-main/src/components/ArrowTable.tsx. 
Typescipt projects are required to use pnpm for commands. MySQL databases are typically planetscale, and in that case we follow planetscales recommended use of prisma (if prisms ORM is used).
Documentation should be broken down into:
Introduction:
- Provide a brief overview of the project.
- Mention the purpose and core functionality of the code repository.
- Highlight the key features and potential use cases.
Codebase Overview:
- Provide an in-depth overview of the codebase architecture and design patterns used.
- Detail the modules, components, and their interactions within the application.
Development Environment Setup:
- Step-by-step instructions for setting up the development environment, including necessary tools and dependencies.
- Include guidelines for configuring IDEs, linters, and other development tools.
Code Repository Structure:
- Explain the repository structure, detailing the purpose of different directories and files.
- Document naming conventions, file organization, and any specific standards followed in the codebase.
Key Points of Complexity:
- Outline each keypoint of complexity
    - Breakdown each keypoint
Installation and Setup:
- Offer detailed instructions on installing and setting up the project.
- Include any prerequisites or dependencies required.
Getting Started:
- Guide users through a simple, initial setup or quick-start process.
- Include basic examples or a simple tutorial to help users begin using the project quickly.
The output should be detailed in standard markdown, using headers to improve readability. 
"""


def check_prompt_token_size(prompt: str) -> None:
    """Use GPT-2 to check the approximate number of tokens in a prompt"""
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokens = tokenizer.encode(prompt, add_special_tokens=False)
    # Token count
    return len(tokens)


def request_message(input: str, system_prompt: str) -> anthropic.types.Message:
    """Send message to Anthropic."""
    response = CLIENT.messages.create(
        model="claude-3-opus-20240229",
        system=system_prompt,
        max_tokens=4096,
        messages=[
            {"role": "user", "content": input},
        ],
    )

    return response


def read_file(file_path):
    """Read the text file containing the repo content."""
    # read txt file
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            repo_content = file.read()
    else:
        print("Error: The file does not exist.")

    return repo_content


def generate_docs(file_path):
    """Generate docs for the provided repo using Claude Opus."""
    repo_name = str(os.path.splitext(os.path.basename(file_path))[0]).replace(
        "_code", ""
    )
    file_content = read_file(file_path)
    input_prompt = f"Given this repo. \n{file_content}\ncomplete your instruction"
    token_size = check_prompt_token_size(input_prompt)

    proceed_check = input(
        f"Input token size is: {token_size}. Do you wish to proceed? (Y/N)"
    )
    if str(proceed_check).upper() != "Y":
        print("Exiting")

    response = request_message(input_prompt, BASIC_DOCS_SYSTEM_PROMPT)

    message = response.content[0].text
    with open(f"{repo_name}-docs.md", "w", encoding="utf-8") as file:
        file.write(message)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python api.py <txt file path>")
        sys.exit(1)

    generate_docs(sys.argv[1])
