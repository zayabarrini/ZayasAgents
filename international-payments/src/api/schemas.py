from pydantic import BaseModel, Field, validator
from decimal import Decimal
from typing import Dict, Optional, List
from ..core.constants import PaymentCurrency, Language


class PaymentRequestSchema(BaseModel):
    sender_data: Dict[str, str] = Field(..., description="Sender information")
    recipient_data: Dict[str, str] = Field(..., description="Recipient information")
    amount: Decimal = Field(..., gt=0, description="Payment amount")
    currency: PaymentCurrency = Field(..., description="Source currency")
    target_currency: PaymentCurrency = Field(..., description="Target currency")
    language: Language = Field(Language.EN, description="Response language")

    @validator("sender_data")
    def validate_sender_data(cls, v):
        required_fields = ["name", "account_number", "country"]
        for field in required_fields:
            if field not in v:
                raise ValueError(f"Missing required sender field: {field}")
        return v

    @validator("recipient_data")
    def validate_recipient_data(cls, v):
        required_fields = ["name", "account_number", "country"]
        for field in required_fields:
            if field not in v:
                raise ValueError(f"Missing required recipient field: {field}")
        return v


class PaymentResponseSchema(BaseModel):
    success: bool
    transaction_id: Optional[str]
    status: Optional[str]
    amount: Optional[float]
    currency: Optional[str]
    message: Optional[str]
    error_code: Optional[str]
    timestamp: Optional[str]
    security_level: Optional[str]
    compliance_status: Optional[str]


class ExchangeRateRequestSchema(BaseModel):
    base_currency: PaymentCurrency
    target_currency: PaymentCurrency


class ExchangeRateResponseSchema(BaseModel):
    base_currency: str
    target_currency: str
    rate: float
    timestamp: str
    source: str


class ComplianceCheckSchema(BaseModel):
    sender_country: str
    recipient_country: str
    amount: float
    currency: str


class ComplianceResponseSchema(BaseModel):
    aml_check: bool
    kyc_verified: bool
    risk_level: str
    required_documents: List[str]
