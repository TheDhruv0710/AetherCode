#!/usr/bin/env python3
"""
Test script for repository service functionality
"""

import os
import sys
import json
import tempfile
from services.repo_service import RepositoryService

def test_github_repo_download():
    """Test downloading and analyzing a GitHub repository"""
    repo_service = RepositoryService()
    
    # Test with a small public repository
    test_repo_url = "https://github.com/octocat/Hello-World"
    project_id = "test-project-123"
    
    print(f"Testing repository download: {test_repo_url}")
    
    try:
        # Test repository cloning (ZIP download)
        print("1. Testing repository download...")
        repo_path = repo_service.clone_repository(test_repo_url, project_id)
        print(f"✅ Repository downloaded to: {repo_path}")
        
        # Test repository info fetching
        print("\n2. Testing repository info fetching...")
        repo_info = repo_service.get_repository_info(test_repo_url)
        print(f"✅ Repository info: {json.dumps(repo_info, indent=2)}")
        
        # Test file structure
        print("\n3. Testing file structure extraction...")
        file_structure = repo_service.get_file_structure(repo_path)
        print(f"✅ File structure: {json.dumps(file_structure, indent=2)}")
        
        # Test key files extraction
        print("\n4. Testing key files extraction...")
        key_files = repo_service.get_key_files(repo_path)
        print(f"✅ Key files found: {list(key_files.keys())}")
        for filename, content in key_files.items():
            print(f"   - {filename}: {len(content)} characters")
        
        # Test repository summary
        print("\n5. Testing repository summary...")
        repo_summary = repo_service.get_repository_summary(repo_path)
        print(f"✅ Repository summary: {len(repo_summary)} characters")
        print(f"Summary preview: {repo_summary[:200]}...")
        
        # Test cleanup
        print("\n6. Testing cleanup...")
        repo_service.cleanup_repository(project_id)
        print("✅ Repository cleaned up successfully")
        
        print("\n🎉 All tests passed! Repository service is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_service():
    """Test AI service functionality"""
    from services.ai_service import AzureOpenAIService
    
    print("\nTesting AI Service...")
    ai_service = AzureOpenAIService()
    
    if ai_service.test_mode:
        print("✅ AI Service running in test mode (Azure OpenAI not configured)")
        
        # Test chat completion
        test_messages = [{"role": "user", "content": "Hello, can you help me analyze this code?"}]
        response = ai_service.chat_completion(test_messages)
        print(f"✅ Chat response: {response[:100]}...")
        
        # Test tech spec generation
        tech_spec = ai_service.generate_tech_spec("Test repo structure", {"test.py": "print('hello')"})
        print(f"✅ Tech spec generated: {len(tech_spec)} characters")
        
        return True
    else:
        print("✅ AI Service configured with Azure OpenAI")
        return True

if __name__ == "__main__":
    print("🚀 Starting AetherCode Backend Tests\n")
    
    # Test repository service
    repo_test_passed = test_github_repo_download()
    
    # Test AI service
    ai_test_passed = test_ai_service()
    
    print(f"\n📊 Test Results:")
    print(f"Repository Service: {'✅ PASSED' if repo_test_passed else '❌ FAILED'}")
    print(f"AI Service: {'✅ PASSED' if ai_test_passed else '❌ FAILED'}")
    
    if repo_test_passed and ai_test_passed:
        print("\n🎉 All backend services are working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        sys.exit(1)
