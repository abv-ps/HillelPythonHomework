from abc import ABC, abstractmethod


class MessageSender(ABC):
    """
    Interface for sending messages through different services.
    """

    @abstractmethod
    def send_message(self, message: str) -> None:
        """
        Sends a message using a specific messaging service.

        Args:
            message (str): The message content to be sent.
        """
        pass


class SMSService:
    """
    Service for sending SMS messages.
    """

    def send_sms(self, phone_number: str, message: str) -> None:
        print(f"Sending SMS to {phone_number}: {message}")


class EmailService:
    """
    Service for sending emails.
    """

    def send_email(self, email_address: str, message: str) -> None:
        print(f"Sending Email to {email_address}: {message}")


class PushService:
    """
    Service for sending push notifications.
    """

    def send_push(self, device_id: str, message: str) -> None:
        print(f"Sending Push Notification to device {device_id}: {message}")


class SMSAdapter(MessageSender):
    """
    Adapter for SMSService to implement MessageSender interface.
    """

    def __init__(self, sms_service: SMSService, phone_number: str) -> None:
        self.sms_service = sms_service
        self.phone_number = phone_number

    def send_message(self, message: str) -> None:
        try:
            self.sms_service.send_sms(self.phone_number, message)
        except Exception as e:
            print(f"Error sending SMS: {e}")


class EmailAdapter(MessageSender):
    """
    Adapter for EmailService to implement MessageSender interface.
    """

    def __init__(self, email_service: EmailService, email_address: str) -> None:
        self.email_service = email_service
        self.email_address = email_address

    def send_message(self, message: str) -> None:
        try:
            self.email_service.send_email(self.email_address, message)
        except Exception as e:
            print(f"Error sending Email: {e}")


class PushAdapter(MessageSender):
    """
    Adapter for PushService to implement MessageSender interface.
    """

    def __init__(self, push_service: PushService, device_id: str) -> None:
        self.push_service = push_service
        self.device_id = device_id

    def send_message(self, message: str) -> None:
        try:
            self.push_service.send_push(self.device_id, message)
        except Exception as e:
            print(f"Error sending Push Notification: {e}")


# Example usage
if __name__ == "__main__":
    sms_service = SMSService()
    email_service = EmailService()
    push_service = PushService()

    sms_adapter = SMSAdapter(sms_service, "+380123456789")
    email_adapter = EmailAdapter(email_service, "user@example.com")
    push_adapter = PushAdapter(push_service, "device123")

    message = "Hello! This is a test message."

    adapters = [sms_adapter, email_adapter, push_adapter]

    for adapter in adapters:
        adapter.send_message(message)
