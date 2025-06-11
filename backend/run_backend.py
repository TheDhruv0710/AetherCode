"""
AetherCode - Backend Server Runner
"""

from app import app

if __name__ == '__main__':
    print("Starting AetherCode backend server...")
    print("API available at http://localhost:5000/api")
    app.run(debug=True, host='0.0.0.0', port=5000)
