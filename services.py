import git
import os
import shutil
import json
import time
import tempfile
import openai
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

# Initialize OpenAI client
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

def call_openai_api(prompt, system_prompt="You are a helpful AI assistant for code review."):
    """
    Call the OpenAI API with the given prompt and return the response.
    Falls back to mock data if the API key is not set or if the API call fails.
    """
    if not client or not OPENAI_API_KEY:
        print("OpenAI API key not set. Using mock data.")
        return get_mock_response(prompt)
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        # Fallback to mock data on API failure
        return get_mock_response(prompt)


def get_mock_response(prompt):
    """Returns mock data for different prompts."""
    if "technical specification" in prompt.lower() or "repository" in prompt.lower():
        return {
            "tech_spec": "# Mock Technical Specification\n\n## Project Overview\nThis appears to be a web application built with Flask that provides a code review and analysis dashboard. The application has a modern UI with a dark green theme and provides features for analyzing GitHub repositories, conducting AI-assisted code reviews, and generating reports.\n\n## Architecture\nThe application follows a typical Flask web application architecture with routes, services, and templates. It uses OpenAI's API for generating insights about code.\n\n## Key Components\n- Flask web server\n- GitHub repository analysis\n- OpenAI integration for code insights\n- Modern UI with dark green theme",
            "architecture": "The application uses a simple MVC-like architecture with Flask routes handling requests, services performing business logic, and templates rendering the UI.",
            "dependencies": "- Flask: Web framework\n- GitPython: For GitHub repository operations\n- OpenAI: For AI-powered code analysis\n- python-dotenv: For environment variable management",
            "questions": [
                "What are the main features you want to implement in the dashboard?",
                "How do you plan to handle authentication for private repositories?",
                "What specific code metrics are most important for your analysis?",
                "Would you like to implement real-time collaboration features?"
            ]
        }
    elif "dialogue" in prompt.lower():
        return {
            "ai_response": "That's a great insight! How would you refactor the code to improve performance (from OpenAI)?",
            "mom": "- User clarified the purpose of the main function.",
            "insights": "- The current implementation can be optimized."
        }
    elif "reports" in prompt.lower():
        return {
            "tech_spec": "This is the final refined technical specification (from OpenAI).",
            "mom": "- User clarified the purpose of the main function.\n- User suggested performance improvements.",
            "insights": "- The current implementation can be optimized.\n- A refactoring task has been created.",
            "code_health": "Overall code health is good, with some areas for improvement."
        }
    return {}


