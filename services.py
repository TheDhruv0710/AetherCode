import os
import json
import time
import tempfile
import openai
from openai import AzureOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_API_BASE, OPENAI_API_VERSION

# Import the github_api module for repository analysis without Git
from github_api import analyze_github_repository, get_repository_structure, get_key_file_contents

# Initialize Azure OpenAI client
client = None
if OPENAI_API_KEY and OPENAI_API_BASE:
    client = AzureOpenAI(
        api_key=OPENAI_API_KEY,
        api_version=OPENAI_API_VERSION,
        azure_endpoint=OPENAI_API_BASE
    )

def call_openai_api(prompt, system_prompt="You are a helpful AI assistant for code review."):
    """
    Call the Azure OpenAI API with the given prompt and return the response.
    Raises an exception if the API key is not set or if the API call fails.
    """
    if not client or not OPENAI_API_KEY or not OPENAI_API_BASE:
        raise ValueError("Azure OpenAI API configuration not complete. Please check your .env file.")
    
    try:
        # For Azure OpenAI, we just need to use the model parameter with the deployment name
        response = client.chat.completions.create(
            model=OPENAI_MODEL,  # This should be the deployment name in Azure
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise RuntimeError(f"Azure OpenAI API call failed: {e}")


# Azure OpenAI API functionality only


def analyze_repository(repo_url):
    """
    Analyzes a GitHub repository using the github_api module (no Git installation required),
    and generates a technical specification using Azure OpenAI API.
    """
    # Check if Azure OpenAI API configuration is complete
    if not OPENAI_API_KEY or not OPENAI_API_BASE:
        raise ValueError("Azure OpenAI API configuration not complete. Please check your .env file.")
        
    try:
        if not repo_url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format")
        
        # Use the github_api module to analyze the repository
        print(f"Analyzing repository: {repo_url}")
        repo_analysis = analyze_github_repository(repo_url)
        
        # Check if there was an error during analysis
        if 'error' in repo_analysis:
            raise RuntimeError(f"Error analyzing repository: {repo_analysis['error']}")
        
        # Extract the analysis results
        file_structure = repo_analysis['file_structure']
        file_contents = repo_analysis['file_contents']
        commit_history = repo_analysis['commit_history']
        
        # Prepare the prompt for OpenAI API
        prompt = f"""Repository URL: {repo_url}

Repository Structure:
{file_structure}

Key File Contents:
{file_contents}

Commit History:
{commit_history}

Based on this repository information, generate a comprehensive technical specification that includes:
1. Project overview and purpose
2. Architecture and design patterns
3. Key components and their relationships
4. Technologies and frameworks used
5. API endpoints (if applicable)
6. Database schema (if applicable)
7. Deployment considerations
8. Potential improvements or issues

Provide your response in JSON format with the following structure:
{
    "tech_spec": "The technical specification with sections and details",
    "insights": "Initial insights about the codebase",
    "code_health": "Assessment of code quality and health"
}
"""
        
        # Call Azure OpenAI API
        response = call_openai_api(prompt)
        
        return response
        
    except ValueError as e:
        error_msg = f"Value error: {e}"
        print(error_msg)
        return {
            "error": "Invalid repository URL",
            "details": str(e),
            "tech_spec": "Unable to analyze repository due to invalid URL format.",
            "questions": ["Is the URL in the correct format (https://github.com/username/repo)?"] 
        }
    except Exception as e:
        error_msg = f"Unexpected error during repository analysis: {e}"
        print(error_msg)
        return {
            "error": "Repository analysis failed",
            "details": str(e),
            "tech_spec": "Unable to analyze repository. Please check the repository URL and try again.",
            "questions": ["Is the repository public?", "Is the URL correct?", "Does the repository exist?", "Is the repository accessible?", "Is the repository structure valid?"]
        }


def get_repo_structure(repo_dir, max_files=50):
    """
    Returns a string representation of the repository file structure.
    Limits the number of files to avoid overwhelming the API.
    """
    structure = []
    file_count = 0
    
    for root, dirs, files in os.walk(repo_dir):
        if '.git' in root:
            continue
            
        level = root.replace(repo_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        folder_name = os.path.basename(root)
        structure.append(f"{indent}{folder_name}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            if file_count >= max_files:
                structure.append(f"{sub_indent}... (more files not shown)")
                break
            structure.append(f"{sub_indent}{file}")
            file_count += 1
    
    return '\n'.join(structure)


def get_key_file_contents(repo_dir, max_files=10, max_lines=50):
    """
    Returns the contents of key files in the repository.
    Focuses on important files like README, setup files, and main code files.
    """
    important_files = []
    
    # Priority files to look for
    priority_patterns = [
        'README.md', 'README.txt', 'setup.py', 'requirements.txt',
        'package.json', 'Dockerfile', '.env.example', 'main.py', 'app.py',
        'index.js', 'config.py'
    ]
    
    # Find priority files first
    for root, _, files in os.walk(repo_dir):
        if '.git' in root:
            continue
            
        for file in files:
            if file in priority_patterns and len(important_files) < max_files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(max_lines * 100)  # Approximate line limit
                        lines = content.split('\n')[:max_lines]
                        important_files.append(f"File: {os.path.relpath(file_path, repo_dir)}\n{'='*40}\n{chr(10).join(lines)}\n\n")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    
    return '\n'.join(important_files)


def get_commit_history(repo, max_commits=10):
    """
    Returns a summary of the recent commit history.
    """
    commits = []
    try:
        for commit in list(repo.iter_commits())[:max_commits]:
            commits.append(f"Commit: {commit.hexsha[:7]}")
            commits.append(f"Author: {commit.author.name}")
            commits.append(f"Date: {commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            commits.append(f"Message: {commit.message.strip()}")
            commits.append("-" * 40)
    except Exception as e:
        print(f"Error getting commit history: {e}")
        commits.append("Could not retrieve commit history.")
    
    return '\n'.join(commits)


# Store dialogue history for each project
dialogue_history = {}

def process_dialogue(project_id, user_response):
    """
    Processes a turn in the dialogue with the AI.
    Maintains conversation history to provide context for the AI.
    Uses Azure OpenAI API for generating responses.
    """
    # Initialize dialogue history for this project if it doesn't exist
    if project_id not in dialogue_history:
        dialogue_history[project_id] = []
    
    # Add user message to dialogue history
    dialogue_history[project_id].append({"role": "user", "content": user_response})
    
    # Prepare system prompt for code review dialogue
    system_prompt = """You are an expert code reviewer and AI interviewer.
    Engage in a dialogue about the codebase, asking insightful questions and providing helpful feedback.
    Your goal is to understand the code better and help improve it.
    Your response must be in JSON format with the following structure:
    {
        "ai_response": "Your response to the user",
        "discussion_points": "A bullet point to add to the discussion points",
        "insights": "A key insight gained from this exchange",
        "action_items": ["Optional list of action items identified"]
    }
    """
    
    # Prepare the conversation history for the API call
    conversation = []
    for msg in dialogue_history[project_id][-10:]:  # Include only the last 10 messages to avoid token limits
        conversation.append(msg["content"])
    
    # Create the prompt with conversation history
    prompt = f"Project ID: {project_id}\n\nConversation History:\n"
    prompt += "\n".join([f"{'User: ' if i % 2 == 0 else 'AI: '}{msg}" for i, msg in enumerate(conversation)])
    prompt += "\n\nBased on this conversation, provide your next response, discussion points update, and any insights or action items."
    
    # Call Azure OpenAI API
    try:
        response = call_openai_api(prompt, system_prompt)
    except Exception as e:
        # Return error response if API call fails
        return {
            "error": str(e),
            "ai_response": f"Error: Could not process request. Please check your Azure OpenAI configuration.",
            "discussion_points": "- Error occurred during AI processing.",
            "insights": "- System encountered an error with Azure OpenAI API."
        }
    
    # Add AI response to dialogue history
    if "ai_response" in response:
        dialogue_history[project_id].append({"role": "assistant", "content": response["ai_response"]})
    
    return response


def generate_reports(project_id):
    """
    Generates the final reports for the project based on the dialogue history.
    Uses Azure OpenAI API for generating comprehensive reports.
    """
    if project_id not in dialogue_history or not dialogue_history[project_id]:
        return {"error": "No dialogue history found for this project."}
    
    # Prepare system prompt for generating final reports
    system_prompt = """You are an expert code reviewer and technical writer.
    Based on the provided dialogue history, generate comprehensive final reports.
    Your response must be in JSON format with the following structure:
    {
        "tech_spec": "Final technical specification based on the dialogue",
        "discussion_points": "Complete discussion points summarizing the entire conversation",
        "insights": "Key insights and findings from the code review",
        "code_health": "Assessment of the overall code health and recommendations",
        "action_items": ["List of action items and next steps"]
    }
    """
    
    # Prepare the conversation history for the API call
    conversation = []
    for msg in dialogue_history[project_id]:
        conversation.append(f"{msg['role'].capitalize()}: {msg['content']}")
    
    # Create the prompt with the full conversation history
    prompt = f"Project ID: {project_id}\n\nComplete Dialogue History:\n"
    prompt += "\n".join(conversation)
    prompt += "\n\nBased on this complete conversation, generate final reports including technical specification, discussion points, insights, code health assessment, and action items."
    
    # Call Azure OpenAI API
    try:
        return call_openai_api(prompt, system_prompt)
    except Exception as e:
        # Return error response if API call fails
        return {
            "error": str(e),
            "tech_spec": "Error: Could not generate technical specification. Please check your Azure OpenAI configuration.",
            "discussion_points": "Error occurred during report generation.",
            "insights": "System encountered an error with Azure OpenAI API.",
            "code_health": "Unable to assess code health due to API error.",
            "action_items": ["Check Azure OpenAI API configuration", "Verify API key and endpoint URL"]
        }


# Function to get repository structure
def get_repository_structure(project_id):
    """
    Get the repository structure for a project.
    In a real implementation, this would retrieve the stored repository structure.
    
    Args:
        project_id (str): The project ID
        
    Returns:
        dict: Repository structure information
    """
    try:
        # In a production environment, you would retrieve this from a database
        # For now, we'll return a simple structure or check the temp_repos directory
        import os
        from config import TEMP_REPO_DIR
        
        # Check if we have any repositories in the temp_repos directory
        if os.path.exists(TEMP_REPO_DIR):
            repo_dirs = [d for d in os.listdir(TEMP_REPO_DIR) if os.path.isdir(os.path.join(TEMP_REPO_DIR, d))]
            
            if repo_dirs:
                # Use the most recent repository directory
                repo_dir = os.path.join(TEMP_REPO_DIR, repo_dirs[-1])
                
                # Find subdirectories in the repository directory
                extracted_dirs = [d for d in os.listdir(repo_dir) if os.path.isdir(os.path.join(repo_dir, d))]
                if extracted_dirs:
                    # Use the first extracted directory (typically the repository name with branch)
                    repo_dir = os.path.join(repo_dir, extracted_dirs[0])
                
                # Get the repository structure using the github_api module
                from github_api import get_repository_structure as get_repo_structure
                file_structure = get_repo_structure(repo_dir)
                
                # Print the file structure for debugging
                print(f"File structure for {project_id}:\n{file_structure}")
                
                return {
                    "file_structure": file_structure,
                    "project_id": project_id
                }
        
        # If no repository is found, return a simple structure
        return {
            "file_structure": "Repository structure not available.",
            "project_id": project_id
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "error": f"Failed to get repository structure: {str(e)}",
            "project_id": project_id
        }
