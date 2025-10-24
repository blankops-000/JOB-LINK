# Import the requests library to make HTTP calls to the M-Pesa API
import requests
# Import base64 for encoding authentication strings as required by M-Pesa
import base64
# Import datetime to generate timestamps for API requests
from datetime import datetime
# Import json for handling JSON data in API responses
import json
# Import current_app to access Flask application configuration
from flask import current_app

# Define the main M-Pesa service class that handles all payment operations
class MpesaService:
    """
    M-Pesa API Service for handling payments in Kenya
    This class handles STK push (Lipa Na M-Pesa) payments
    """
    
    # Constructor method that runs when a new MpesaService object is created
    def __init__(self):
        # Get the M-Pesa consumer key from Flask app configuration
        self.consumer_key = current_app.config['MPESA_CONSUMER_KEY']
        # Get the M-Pesa consumer secret from Flask app configuration
        self.consumer_secret = current_app.config['MPESA_CONSUMER_SECRET']
        # Get the M-Pesa base URL, default to sandbox for testing
        self.base_url = current_app.config.get('MPESA_BASE_URL', 'https://sandbox.safaricom.co.ke')
    
    # Method to get an access token from M-Pesa API (required for all API calls)
    def get_access_token(self):
        # Use try-except block to handle potential errors
        try:
            # Create authentication string by combining consumer key and secret with colon
            auth_string = f"{self.consumer_key}:{self.consumer_secret}"
            # Encode the authentication string to base64 format (M-Pesa requirement)
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            
            # Create headers for the HTTP request with Basic Authentication
            headers = {
                'Authorization': f'Basic {encoded_auth}'  # Basic Auth with encoded credentials
            }
            
            # Make GET request to M-Pesa OAuth endpoint to get access token
            response = requests.get(
                f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials',  # OAuth endpoint
                headers=headers,      # Include authentication headers
                timeout=30            # Set 30-second timeout to prevent hanging
            )
            
            # Check if the request was successful (HTTP status 200)
            if response.status_code == 200:
                # Parse the JSON response from M-Pesa
                token_data = response.json()
                # Extract and return the access token from the response
                return token_data.get('access_token')
            else:
                # Log error details if token request failed
                print(f"M-Pesa token error: {response.status_code} - {response.text}")
                # Return None to indicate failure
                return None
                
        # Catch any exceptions that occur during the token request
        except Exception as e:
            # Log the exception details
            print(f"M-Pesa token exception: {str(e)}")
            # Return None to indicate failure
            return None
    
    # Method to initiate STK push (Lipa Na M-Pesa) payment
    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        # Use try-except block to handle potential errors
        try:
            # First, get an access token for authentication
            access_token = self.get_access_token()
            # Check if token was obtained successfully
            if not access_token:
                # Return error if token acquisition failed
                return {'success': False, 'error': 'Failed to get access token'}
            
            # Format phone number to M-Pesa required format (2547...)
            # Check if phone number starts with 0 (local Kenyan format)
            if phone_number.startswith('0'):
                # Replace leading 0 with 254 (0712345678 -> 254712345678)
                phone_number = '254' + phone_number[1:]
            # Check if phone number starts with + (international format)
            elif phone_number.startswith('+'):
                # Remove the + prefix (+254712345678 -> 254712345678)
                phone_number = phone_number[1:]
            
            # Generate current timestamp in format required by M-Pesa (YYYYMMDDHHMMSS)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            # Get M-Pesa passkey from application configuration
            passkey = current_app.config['MPESA_PASSKEY']
            # Get business shortcode (paybill/till number) from configuration
            business_shortcode = current_app.config['MPESA_BUSINESS_SHORTCODE']
            
            # Generate password by combining shortcode, passkey and timestamp, then base64 encode
            password = base64.b64encode(
                f"{business_shortcode}{passkey}{timestamp}".encode()  # Combine and convert to bytes
            ).decode()  # Convert base64 bytes back to string
            
            # Create the payload (data) for the STK push request
            payload = {
                "BusinessShortCode": business_shortcode,  # Business paybill/till number
                "Password": password,                     # Encoded password
                "Timestamp": timestamp,                   # Current timestamp
                "TransactionType": "CustomerPayBillOnline",  # Type of transaction
                "Amount": amount,                         # Payment amount (integer)
                "PartyA": phone_number,                   # Customer phone number
                "PartyB": business_shortcode,             # Business shortcode (recipient)
                "PhoneNumber": phone_number,              # Customer phone number (again)
                "CallBackURL": f"{current_app.config['BASE_URL']}/api/payments/mpesa-callback",  # Callback endpoint
                "AccountReference": account_reference,    # Unique reference for tracking
                "TransactionDesc": transaction_desc       # Description shown to customer
            }
            
            # Create headers for the STK push request
            headers = {
                'Authorization': f'Bearer {access_token}',  # Use access token for authentication
                'Content-Type': 'application/json'         # Specify JSON content type
            }
            
            # Make POST request to M-Pesa STK push endpoint
            response = requests.post(
                f'{self.base_url}/mpesa/stkpush/v1/processrequest',  # STK push API endpoint
                json=payload,        # Send payload as JSON
                headers=headers,     # Include authentication headers
                timeout=30           # Set 30-second timeout
            )
            
            # Check if the API request was successful
            if response.status_code == 200:
                # Parse the JSON response from M-Pesa
                result = response.json()
                # Check if M-Pesa accepted the request (ResponseCode 0 means success)
                if result.get('ResponseCode') == '0':
                    # Return success with transaction details
                    return {
                        'success': True,                              # Indicate success
                        'checkout_request_id': result.get('CheckoutRequestID'),  # ID for tracking
                        'customer_message': result.get('CustomerMessage'),       # Message to customer
                        'merchant_request_id': result.get('MerchantRequestID')   # Merchant tracking ID
                    }
                else:
                    # Return error if M-Pesa rejected the request
                    return {
                        'success': False,                                     # Indicate failure
                        'error': result.get('ResponseDescription', 'Payment request failed'),  # Error message
                        'response_code': result.get('ResponseCode')           # M-Pesa error code
                    }
            else:
                # Return error if HTTP request failed
                return {
                    'success': False,                             # Indicate failure
                    'error': f'HTTP {response.status_code}: {response.text}'  # HTTP error details
                }
                
        # Catch any exceptions that occur during STK push
        except Exception as e:
            # Return exception details
            return {
                'success': False,           # Indicate failure
                'error': f'Exception: {str(e)}'  # Exception message
            }
    
    # Method to check the status of a transaction using checkout request ID
    def check_transaction_status(self, checkout_request_id):
        # Use try-except block to handle potential errors
        try:
            # First, get an access token for authentication
            access_token = self.get_access_token()
            # Check if token was obtained successfully
            if not access_token:
                # Return error if token acquisition failed
                return {'success': False, 'error': 'Failed to get access token'}
            
            # Generate current timestamp for the request
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            # Get M-Pesa passkey from configuration
            passkey = current_app.config['MPESA_PASSKEY']
            # Get business shortcode from configuration
            business_shortcode = current_app.config['MPESA_BUSINESS_SHORTCODE']
            
            # Generate password (same as in STK push)
            password = base64.b64encode(
                f"{business_shortcode}{passkey}{timestamp}".encode()  # Combine and encode
            ).decode()  # Convert to string
            
            # Create payload for status check request
            payload = {
                "BusinessShortCode": business_shortcode,      # Business shortcode
                "Password": password,                         # Encoded password
                "Timestamp": timestamp,                       # Current timestamp
                "CheckoutRequestID": checkout_request_id      # ID from STK push response
            }
            
            # Create headers for the status check request
            headers = {
                'Authorization': f'Bearer {access_token}',    # Use access token
                'Content-Type': 'application/json'           # JSON content type
            }
            
            # Make POST request to M-Pesa status check endpoint
            response = requests.post(
                f'{self.base_url}/mpesa/stkpushquery/v1/query',  # Status check API endpoint
                json=payload,        # Send payload as JSON
                headers=headers,     # Include authentication headers
                timeout=30           # Set 30-second timeout
            )
            
            # Check if the API request was successful
            if response.status_code == 200:
                # Parse and return the JSON response
                result = response.json()
                return {
                    'success': True,                 # Indicate success
                    'result_code': result.get('ResultCode'),      # M-Pesa result code
                    'result_desc': result.get('ResultDesc'),      # Result description
                    'response': result               # Full response object
                }
            else:
                # Return error if HTTP request failed
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        # Catch any exceptions that occur during status check
        except Exception as e:
            # Return exception details
            return {'success': False, 'error': str(e)}