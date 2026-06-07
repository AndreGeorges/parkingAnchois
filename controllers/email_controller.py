from services.email_service import sendEmail, send_email

def notifier(etat, event):
    sendEmail(etat, event)

