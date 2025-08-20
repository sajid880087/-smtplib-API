from fastapi import FastAPI, Form
from pydantic import EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# --- Sender Info ---
SENDER_EMAIL = "sajitenamdar@gmail.com"
SENDER_PASSWORD = "izco vznp egme himr"   # App password

@app.post("/send-email/")
def send_email(
    to_email: EmailStr = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    cc_list: str = Form(""),   # optional, comma-separated
    bcc_list: str = Form("")   # optional, comma-separated
):
    try:
        # Convert CC/BCC to list
        cc_emails = [e.strip() for e in cc_list.split(",") if e.strip()]
        bcc_emails = [e.strip() for e in bcc_list.split(",") if e.strip()]

        # --- Setup SMTP ---
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # --- Create Email ---
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        if cc_emails:
            msg['Cc'] = ", ".join(cc_emails)
        msg['Subject'] = subject

        msg.attach(MIMEText(f"Hello,\n\n{message}", 'plain'))

        # --- Combine Recipients (To + CC + BCC) ---
        all_recipients = [to_email] + cc_emails + bcc_emails

        # --- Send ---
        server.sendmail(SENDER_EMAIL, all_recipients, msg.as_string())
        server.quit()

        return {"status": "success", "message": "Email sent successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
