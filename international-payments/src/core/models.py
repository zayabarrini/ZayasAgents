from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
from decimal import Decimal
from .constants import PaymentCurrency, Language, PaymentStatus, RiskLevel


@dataclass
class PaymentRequest:
    sender_data: Dict[str, Any]
    recipient_data: Dict[str, Any]
    amount: Decimal
    currency: PaymentCurrency
    target_currency: PaymentCurrency
    language: Language


@dataclass
class PaymentResponse:
    success: bool
    transaction_id: Optional[str] = None
    status: Optional[PaymentStatus] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    message: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class SecurityContext:
    user_ip: str
    user_agent: str
    device_fingerprint: Dict[str, Any]
    session_id: str


@dataclass
class ComplianceResult:
    aml_check: bool
    kyc_verified: bool
    sanction_screening: bool
    risk_level: RiskLevel
    required_documents: List[str]


@dataclass
class ExchangeRate:
    base_currency: PaymentCurrency
    target_currency: PaymentCurrency
    rate: Decimal
    timestamp: datetime
    source: str
