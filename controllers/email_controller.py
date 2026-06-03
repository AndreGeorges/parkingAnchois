from services.email_service import sendEmail

def notifier(etat, event):
    sendEmail(etat, event)

