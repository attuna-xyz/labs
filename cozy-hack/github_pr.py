import os
import jwt
import time
import requests
import logging
from github import Github
from github import GithubException
from config import *
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_private_key(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def create_jwt(app_id, private_key):
    now = int(time.time())
    payload = {
        'iat': now,
        'exp': now + 600,
        'iss': app_id
    }
    return jwt.encode(payload, private_key, algorithm='RS256')

def get_installation_access_token(jwt, installation_id):
    headers = {
        'Authorization': f'Bearer {jwt}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.post(
        f'https://api.github.com/app/installations/{installation_id}/access_tokens',
        headers=headers
    )
    response.raise_for_status()
    return response.json()['token']

def create_pull_request(installation_id, repo_name, branch_name, file_path, commit_message, pr_title, pr_body):
    logger.info(f"Starting PR creation process for {repo_name}, branch: {branch_name}")

    # Load GitHub App credentials
    app_id = os.environ.get('GITHUB_APP_ID')
    private_key_path = os.environ.get('GITHUB_PRIVATE_KEY_PATH')
    print("private_key_path", private_key_path)
    if not app_id :
        logger.error("GitHub App credentials not found in environment variables")
        raise ValueError("GitHub App credentials not found")
    if not private_key_path:
        logger.error("Private key path not found in environment variables")
        raise ValueError("Private key path not found")


    private_key = read_private_key(private_key_path)
    logger.info("Private key read successfully")

    # Create JWT
    jwt_token = create_jwt(app_id, private_key)
    logger.info("JWT token created successfully")

    # Get installation access token
    try:
        access_token = get_installation_access_token(jwt_token, installation_id)
        logger.info("Installation access token obtained successfully")
    except requests.RequestException as e:
        logger.error(f"Failed to get installation access token: {str(e)}")
        raise

    # Authenticate as GitHub App installation
    g = Github(access_token)

    try:
        # Get the repository
        repo = g.get_repo(repo_name)
        logger.info(f"Successfully accessed repository: {repo_name}")

        # Get the main branch
        source_branch = repo.get_branch("main")
        logger.info("Retrieved main branch")

        # Create a new branch
        try:
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)
            logger.info(f"Created new branch: {branch_name}")
        except GithubException as e:
            if e.status == 422:  # Branch already exists
                logger.info(f"Branch {branch_name} already exists. Proceeding with existing branch.")
            else:
                logger.error(f"Error creating branch: {str(e)}")
                raise

        # Read file content
        with open(file_path, 'r') as file:
            content = file.read()

        # Create or update file in the repository
        file_name = os.path.basename(file_path)
        try:
            contents = repo.get_contents(file_name, ref=branch_name)
            repo.update_file(contents.path, commit_message, content, contents.sha, branch=branch_name)
            logger.info(f"Updated file: {file_name}")
        except GithubException:
            repo.create_file(file_name, commit_message, content, branch=branch_name)
            logger.info(f"Created new file: {file_name}")

        # Create pull request
        try:
            pr = repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base="main")
            logger.info(f"Successfully created pull request. PR number: {pr.number}")
            return pr.number
        except GithubException as e:
            logger.error(f"Error creating pull request: {str(e)}")
            # Check if PR already exists
            pulls = list(repo.get_pulls(state='open', head=branch_name, base='main'))
            if pulls:
                logger.info(f"Pull request already exists. PR number: {pulls[0].number}")
                return pulls[0].number
            else:
                raise

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

def develyn_raise_pr():
    installation_id = os.environ.get('GITHUB_INSTALLATION_ID')# Replace with your GitHub App's installation ID
    repo_name = "attuna-xyz/prompt-learner"
    branch_name = BRANCH_NAME
    file_path = OUTPUT_FILE
    commit_message = "Add new guide in a notebook format"
    pr_title = "New Notebook Guide for Extreme Classification"
    pr_body = "This PR adds a new Extreme Classification Demo to the project."

    pr_number = create_pull_request(installation_id, repo_name, branch_name, file_path, commit_message, pr_title, pr_body)
    return f"Pull request created successfully. PR number: {pr_number}"