import os
import sys
import ast
import shutil


def make_zip_file(directory_path: str, output_file_name: str) -> str:
    """Zip the given directory of a local repository"""
    shutil.make_archive(output_file_name, "zip", directory_path)
    return f"{output_file_name}.zip"


def is_desired_file(file_path: str) -> bool:
    """Check if the file is a JavaScript, TypeScript, or Prisma."""
    return (
        file_path.endswith(".ts")
        or file_path.endswith(".tsx")
        or file_path.endswith(".prisma")
    )


def is_likely_useful_file(file_path: str) -> bool:
    """Determine if the file is likely to be useful by excluding certain directories and specific file types."""
    excluded_dirs = [
        "docs",
        "examples",
        "tests",
        "test",
        "__pycache__",
        "scripts",
        "benchmarks",
        "node_modules",
        ".venv",
        "data",
    ]
    utility_or_config_files = ["hubconf.py", "setup.py", "package-lock.json"]
    github_workflow_or_docs = ["stale.py", "gen-card-", "write_model_card"]

    check_path = file_path.replace("\\", "/")
    parts = check_path.split(os.sep)[1:]
    if any(part.startswith(".") for part in parts):
        return False
    if "test" in check_path.lower():
        return False
    for excluded_dir in excluded_dirs:
        if f"/{excluded_dir}/" in check_path or check_path.startswith(
            f"{excluded_dir}/"
        ):
            return False
    for file_name in utility_or_config_files:
        if file_name in check_path:
            return False
    if not all(doc_file not in check_path for doc_file in github_workflow_or_docs):
        return False

    return True


def has_sufficient_content(file_content: list[str], min_line_count: int = 5) -> bool:
    """Check if the file has a minimum number of substantive lines."""
    lines = [
        line
        for line in file_content
        if line.strip() and not line.strip().startswith("//")
    ]
    return len(lines) >= min_line_count


def remove_comments_and_docstrings(source):
    """Remove comments and docstrings from the Python source code."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)
        ) and ast.get_docstring(node):
            node.body = node.body[1:]  # Remove docstring
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            node.value.s = ""  # Remove comments
    return ast.unparse(tree)


def extract_local_directory(directory_path: str) -> None:
    """Walks through a local directory and converts relevant code files to a .txt file"""
    repo_name = os.path.basename(directory_path)
    output_file = f"{repo_name}_code.txt"

    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Skip directories, non-code files, less likely useful files, hidden directories, and test files
                if (
                    file_path.endswith("/")
                    or not is_desired_file(file_path)
                    or not is_likely_useful_file(file_path)
                ):
                    continue
                with open(file_path, "r", encoding="utf-8") as file_content:
                    # Skip test files based on content and files with insufficient substantive content
                    file_lines = file_content.readlines()
                    if is_desired_file(file_path) and has_sufficient_content(
                        file_lines
                    ):
                        outfile.write(f"# File: {file_path}\n")
                        outfile.writelines(file_lines)
                        outfile.write("\n\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_repo.py <local repository directory>")
        sys.exit(1)

    directory_path = sys.argv[1]
    extract_local_directory(directory_path)
