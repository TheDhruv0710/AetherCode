# AetherCode: The Cognitive Core Interface

AetherCode is a groundbreaking AI-powered web application for the 'AI & Developer Productivity Hackathon.' Our vision is to replace cumbersome, scheduled code review meetings with an intelligent AI interviewer that understands code, asks precise questions, and automatically generates comprehensive documentation in real-time. AetherCode is the future of streamlined, efficient, and AI-augmented developer collaboration.

## How to Run

1.  **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
2.  **Run the Flask application:**
    ```
    python app.py
    ```
3.  Open your browser and navigate to `http://127.0.0.1:5000`.

## Project Structure

-   `app.py`: Main Flask application file.
-   `routes.py`: Defines the API endpoints.
-   `services.py`: Contains the business logic for interacting with Git and the AI.
-   `templates/index.html`: The main HTML file for the frontend.
-   `static/css/style.css`: The CSS file for styling the frontend.
-   `static/js/script.js`: The JavaScript file for frontend logic.
-   `requirements.txt`: The Python dependencies for the project.
