# Cold_Emailer
# Job Application Email Bot

This FastAPI application uses a text-generation model (`google/flan-t5-large`) to create polite and personalized job application emails and sends them to recruiters via Gmail. The resume is automatically attached to the email.

## Features

- Extracts recruiter email from job description
- Generates a professional application email using AI
- Sends the email with your resume as a PDF attachment
- Includes endpoints to generate or send the email

## Requirements

- Python 3.9+
- A Google Cloud project with Gmail API enabled
- `credentials.json` file for OAuth2
- Installed dependencies

## Installation

1. **Clone the repository**  
```bash
git clone https://github.com/asim-cyb1/Cold_Emailer.git
cd job-email-bot
