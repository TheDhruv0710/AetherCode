"""
Code review service for AetherCode application
"""
import random

# Mock AI responses for development (would be replaced with actual OpenAI API calls)
MOCK_AI_RESPONSES = {
    'greetings': [
        "Hello! How can I help you with your code today?",
        "Hi there! What coding challenge are you working on?",
        "Greetings! I'm here to assist with your programming needs."
    ],
    'code_review': {
        'python': [
            "Your Python code looks good! Consider using list comprehensions for better readability.",
            "I noticed you're not using type hints. They can make your code more maintainable.",
            "Your code follows PEP 8 guidelines well. You might want to add more docstrings."
        ],
        'javascript': [
            "Your JavaScript code is clean. Consider using const/let instead of var.",
            "You might benefit from using arrow functions for better scoping.",
            "Your code could be more modular. Consider breaking it into smaller functions."
        ],
        'general': [
            "Your code is well-structured. Here are some minor suggestions for improvement...",
            "I found a few potential issues that might cause bugs later. Let me explain...",
            "Your algorithm works, but there might be a more efficient approach."
        ]
    }
}

def generate_review(code, language, analysis):
    """Generate a code review based on analysis results"""
    issues = analysis.get('issues', [])
    metrics = analysis.get('metrics', {})
    
    # Start with a general comment
    if language in MOCK_AI_RESPONSES['code_review']:
        review = random.choice(MOCK_AI_RESPONSES['code_review'][language])
    else:
        review = random.choice(MOCK_AI_RESPONSES['code_review']['general'])
    
    # Add information about code metrics
    review += f"\n\n**Code Metrics:**\n- Lines of code: {metrics.get('lines', 0)}\n- Estimated complexity: {metrics.get('complexity', 0)}"
    
    # Add information about issues
    if issues:
        review += "\n\n**Potential Issues:**"
        for i, issue in enumerate(issues[:5]):  # Limit to 5 issues
            review += f"\n{i+1}. Line {issue['line']}: {issue['type']} - {issue['text']}"
        
        if len(issues) > 5:
            review += f"\n...and {len(issues) - 5} more issues."
    else:
        review += "\n\n**No significant issues found.**"
    
    # Add recommendations
    review += "\n\n**Recommendations:**"
    if 'complexity' in [issue['type'] for issue in issues]:
        review += "\n- Consider breaking down complex functions into smaller, more manageable pieces."
    if 'unused_import' in [issue['type'] for issue in issues] or 'unused_var' in [issue['type'] for issue in issues]:
        review += "\n- Remove unused imports and variables to improve code cleanliness."
    if 'bad_practice' in [issue['type'] for issue in issues]:
        review += "\n- Address potential bad practices identified in the code."
    if 'long_line' in [issue['type'] for issue in issues]:
        review += "\n- Break long lines into smaller chunks for better readability."
    if 'todo' in [issue['type'] for issue in issues]:
        review += "\n- Address TODO comments before finalizing the code."
    
    # Add a positive closing note
    review += "\n\nOverall, your code is on the right track. Let me know if you'd like more specific guidance on any of these points!"
    
    return review
