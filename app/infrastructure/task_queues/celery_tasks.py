import random
import time

from .celery_app import celery_app


@celery_app.task(name="send_email_notification")
def send_email_notification(email: str, username: str, subject: str, message: str):
    failure_probability = random.random()

    time.sleep(5)

    if failure_probability < 0.40:
        print(f"❌ Failed to send email to {email} - Connection timeout")
        raise Exception(
            f"Email service connection timeout with chance: {failure_probability}",
        )

    print(f"✅ Sending email to {email}")
    print(f"   Username: {username}")
    print(f"   Subject: {subject}")
    print(f"   Message: {message}")
    return {"status": "success", "email": email}


@celery_app.task(name="send_telegram_notification")
def send_telegram_notification(
    telegram: str,
    username: str,
    subject: str,
    message: str,
):
    time.sleep(5)

    if random.random() < 0.05:
        print(f"❌ Failed to send Telegram to {telegram} - API rate limit")
        raise Exception("Telegram API rate limit exceeded")

    print(f"✅ Sending Telegram message to {telegram}")
    print(f"   Username: {username}")
    print(f"   Subject: {subject}")
    print(f"   Message: {message}")
    return {"status": "success", "telegram": telegram}


@celery_app.task(name="send_sms_notification")
def send_sms_notification(phone: str, username: str, subject: str, message: str):
    time.sleep(5)

    if random.random() < 0.05:
        print(f"❌ Failed to send SMS to {phone} - Gateway error")
        raise Exception("SMS gateway error")

    print(f"✅ Sending SMS to {phone}")
    print(f"   Username: {username}")
    print(f"   Subject: {subject}")
    print(f"   Message: {message}")
    return {"status": "success", "phone": phone}


@celery_app.task(name="send_notification_with_fallback")
def send_notification_with_fallback(
    email: str,
    telegram: str,
    phone: str,
    username: str,
    subject: str,
    message: str,
):
    """Try to send notification via email, if fails try telegram, if fails try
    SMS."""
    errors = []

    # Try Email first
    try:
        return send_email_notification(email, username, subject, message)
    except Exception as e:
        errors.append(f"Email: {str(e)}")
        print("⚠️  Email failed, trying Telegram...")

    # Try Telegram then
    try:
        return send_telegram_notification(telegram, username, subject, message)
    except Exception as e:
        errors.append(f"Telegram: {str(e)}")
        print("⚠️  Telegram failed, trying SMS...")

    # Try SMS then
    try:
        return send_sms_notification(phone, username, subject, message)
    except Exception as e:
        errors.append(f"SMS: {str(e)}")
        print("❌ All notification channels failed!")

    raise Exception(f"All channels failed: {'; '.join(errors)}")
