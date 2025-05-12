import base64, re
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from transformers import pipeline
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

app = FastAPI()
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
generator = pipeline("text2text-generation", model="google/flan-t5-large")


def extract_email(text):
    matches = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    return matches[0] if matches else None


def generate_email(job_description: str):
    prompt = f"""You are a professional job seeker named Asim Mahroos Mohammed.
Write a short, polite email to the recruiter based on the following job description.
Mention your skills in React, Java, AWS, and QA automation.
Do not ask for relocation assistance.

Job Description:
{job_description}

Email:"""
    result = generator(prompt, max_length=256, num_return_sequences=1)
    return result[0]['generated_text'].strip()


def create_email(to_email, subject, body_text, resume_data):
    message = MIMEMultipart()
    message['to'] = to_email
    message['subject'] = subject
    message.attach(MIMEText(body_text, 'plain'))

    part = MIMEApplication(resume_data, Name="Asim_Mahroos_Resume.pdf")
    part['Content-Disposition'] = 'attachment; filename="Asim_Mahroos_Resume.pdf"'
    message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}


def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)


@app.post("/generate-email")
async def gen_email_endpoint(job_description: str = Form(...)):
    email = generate_email(job_description)
    return {"email": email}


@app.post("/send-email")
async def send_email(job_description: str = Form(...), resume: UploadFile = Form(...)):
    recruiter_email = extract_email(job_description)
    if not recruiter_email:
        return JSONResponse(content={"error": "No valid email found"}, status_code=400)

    email_body = generate_email(job_description)
    resume_data = await resume.read()

    message = create_email(recruiter_email, "Application for the Job Opening", email_body, resume_data)
    service = get_gmail_service()
    service.users().messages().send(userId='me', body=message).execute()

    return {"status": "Email sent successfully", "to": recruiter_email}


# Add this block to run the server directly with `python bot.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:app", host="127.0.0.1", port=8000, reload=True)
