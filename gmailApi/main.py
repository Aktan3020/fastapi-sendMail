import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # Импортируйте класс CORSMiddleware
from typing import Optional
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",  # Укажите разрешенные домены
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = "noor.village.farmer@gmail.com"
smtp_password = "oontgzijanjtafac"

from_email = 'noor.village.farmer@gmail.com'

class EmailData(BaseModel):
    email: str
    title: str
    desc: str

@app.post("/send_email/")
async def send_email(data: EmailData):
    response = {"email": data.email, "title": data.title, "desc": data.desc}
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        msg = MIMEMultipart("alternative") 
        msg['From'] = from_email
        msg['To'] = data.email
        msg['Subject'] = data.title if data.title else "No Subject"

        html_content = """
        <html>
        <head>
        <style>
     h1{
     text-align:center;

     }
     @keyframes asa{
     0%{
     tranform:rotate(0deg);
     }
       50%{
     tranform:rotate(360deg);
     }
          100%{
     tranform:rotate(0deg);
     }
     }
        </style>
        </head>
        <body>
            <h1 style="color:white;background:black;height:40px;display:flex;justify-content:center;align-items:center ">{data.title}</h1>
            <p style="color:black;border:1px doted black;height:30px;display:flex;justify-content:center;align-items:center ">{data.desc}</p>
        </body>
        </html>
        """
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)
        
        server.sendmail(from_email, data.email, msg.as_string())
        print("Письмо успешно отправлено")
    except Exception as e:
        print("Ошибка при отправке письма:", e)
    finally:
        server.quit()
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
