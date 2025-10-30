"""
SendGrid Email Service
Handles all email notifications for the JobLink platform
"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from flask import current_app


class EmailService:
    """Email service using SendGrid"""
    
    @staticmethod
    def send_email(to_email, subject, html_content, text_content=None):
        """
        Send an email using SendGrid
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            html_content (str): HTML content of the email
            text_content (str, optional): Plain text content
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            api_key = current_app.config.get('SENDGRID_API_KEY')
            if not api_key:
                current_app.logger.warning("SendGrid API key not configured")
                return False
            
            from_email = Email(
                current_app.config.get('SENDGRID_FROM_EMAIL'),
                current_app.config.get('SENDGRID_FROM_NAME')
            )
            to_email = To(to_email)
            
            # Create message
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
            
            if text_content:
                message.plain_text_content = Content("text/plain", text_content)
            
            # Send email
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            
            current_app.logger.info(f"Email sent to {to_email}: {response.status_code}")
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            current_app.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new user"""
        subject = "Welcome to JobLink!"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">Welcome to JobLink, {user.first_name}!</h2>
                    <p>Thank you for joining JobLink, your trusted platform for connecting with local service providers.</p>
                    <p>Your account has been successfully created with the email: <strong>{user.email}</strong></p>
                    <p>You can now:</p>
                    <ul>
                        <li>Browse and book local service providers</li>
                        <li>Manage your bookings and appointments</li>
                        <li>Rate and review service providers</li>
                    </ul>
                    <p>If you have any questions, feel free to contact our support team.</p>
                    <p>Best regards,<br>The JobLink Team</p>
                </div>
            </body>
        </html>
        """
        return EmailService.send_email(user.email, subject, html_content)
    
    @staticmethod
    def send_booking_confirmation(booking, client, provider):
        """Send booking confirmation email to client"""
        subject = f"Booking Confirmation - {booking.service_category.name}"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">Booking Confirmed!</h2>
                    <p>Hi {client.first_name},</p>
                    <p>Your booking has been confirmed. Here are the details:</p>
                    <div style="background: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Service:</strong> {booking.service_category.name}</p>
                        <p><strong>Provider:</strong> {provider.first_name} {provider.last_name}</p>
                        <p><strong>Date:</strong> {booking.scheduled_date.strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p><strong>Duration:</strong> {booking.duration_hours} hour(s)</p>
                        <p><strong>Total Amount:</strong> KES {booking.total_amount}</p>
                        <p><strong>Address:</strong> {booking.address}</p>
                    </div>
                    <p>The provider will contact you shortly to confirm the appointment.</p>
                    <p>Best regards,<br>The JobLink Team</p>
                </div>
            </body>
        </html>
        """
        return EmailService.send_email(client.email, subject, html_content)
    
    @staticmethod
    def send_booking_notification_to_provider(booking, provider, client):
        """Send new booking notification to provider"""
        subject = f"New Booking Request - {booking.service_category.name}"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">New Booking Request!</h2>
                    <p>Hi {provider.first_name},</p>
                    <p>You have received a new booking request:</p>
                    <div style="background: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Client:</strong> {client.first_name} {client.last_name}</p>
                        <p><strong>Service:</strong> {booking.service_category.name}</p>
                        <p><strong>Date:</strong> {booking.scheduled_date.strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p><strong>Duration:</strong> {booking.duration_hours} hour(s)</p>
                        <p><strong>Amount:</strong> KES {booking.total_amount}</p>
                        <p><strong>Address:</strong> {booking.address}</p>
                        {f'<p><strong>Special Requests:</strong> {booking.special_requests}</p>' if booking.special_requests else ''}
                    </div>
                    <p>Please log in to your account to confirm or manage this booking.</p>
                    <p>Best regards,<br>The JobLink Team</p>
                </div>
            </body>
        </html>
        """
        return EmailService.send_email(provider.email, subject, html_content)
    
    @staticmethod
    def send_payment_confirmation(payment, booking, user):
        """Send payment confirmation email"""
        subject = "Payment Confirmation - JobLink"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #10b981;">Payment Successful!</h2>
                    <p>Hi {user.first_name},</p>
                    <p>Your payment has been processed successfully.</p>
                    <div style="background: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Amount Paid:</strong> KES {payment.amount}</p>
                        <p><strong>M-Pesa Receipt:</strong> {payment.mpesa_receipt}</p>
                        <p><strong>Booking ID:</strong> #{booking.id}</p>
                        <p><strong>Service:</strong> {booking.service_category.name}</p>
                        <p><strong>Date:</strong> {booking.scheduled_date.strftime('%B %d, %Y')}</p>
                    </div>
                    <p>Thank you for using JobLink!</p>
                    <p>Best regards,<br>The JobLink Team</p>
                </div>
            </body>
        </html>
        """
        return EmailService.send_email(user.email, subject, html_content)
    
    @staticmethod
    def send_password_reset_email(user, reset_token):
        """Send password reset email"""
        reset_link = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}"
        subject = "Password Reset Request - JobLink"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">Password Reset Request</h2>
                    <p>Hi {user.first_name},</p>
                    <p>We received a request to reset your password. Click the button below to reset it:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" style="background: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a>
                    </div>
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="color: #6b7280; word-break: break-all;">{reset_link}</p>
                    <p>This link will expire in 1 hour.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                    <p>Best regards,<br>The JobLink Team</p>
                </div>
            </body>
        </html>
        """
        return EmailService.send_email(user.email, subject, html_content)
