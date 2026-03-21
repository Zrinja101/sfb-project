#!/usr/bin/env python3
"""
Pre-commit hook to ensure all Python packages have __init__.py files.
"""

import os
import sys
from pathlib import Path


def find_python_packages_without_init(root_dir: str) -> list[str]:
    """Find Python packages (directories with .py files) missing __init__.py."""
    missing_init = []

    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if not d.startswith(
            '.') and d not in ['__pycache__', '.venv', '.pytest_cache']]

        # Check if this directory contains Python files
        has_py_files = any(f.endswith('.py') for f in files)

        if has_py_files:
            init_file = os.path.join(root, '__init__.py')
            if not os.path.exists(init_file):
                missing_init.append(root)

    return missing_init


def main():
    """Main entry point for the pre-commit hook."""
    # Get the repository root
    repo_root = Path(__file__).parent.parent

    # Find missing __init__.py files
    missing = find_python_packages_without_init(str(repo_root))

    if missing:
        print("❌ Missing __init__.py files in the following Python packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\n💡 All Python packages must have __init__.py files.")
        print("   Run the following command to add them automatically:")
        print("   python scripts/add_init_files.py")
        return 1

    print("✅ All Python packages have __init__.py files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
