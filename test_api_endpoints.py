#!/usr/bin/env python3
"""
Test script for API endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_health_endpoint():
    """Test health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_repo_analyze_endpoint():
    """Test repository analysis endpoint"""
    print("\nTesting repository analysis endpoint...")
    try:
        payload = {
            "repo_url": "https://github.com/octocat/Hello-World"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/repo/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Repository analysis successful")
            print(f"   Project ID: {data.get('project_id')}")
            print(f"   Status: {data.get('status')}")
            print(f"   Files found: {len(data.get('files', []))}")
            return data.get('project_id')
        else:
            print(f"❌ Repository analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Repository analysis error: {e}")
        return None

def test_ai_chat_endpoint(project_id):
    """Test AI chat endpoint"""
    print(f"\nTesting AI chat endpoint with project {project_id}...")
    try:
        payload = {
            "project_id": project_id,
            "message": "What can you tell me about this repository?"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/ai/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ AI chat successful")
            print(f"   Response preview: {data.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ AI chat failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ AI chat error: {e}")
        return False

def test_reports_endpoint(project_id):
    """Test reports generation endpoint"""
    print(f"\nTesting reports endpoint with project {project_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/ai/reports/{project_id}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Reports generation successful")
            print(f"   Code health report: {len(data.get('code_health_report', ''))} chars")
            print(f"   Meeting minutes: {len(data.get('mom_content', ''))} chars")
            print(f"   Insights: {len(data.get('insights_content', ''))} chars")
            return True
        else:
            print(f"❌ Reports generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Reports generation error: {e}")
        return False

def test_file_content_endpoint(project_id):
    """Test file content retrieval endpoint"""
    print(f"\nTesting file content endpoint with project {project_id}...")
    try:
        # Try to get README.md content
        response = requests.get(f"{BASE_URL}/api/repo/{project_id}/file?path=README")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ File content retrieval successful")
            print(f"   Content preview: {data.get('content', '')[:100]}...")
            return True
        else:
            print(f"❌ File content retrieval failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ File content retrieval error: {e}")
        return False

def main():
    """Run all API endpoint tests"""
    print("🚀 Starting API Endpoint Tests\n")
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    if not health_ok:
        print("❌ Health check failed, server may not be running")
        return
    
    # Test repository analysis
    project_id = test_repo_analyze_endpoint()
    if not project_id:
        print("❌ Repository analysis failed, cannot continue with other tests")
        return
    
    # Wait a moment for processing
    time.sleep(1)
    
    # Test AI chat
    chat_ok = test_ai_chat_endpoint(project_id)
    
    # Test file content
    file_ok = test_file_content_endpoint(project_id)
    
    # Test reports generation
    reports_ok = test_reports_endpoint(project_id)
    
    # Summary
    print(f"\n📊 API Test Results:")
    print(f"Health Check: {'✅ PASSED' if health_ok else '❌ FAILED'}")
    print(f"Repository Analysis: {'✅ PASSED' if project_id else '❌ FAILED'}")
    print(f"AI Chat: {'✅ PASSED' if chat_ok else '❌ FAILED'}")
    print(f"File Content: {'✅ PASSED' if file_ok else '❌ FAILED'}")
    print(f"Reports Generation: {'✅ PASSED' if reports_ok else '❌ FAILED'}")
    
    all_passed = all([health_ok, project_id, chat_ok, file_ok, reports_ok])
    
    if all_passed:
        print("\n🎉 All API endpoints are working correctly!")
    else:
        print("\n⚠️ Some API endpoints had issues. Check the details above.")

if __name__ == "__main__":
    main()
