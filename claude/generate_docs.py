import os
import sys

from .api import (
    BASIC_DOCS_SYSTEM_PROMPT,
    REFINED_DOCS_FOLLOW_UP_PROMPT,
    check_prompt_token_size,
    read_file,
    request_message,
)
from claude.extract_repo import extract_local_directory


def generate_docs_from_local_repo(directory_path):
    """Generate docs for the provided repo using Claude Opus."""

    code_file_path = extract_local_directory(directory_path)
    repo_name = str(os.path.splitext(os.path.basename(code_file_path))[0]).replace(
        "_code", ""
    )
    file_content = read_file(code_file_path)
    input_prompt = f"Given this repo. \n{file_content}\ncomplete your instruction"
    token_size = check_prompt_token_size(input_prompt)

    proceed_check = input(
        f"Input token size is: {token_size}. Do you wish to proceed? (Y/N)"
    )
    if str(proceed_check).upper() != "Y":
        print("Exiting")

    messages = [
        {"role": "user", "content": input_prompt},
    ]
    response = request_message(BASIC_DOCS_SYSTEM_PROMPT, messages)

    message = response.content[0].text
    with open(f"{repo_name}-docs.md", "w", encoding="utf-8") as file:
        file.write(message)

    proceed_check = input(
        f"Please check the file generated at: {repo_name}-docs.md. Do you wish to further refine documentation? (Y/N)"
    )
    if str(proceed_check).upper() != "Y":
        print("Exiting")

    messages.extend(
        [
            {"role": "assistant", "content": message},
            {"role": "user", "content": REFINED_DOCS_FOLLOW_UP_PROMPT},
        ]
    )
    response = request_message(BASIC_DOCS_SYSTEM_PROMPT, messages)

    message = response.content[0].text
    with open(f"{repo_name}-further-docs.md", "w", encoding="utf-8") as file:
        file.write(message)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_docs.py <local repository directory>")
        sys.exit(1)

    directory_path = sys.argv[1]
    generate_docs_from_local_repo(directory_path)
