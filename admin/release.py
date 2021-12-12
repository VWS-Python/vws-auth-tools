"""
Release the next version.
"""

import os
from pathlib import Path

from github import Github
from github.ContentFile import ContentFile
from github.Repository import Repository


def update_changelog(version: str, github_repository: Repository) -> None:
    """
    Add a version title to the changelog.
    """
    changelog_path = Path('CHANGELOG.rst')
    branch = 'master'
    changelog_content_file = github_repository.get_contents(
        path=str(changelog_path),
        ref=branch,
    )
    # ``get_contents`` can return a ``ContentFile`` or a list of
    # ``ContentFile``s.
    assert isinstance(changelog_content_file, ContentFile)
    changelog_bytes = changelog_content_file.decoded_content
    changelog_contents = changelog_bytes.decode('utf-8')
    new_changelog_contents = changelog_contents.replace(
        'Next\n----',
        f'Next\n----\n\n{version}\n------------',
    )
    github_repository.update_file(
        path=str(changelog_path),
        message=f'Update for release {version}',
        content=new_changelog_contents,
        sha=changelog_content_file.sha,
    )


def main() -> None:
    """
    Perform a release.
    """
    github_token = os.environ['GITHUB_TOKEN']
    github_repository_name = os.environ['GITHUB_REPOSITORY']
    version_str = os.environ['NEXT_VERSION']
    github_client = Github(github_token)
    github_repository = github_client.get_repo(
        full_name_or_id=github_repository_name,
    )
    update_changelog(version=version_str, github_repository=github_repository)


if __name__ == '__main__':
    main()