def analyze_repository(repo_url):
    """
    Clones a GitHub repository, analyzes its structure and code,
    and generates a technical specification using OpenAI.
    Falls back to mock data if cloning fails or if API key is not available.
    """
    # Check if OpenAI API key is available - if not, use mock data immediately
    if not OPENAI_API_KEY:
        print("OpenAI API key not set. Using mock data for repository analysis.")
        mock_data = get_mock_response(f"technical specification for repository {repo_url}")
        # Add repository URL to the mock data
        mock_data["repository_url"] = repo_url
        mock_data["note"] = "This is mock data. To get actual analysis, please set your OpenAI API key."
        return mock_data
        
    try:
        if not repo_url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format")

        # Create a platform-independent temporary directory
        temp_base = tempfile.gettempdir()
        
        # Extract repo name from URL
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        if not repo_name:
            repo_name = f"repo_{int(time.time())}"
            
        # Create full path to clone directory
        clone_dir = os.path.join(temp_base, f"aethercode_{repo_name}")
        print(f"Clone directory: {clone_dir}")

        # Clean up existing directory if it exists
        if os.path.exists(clone_dir):
            print(f"Removing existing directory: {clone_dir}")
            shutil.rmtree(clone_dir, ignore_errors=True)

        print(f"Cloning repository: {repo_url}")
        # Configure git to use longer timeouts
        git_env = os.environ.copy()
        git_env['GIT_HTTP_LOW_SPEED_LIMIT'] = '1000'
        git_env['GIT_HTTP_LOW_SPEED_TIME'] = '60'
        
        # Clone with explicit options
        repo = git.Repo.clone_from(
            repo_url, 
            clone_dir,
            env=git_env,
            depth=1  # Shallow clone for faster download
        )
        
        # Analyze the repository structure
        file_structure = get_repo_structure(clone_dir)
        file_contents = get_key_file_contents(clone_dir)
        commit_history = get_commit_history(repo)
        
        # Prepare a detailed prompt for OpenAI
        system_prompt = """You are an expert code reviewer and software architect. 
        Analyze the provided repository information and generate a comprehensive technical specification.
        Your response must be in JSON format with the following structure:
        {
            "tech_spec": "Detailed technical specification of the project",
            "architecture": "Description of the software architecture",
            "dependencies": "List of key dependencies and their purposes",
            "questions": ["List of 3-5 insightful questions to ask about the codebase"]
        }
        """
        
        prompt = f"""Repository: {repo_url}\n\n
        File Structure:\n{file_structure}\n\n
        Key Files:\n{file_contents}\n\n
        Commit History:\n{commit_history}\n\n
        Based on this information, generate a technical specification for the repository.
        """
        
        # Clean up the cloned repository
        shutil.rmtree(clone_dir)
        
        # Call OpenAI API with the detailed prompt
        return call_openai_api(prompt, system_prompt)

    except git.exc.GitCommandError as e:
        error_msg = f"Git command error: {e}"
        print(error_msg)
        return {
            "error": "Failed to clone repository",
            "details": str(e),
            "tech_spec": "Unable to analyze repository due to Git error. Please check the repository URL and try again.",
            "questions": ["Is the repository public?", "Is the URL correct?", "Does the repository exist?"]
        }
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
        # Still try to use OpenAI for a mock response
        prompt = "Generate a technical specification for a mock project."
        mock_response = call_openai_api(prompt)
        mock_response["error"] = "Repository analysis failed"
        mock_response["details"] = str(e)
        return mock_response


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
    Works in both API and mock modes.
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
        "mom": "A bullet point to add to the meeting minutes",
        "insights": "A key insight gained from this exchange",
        "todos": ["Optional list of to-do items identified"]
    }
    """
    
    # Prepare the conversation history for the API call
    conversation = []
    for msg in dialogue_history[project_id][-10:]:  # Include only the last 10 messages to avoid token limits
        conversation.append(msg["content"])
    
    # Create the prompt with conversation history
    prompt = f"Project ID: {project_id}\n\nConversation History:\n"
    prompt += "\n".join([f"{'User: ' if i % 2 == 0 else 'AI: '}{msg}" for i, msg in enumerate(conversation)])
    prompt += "\n\nBased on this conversation, provide your next response, meeting minutes update, and any insights or to-dos."
    
    # Call OpenAI API or use mock data
    if not OPENAI_API_KEY:
        print("OpenAI API key not set. Using mock data for dialogue.")
        response = get_mock_response("dialogue")
        # Add project-specific context to mock response
        response["ai_response"] = f"[Mock Mode] {response['ai_response']} (Project: {project_id})"
        response["mom"] += f" (Project: {project_id})"
        response["note"] = "This is mock data. To get actual AI responses, please set your OpenAI API key."
    else:
        response = call_openai_api(prompt, system_prompt)
    
    # Add AI response to dialogue history
    if "ai_response" in response:
        dialogue_history[project_id].append({"role": "assistant", "content": response["ai_response"]})
    
    return response


def generate_reports(project_id):
    """
    Generates the final reports for the project based on the dialogue history.
    Works in both API and mock modes.
    """
    if project_id not in dialogue_history or not dialogue_history[project_id]:
        return {"error": "No dialogue history found for this project."}
    
    # Prepare system prompt for generating final reports
    system_prompt = """You are an expert code reviewer and technical writer.
    Based on the provided dialogue history, generate comprehensive final reports.
    Your response must be in JSON format with the following structure:
    {
        "tech_spec": "Final technical specification based on the dialogue",
        "mom": "Complete meeting minutes summarizing the entire conversation",
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
    prompt += "\n\nBased on this complete conversation, generate final reports including technical specification, meeting minutes, insights, code health assessment, and action items."
    
    # Call OpenAI API or use mock data
    if not OPENAI_API_KEY:
        print("OpenAI API key not set. Using mock data for reports.")
        mock_response = get_mock_response("reports")
        # Add project-specific context to mock response
        mock_response["tech_spec"] = f"[Mock Mode] Technical Specification for Project: {project_id}\n" + mock_response["tech_spec"]
        mock_response["mom"] += f"\n- Project ID: {project_id}"
        mock_response["note"] = "This is mock data. To get actual AI-generated reports, please set your OpenAI API key."
        return mock_response
    else:
        return call_openai_api(prompt, system_prompt)
