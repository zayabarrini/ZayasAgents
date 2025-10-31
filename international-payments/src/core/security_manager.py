import hashlib
import hmac
import secrets
import base64
from cryptography.fernet import Fernet
from typing import Dict, Any
from .models import SecurityContext


class SecurityManager:
    def __init__(self, encryption_key: bytes = None):
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.fernet = Fernet(self.encryption_key)

    def encrypt_sensitive_data(self, data: str) -> str:
        encrypted_data = self.fernet.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        decoded_data = base64.urlsafe_b64decode(encrypted_data)
        decrypted_data = self.fernet.decrypt(decoded_data)
        return decrypted_data.decode()

    def generate_payment_token(self, payment_data: Dict) -> str:
        data_string = self._normalize_payment_data(payment_data)
        return hashlib.sha256(data_string.encode()).hexdigest()

    def validate_payment_token(self, token: str, payment_data: Dict) -> bool:
        expected_token = self.generate_payment_token(payment_data)
        return hmac.compare_digest(token, expected_token)

    def _normalize_payment_data(self, payment_data: Dict) -> str:
        """Normalize payment data for consistent hashing"""
        normalized = {
            "amount": str(payment_data.get("amount", 0)),
            "currency": payment_data.get("currency", ""),
            "sender": payment_data.get("sender", {}).get("account_number", ""),
            "recipient": payment_data.get("recipient", {}).get("account_number", ""),
            "timestamp": payment_data.get("timestamp", ""),
        }
        return str(sorted(normalized.items()))
