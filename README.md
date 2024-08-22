# AI Docs

> [!NOTE]
> Documentation auto-generated by [ai-docs.](https://github.com/connor-john/ai-docs)

## Introduction
AI Docs is a Python project that generates technical documentation for code repositories using the Anthropic Claude AI model. The project aims to automate the process of creating comprehensive documentation by analyzing the codebase and generating readable, structured content. It can be particularly useful for quickly documenting projects and facilitating knowledge transfer among development teams.

## Codebase Overview
The AI Docs codebase is organized into a few key modules:

- `api.py`: Contains the main functionality for interacting with the Anthropic API, sending prompts, and receiving generated documentation.
- `extract_repo.py`: Responsible for extracting relevant code files from a local repository and converting them into a single text file for processing.
- `generate_docs.py`: Provides a high-level function to generate documentation for a given local repository directory.

The project uses the `anthropic` library for communicating with the Claude AI model and the `transformers` library for token counting. It also utilizes the `python-dotenv` library for managing environment variables, such as the Anthropic API key.

## Development Environment Setup
To set up the development environment for AI Docs, follow these steps:

1. Ensure you have Python 3.9 or higher installed on your system.
2. Clone the AI Docs repository from the version control system.
3. Navigate to the project directory.
4. Install Poetry, the dependency management tool used by the project, by following the official installation guide: https://python-poetry.org/docs/#installation
5. Run `poetry install` to install the project dependencies.
6. Set up your Anthropic API key as an environment variable named `ANTHROPIC_API_KEY`. You can use a `.env` file for this purpose.

## Code Repository Structure
The AI Docs repository has the following structure:

- `pyproject.toml`: The Poetry configuration file that defines the project's dependencies and metadata.
- `ai_docs/`: The main package directory containing the Python modules.
  - `api.py`: Contains the core functionality for interacting with the Anthropic API.
  - `extract_repo.py`: Handles the extraction of code files from a local repository.
  - `generate_docs.py`: Provides a high-level function to generate documentation for a given repository.

## Key Points of Complexity
1. Token Management:
   - The `check_prompt_token_size` function in `api.py` uses the GPT-2 tokenizer to estimate the number of tokens in a prompt. This is important to ensure that the prompt does not exceed the maximum token limit of the Claude model.
   - Handling token limits and efficiently constructing prompts is crucial for effectively utilizing the AI model.

2. Extracting Relevant Code Files:
   - The `extract_repo.py` module contains functions to determine which files in a repository are relevant for documentation generation.
   - It filters out unnecessary files and directories based on predefined criteria, such as file extensions, directory names, and file contents.
   - Extracting only the relevant code files helps reduce noise and focuses the documentation on the core aspects of the project.

## Installation and Setup
To install and set up AI Docs, follow these steps:

1. Clone the AI Docs repository from the version control system.
2. Navigate to the project directory.
3. Ensure you have Python 3.9 or higher installed on your system.
4. Install Poetry by following the official installation guide: https://python-poetry.org/docs/#installation
5. Run `poetry install` to install the project dependencies.
6. Set up your Anthropic API key as an environment variable named `ANTHROPIC_API_KEY`. You can use a `.env` file for this purpose.

## Getting Started
To generate documentation for a code repository using AI Docs, follow these steps:

1. Ensure you have completed the installation and setup process.
2. Open a terminal and navigate to the AI Docs project directory.
3. Run the following command, replacing `<local repository directory>` with the path to your code repository:
   ```
   python -m ai_docs.generate_docs <local repository directory>
   ```
4. The script will extract the relevant code files, send them to the Claude AI model for processing, and generate a `README.md` file inside the specified repository directory.
5. Review the generated documentation and make any necessary adjustments or additions.

That's it! You have now generated technical documentation for your code repository using AI Docs.
