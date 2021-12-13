"""
Release the next version.
"""

import os
from pathlib import Path


def update_changelog(version: str) -> None:
    """
    Add a version title to the changelog.
    """
    changelog_path = Path('CHANGELOG.rst')
    changelog_contents = changelog_path.read_text(encoding='utf-8')
    new_changelog_contents = changelog_contents.replace(
        'Next\n----',
        f'Next\n----\n\n{version}\n------------',
    )
    changelog_path.write_text(new_changelog_contents, encoding='utf-8')


def main() -> None:
    """
    Perform a release.
    """
    version_str = os.environ['NEXT_VERSION']
    update_changelog(version=version_str)


if __name__ == '__main__':
    main()
