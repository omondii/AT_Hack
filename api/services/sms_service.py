# sms_service.py
import africastalking
import logging

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self, username, api_key):
        """Initialize Africa's Talking SMS service"""
        africastalking.initialize(username, api_key)
        self.sms = africastalking.SMS

    def send_sms(self, recipient, message):
        """
        Send an SMS message
        
        Args:
            recipient (str): The phone number to send the SMS to
            message (str): The message content
            
        Returns:
            dict: SMS response from Africa's Talking
        """
        try:
            response = self.sms.send(message, [recipient])
            logger.info(f"SMS sent: {response}")
            return response
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            raise
    
    def emergency_contact_confirmation(mapper, conn, rider):
        if rider.contact:
            message = (
            f"Rider {rider.full_name} added you as an Emergency contact. "
            "You will receive a text message or phone call in case they are involved in an accident."
        )
    
        recipient = [rider.contact.phone]
        SMSService.send_sms(recipient, message)



