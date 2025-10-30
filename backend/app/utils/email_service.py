import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_email(to_email, subject, html_content, from_email=None):
    """Send email using SendGrid"""
    try:
        api_key = os.environ.get('SENDGRID_API_KEY')
        if not api_key:
            return {'success': False, 'error': 'SendGrid API key not configured'}
        
        sg = SendGridAPIClient(api_key=api_key)
        
        from_email = from_email or os.environ.get('FROM_EMAIL', 'noreply@joblink.com')
        
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        
        response = sg.send(message)
        
        return {
            'success': True,
            'status_code': response.status_code
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def send_verification_email(user_email, user_name, verification_token):
    """Send email verification"""
    subject = "Verify Your JobLink Account"
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2563eb;">Welcome to JobLink!</h2>
        <p>Hi {user_name},</p>
        <p>Thank you for signing up! Please verify your email address by clicking the button below:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{os.environ.get('FRONTEND_URL', 'http://localhost:3000')}/verify-email?token={verification_token}" 
               style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                Verify Email Address
            </a>
        </div>
        <p>If the button doesn't work, copy and paste this link into your browser:</p>
        <p style="word-break: break-all; color: #6b7280;">
            {os.environ.get('FRONTEND_URL', 'http://localhost:3000')}/verify-email?token={verification_token}
        </p>
        <p>Best regards,<br>The JobLink Team</p>
    </div>
    """
    
    return send_email(user_email, subject, html_content)

def send_booking_confirmation(client_email, client_name, provider_name, service_name, booking_date):
    """Send booking confirmation email"""
    subject = "Booking Confirmation - JobLink"
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #16a34a;">Booking Confirmed!</h2>
        <p>Hi {client_name},</p>
        <p>Your booking has been confirmed with the following details:</p>
        <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <p><strong>Service Provider:</strong> {provider_name}</p>
            <p><strong>Service:</strong> {service_name}</p>
            <p><strong>Date & Time:</strong> {booking_date}</p>
        </div>
        <p>The provider will contact you soon to confirm the details.</p>
        <p>Best regards,<br>The JobLink Team</p>
    </div>
    """
    
    return send_email(client_email, subject, html_content)

def send_booking_notification(provider_email, provider_name, client_name, service_name, booking_date):
    """Send new booking notification to provider"""
    subject = "New Booking Request - JobLink"
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2563eb;">New Booking Request!</h2>
        <p>Hi {provider_name},</p>
        <p>You have received a new booking request:</p>
        <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <p><strong>Client:</strong> {client_name}</p>
            <p><strong>Service:</strong> {service_name}</p>
            <p><strong>Requested Date:</strong> {booking_date}</p>
        </div>
        <p>Please log in to your dashboard to accept or decline this booking.</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{os.environ.get('FRONTEND_URL', 'http://localhost:3000')}/provider/dashboard" 
               style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                View Dashboard
            </a>
        </div>
        <p>Best regards,<br>The JobLink Team</p>
    </div>
    """
    
    return send_email(provider_email, subject, html_content)