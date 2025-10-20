Flight Price Automation
This project is a Python-based automation tool that searches for the best round-trip flight deals for multiple destinations, ranks them based on price and duration, and sends a weekly summary report in a clean, responsive HTML email.

Features
Multi-Destination Search: Scans for flights to a predefined list of destinations.

Intelligent Ranking: Ranks flights using a weighted score based on price, duration, and number of connections to find the best overall deals.

Round-Trip Details: Fetches and displays full journey details for both outbound and return flights, including layovers.

Automated HTML Reports: Generates a modern, minimal, and mobile-friendly HTML email report.

Cloud-Ready: Designed to be deployed as a serverless weekly job using GitHub Actions.

Setup and Configuration
There are two ways to configure and run this project: locally for testing or deployed on GitHub Actions for full automation.

1. Local Setup (for testing)
Clone the repository:

Bash

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
Install dependencies:

Bash

pip install -r requirements.txt
Configure Credentials: Open the CONFIG.py file and hardcode your credentials directly:

Python

# In CONFIG.py
API_KEY = 'YOUR_SERPAPI_KEY_HERE'
SENDER_EMAIL = 'your_email@gmail.com'
RECEIVER_EMAIL = 'recipient_email@example.com'
EMAIL_PASSWORD = 'your_16_digit_app_password'
2. GitHub Actions Setup (for automation)
Push to GitHub: Upload the entire project to a public or private GitHub repository.

Update CONFIG.py: Ensure the CONFIG.py file is set to read from environment variables:

Python

# In CONFIG.py
import os
API_KEY = os.environ.get('API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
# ... and so on
Add Repository Secrets: In your GitHub repository, go to Settings > Secrets and variables > Actions and add the following repository secrets:

API_KEY: Your SerpApi API key.

SENDER_EMAIL: The Gmail address the report will be sent from.

RECEIVER_EMAIL: The email address that will receive the report.

EMAIL_PASSWORD: The 16-digit Google App Password for the sender's email.

Usage
To run locally:

Bash

python main.py
To run on GitHub Actions: The workflow, defined in .github/workflows/main.yml, is configured to run automatically every Sunday at 7 PM IDT. You can also trigger it manually by going to the Actions tab in your GitHub repository and clicking "Run workflow".
