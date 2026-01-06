from mailersend import MailerSendClient, EmailBuilder

ms = MailerSendClient(api_key="mlsn.8c8457b5ce0ae504b9bf576cce706be37456441dab555d52506e7a4df9879a5d")

def send_email(to_email: str, subject: str, body: str):
    email = (EmailBuilder()
             .from_email("test@test-yxj6lj96y554do2r.mlsender.net", "Hostflow")
             .to(to_email)
             .subject(subject)
             .text(body)
             .build())

    response = ms.emails.send(email)
    print(response)