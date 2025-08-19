from pathlib import Path
IGNORE = {
    "extensions": [
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",  
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",  
        ".zip", ".tar", ".gz", ".rar", ".7z", ".bz2",  
        ".exe", ".dll", ".so", ".dylib", ".bin", ".dat", ".class", ".o", ".a",  
        ".pyc", ".pyo", ".pyd", ".db", ".sqlite", ".log", ".lock",  
    ],

    "directories": [
        "__pycache__",
        ".git", ".hg", ".svn", ".bzr",  
        "node_modules", "bower_components",  
        "dist", "build", "out", "target",  
        ".mypy_cache", ".pytest_cache", ".tox", ".ruff_cache", ".coverage",  
        ".idea", ".vscode", ".DS_Store",  
        "env", "venv", ".venv", "ENV",  
    ],

    "filenames": [
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml",  
        "Cargo.lock",
        "Pipfile.lock", "poetry.lock",
        "Thumbs.db",
    ],
}

def should_ignore(path: Path):
    if any(part in IGNORE["directories"] for part in path.parts):
        return True
    if path.suffix in IGNORE["extensions"]:
        return True
    if path.name in IGNORE["filenames"]:
        return True
    return False