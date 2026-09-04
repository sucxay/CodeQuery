import os
from langchain_core.documents import Document


ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".html",
    ".css",
    ".md",
}


def load_repository(repo_path: str) -> list[Document]:

    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in {
                ".git",
                "node_modules",
                "__pycache__",
                ".venv",
                "venv"
            }
        ]

        for file in files:

            extension = os.path.splitext(file)[1].lower()

            if extension not in ALLOWED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                relative_path = os.path.relpath(
                    file_path,
                    repo_path
                )

                document = Document(
                    page_content=content,
                    metadata={
                        "file_path": relative_path,
                        "file_name": file,
                        "extension": extension
                    }
                )

                documents.append(document)

            except (UnicodeDecodeError, OSError):
                continue

    return documents