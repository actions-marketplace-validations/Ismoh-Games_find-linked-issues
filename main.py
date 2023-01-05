import os
import re
import requests


class MissingEnvironmentVariable(Exception):
    pass


def main():
    """ Main function """

    # Get environment variables
    print("Fetching environment variables...")

    token = os.environ.get("TOKEN")
    if not token:
        raise MissingEnvironmentVariable("TOKEN environment variable not found")

    repo = os.environ.get("REPO")
    if not repo:
        raise MissingEnvironmentVariable("REPO environment variable not found")

    pull_request_number = os.environ.get("PULL_REQUEST_NUMBER")
    if not pull_request_number:
        raise MissingEnvironmentVariable("PULL_REQUEST_NUMBER environment variable not found")

    copy_issues_labels = os.environ.get("COPY_ISSUES_LABELS")
    if not copy_issues_labels:
        raise MissingEnvironmentVariable("COPY_ISSUES_LABELS environment variable not found")

    body = os.environ.get("BODY")
    if not body:
        raise MissingEnvironmentVariable("BODY environment variable not found")

    print("Environment variables fetched successfully")

    # Get pull request
    print("Fetching pull request...")

    pattern = r'(.lose|.ix|.esolve)(\S*|\s*).#\d+'

    matches = re.findall(pattern, body, re.MULTILINE)
    print(f"Matches: {matches}")

    issue_numbers = re.search(pattern, body)
    if not issue_numbers:
        raise RuntimeError("No issue found in the body")

    print(f"Issue number: {issue_numbers}")

    # Find issues
    print("Fetching issues...")

    params = {
        "is": "issue",
        "repo": repo,
        "linked": "pr",
        "": " ".join(str(i) for i in issue_numbers)
    }
    response = requests.get("https://api.github.com/search/issues?q=", params=params)

    if response.status_code != 200:
        raise RuntimeError(f"Error fetching issues: {response.text}")


if __name__ == "__main__":
    main()
