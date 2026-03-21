#!/usr/bin/env python3
"""
Script to automatically add missing __init__.py files to Python packages.
"""

import os
from pathlib import Path


def add_missing_init_files(root_dir: str) -> int:
    """Add __init__.py files to Python packages that don't have them."""
    added_count = 0

    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', '.venv', '.pytest_cache', 'node_modules']]

        # Check if this directory contains Python files
        has_py_files = any(f.endswith('.py') for f in files)

        if has_py_files:
            init_file = os.path.join(root, '__init__.py')
            if not os.path.exists(init_file):
                # Create __init__.py with a basic docstring
                rel_path = os.path.relpath(root, root_dir)
                module_name = rel_path.replace(os.sep, '.')

                init_content = f'''"""
{module_name} module.
"""

'''

                with open(init_file, 'w') as f:
                    f.write(init_content)

                print(f"✅ Created {init_file}")
                added_count += 1

    return added_count


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent

    print("🔍 Scanning for missing __init__.py files...")
    added = add_missing_init_files(str(repo_root))

    if added > 0:
        print(f"\n✅ Added {added} __init__.py files.")
        print("   Don't forget to commit these new files!")
    else:
        print("\n✅ All Python packages already have __init__.py files.")


if __name__ == "__main__":
    main()