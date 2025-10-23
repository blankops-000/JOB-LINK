
import base64
from datetime import datetime
import requests
from flask import current_app, has_app_context

class MpesaService:
    """
    Thin wrapper for Safaricom M-Pesa STK push and token endpoints.
    Usage: call from within an app/request context (current_app must be available).
    """

    def _ensure_app_ctx(self):
        if not has_app_context():
            raise RuntimeError("MpesaService requires a Flask application context")

    def _get_cfg(self, key, default=None, required=False):
        self._ensure_app_ctx()
        val = current_app.config.get(key, default)
        if required and not val:
            raise RuntimeError(f"Missing required MPESA config: {key}")
        return val

    def _normalize_phone(self, phone_number: str) -> str:
        if not phone_number:
            return phone_number
        phone_number = phone_number.strip()
        # Remove plus sign
        if phone_number.startswith('+'):
            phone_number = phone_number[1:]
        # If starts with 0 -> convert to 254...
        if phone_number.startswith('0'):
            return '254' + phone_number[1:]
        # If already starts with country code like 254
        return phone_number

    def get_access_token(self):
        """Get M-Pesa API access token. Returns token string or None on failure."""
        try:
            self._ensure_app_ctx()
            consumer_key = self._get_cfg('MPESA_CONSUMER_KEY', required=True)
            consumer_secret = self._get_cfg('MPESA_CONSUMER_SECRET', required=True)
            base_url = self._get_cfg('MPESA_BASE_URL', 'https://sandbox.safaricom.co.ke')

            auth_string = f"{consumer_key}:{consumer_secret}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()

            headers = {'Authorization': f'Basic {encoded_auth}'}
            url = f'{base_url}/oauth/v1/generate?grant_type=client_credentials'

            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                token = data.get('access_token')
                if token:
                    return token
                current_app.logger.error("MPESA token response missing access_token: %s", data)
            else:
                current_app.logger.error("MPESA token error %s: %s", resp.status_code, resp.text)
        except Exception as exc:
            # log and return None (caller handles)
            try:
                current_app.logger.exception("get_access_token exception")
            except Exception:
                pass
        return None

    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """
        Initiate STK push.
        Returns dict: {'success': bool, 'checkout_request_id': str?, 'customer_message': str?, 'error': str?}
        """
        try:
            self._ensure_app_ctx()
            access_token = self.get_access_token()
            if not access_token:
                return {'success': False, 'error': 'Failed to obtain access token'}

            phone = self._normalize_phone(phone_number)
            if not phone:
                return {'success': False, 'error': 'Invalid phone number'}

            try:
                # Ensure amount is numeric
                amount_val = float(amount)
                if amount_val <= 0:
                    raise ValueError("Amount must be > 0")
            except Exception as e:
                return {'success': False, 'error': f'Invalid amount: {e}'}

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            passkey = self._get_cfg('MPESA_PASSKEY', required=True)
            business_shortcode = self._get_cfg('MPESA_BUSINESS_SHORTCODE', required=True)
            base_url = self._get_cfg('MPESA_BASE_URL', 'https://sandbox.safaricom.co.ke')
            callback_base = self._get_cfg('BASE_URL', None)

            if not callback_base:
                return {'success': False, 'error': 'Missing BASE_URL in config for callback'}

            password = base64.b64encode(f"{business_shortcode}{passkey}{timestamp}".encode()).decode()

            payload = {
                "BusinessShortCode": business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount_val),
                "PartyA": phone,
                "PartyB": business_shortcode,
                "PhoneNumber": phone,
                "CallBackURL": f"{callback_base.rstrip('/')}/api/payments/mpesa-callback",
                "AccountReference": account_reference,
                "TransactionDesc": transaction_desc
            }

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            resp = requests.post(f'{base_url}/mpesa/stkpush/v1/processrequest',
                                 json=payload, headers=headers, timeout=10)

            if resp.status_code == 200:
                result = resp.json()
                # Safaricom uses ResponseCode '0' for success
                if str(result.get('ResponseCode')) == '0':
                    return {
                        'success': True,
                        'checkout_request_id': result.get('CheckoutRequestID'),
                        'customer_message': result.get('CustomerMessage')
                    }
                # Return detailed error when present
                return {
                    'success': False,
                    'error': result.get('ResponseDescription') or result.get('errorMessage') or str(result),
                    'raw': result
                }
            else:
                current_app.logger.error("STK push HTTP %s: %s", resp.status_code, resp.text)
                return {'success': False, 'error': f'HTTP {resp.status_code}: {resp.text}'}

        except Exception as exc:
            try:
                current_app.logger.exception("stk_push exception")
            except Exception:
                pass
            return {'success': False, 'error': str(exc)}

    def check_transaction_status(self, checkout_request_id):
        """
        Query STK push status.
        Returns response JSON or {'success': False, 'error': '...'}
        """
        try:
            self._ensure_app_ctx()
            access_token = self.get_access_token()
            if not access_token:
                return {'success': False, 'error': 'Failed to obtain access token'}

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            passkey = self._get_cfg('MPESA_PASSKEY', required=True)
            business_shortcode = self._get_cfg('MPESA_BUSINESS_SHORTCODE', required=True)
            base_url = self._get_cfg('MPESA_BASE_URL', 'https://sandbox.safaricom.co.ke')

            password = base64.b64encode(f"{business_shortcode}{passkey}{timestamp}".encode()).decode()

            payload = {
                "BusinessShortCode": business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            resp = requests.post(f'{base_url}/mpesa/stkpushquery/v1/query',
                                 json=payload, headers=headers, timeout=10)

            if resp.status_code == 200:
                return resp.json()
            current_app.logger.error("STK status HTTP %s: %s", resp.status_code, resp.text)
            return {'success': False, 'error': f'HTTP {resp.status_code}: {resp.text}'}

        except Exception as exc:
            try:
                current_app.logger.exception("check_transaction_status exception")
            except Exception:
                pass
            return {'success': False, 'error': str(exc)}
