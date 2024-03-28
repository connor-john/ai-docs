import os

from claude.api import (
    BASIC_DOCS_SYSTEM_PROMPT,
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

    response = request_message(input_prompt, BASIC_DOCS_SYSTEM_PROMPT)

    message = response.content[0].text
    with open(f"{repo_name}-docs.md", "w", encoding="utf-8") as file:
        file.write(message)
