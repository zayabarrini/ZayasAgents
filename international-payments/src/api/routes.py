from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any
from decimal import Decimal

from .schemas import (
    PaymentRequestSchema,
    PaymentResponseSchema,
    ExchangeRateRequestSchema,
    ExchangeRateResponseSchema,
    ComplianceCheckSchema,
    ComplianceResponseSchema,
)
from ..core.payment_processor import InternationalPaymentProcessor
from ..core.models import PaymentRequest, SecurityContext
from ..core.constants import PaymentCurrency, Language
from ..services.exchange_service import RealTimeExchangeRateService
from ..regional.compliance_rules import RegionalComplianceRules

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


# Dependency injections
def get_payment_processor():
    return InternationalPaymentProcessor()


def get_exchange_service():
    return RealTimeExchangeRateService()


def get_compliance_rules():
    return RegionalComplianceRules()


@router.post("/process", response_model=PaymentResponseSchema)
async def process_payment(
    request: Request,
    payment_data: PaymentRequestSchema,
    processor: InternationalPaymentProcessor = Depends(get_payment_processor),
):
    """
    Process an international payment with security and compliance checks
    """
    try:
        # Create security context from request
        security_context = SecurityContext(
            user_ip=request.client.host if request.client else "0.0.0.0",
            user_agent=request.headers.get("user-agent", "Unknown"),
            device_fingerprint={},  # Would be generated from request details
            session_id=request.headers.get("x-session-id", "unknown"),
        )

        # Convert to internal model
        payment_request = PaymentRequest(
            sender_data=payment_data.sender_data,
            recipient_data=payment_data.recipient_data,
            amount=payment_data.amount,
            currency=payment_data.currency,
            target_currency=payment_data.target_currency,
            language=payment_data.language,
        )

        # Process payment
        result = await processor.process_payment(payment_request, security_context)

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/exchange-rate", response_model=ExchangeRateResponseSchema)
async def get_exchange_rate(
    base_currency: PaymentCurrency,
    target_currency: PaymentCurrency,
    exchange_service: RealTimeExchangeRateService = Depends(get_exchange_service),
):
    """
    Get real-time exchange rate between two currencies
    """
    try:
        rate = await exchange_service.get_exchange_rate(base_currency, target_currency)

        return ExchangeRateResponseSchema(
            base_currency=rate.base_currency.value,
            target_currency=rate.target_currency.value,
            rate=float(rate.rate),
            timestamp=rate.timestamp.isoformat(),
            source=rate.source,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compliance-check", response_model=ComplianceResponseSchema)
async def check_compliance(
    compliance_data: ComplianceCheckSchema,
    compliance_rules: RegionalComplianceRules = Depends(get_compliance_rules),
):
    """
    Check compliance requirements for a potential payment
    """
    try:
        sender_rules = compliance_rules.get_country_rules(
            compliance_data.sender_country
        )
        recipient_rules = compliance_rules.get_country_rules(
            compliance_data.recipient_country
        )

        # Determine required documents
        required_docs = []
        if sender_rules:
            required_docs.extend(
                compliance_rules.get_required_documents(
                    compliance_data.sender_country, compliance_data.amount
                )
            )
        if recipient_rules:
            required_docs.extend(
                compliance_rules.get_required_documents(
                    compliance_data.recipient_country, compliance_data.amount
                )
            )

        # Simplified compliance result
        from ..core.models import ComplianceResult
        from ..core.constants import RiskLevel

        compliance_result = ComplianceResult(
            aml_check=True,
            kyc_verified=len(required_docs) == 0,
            sanction_screening=True,
            risk_level=RiskLevel.LOW if len(required_docs) == 0 else RiskLevel.MEDIUM,
            required_documents=list(set(required_docs)),
        )

        return ComplianceResponseSchema(
            aml_check=compliance_result.aml_check,
            kyc_verified=compliance_result.kyc_verified,
            risk_level=compliance_result.risk_level.value,
            required_documents=compliance_result.required_documents,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/supported-currencies")
async def get_supported_currencies():
    """
    Get list of supported currencies
    """
    return {
        "currencies": [currency.value for currency in PaymentCurrency],
        "count": len(PaymentCurrency),
    }


@router.get("/supported-languages")
async def get_supported_languages():
    """
    Get list of supported languages
    """
    return {"languages": [lang.value for lang in Language], "count": len(Language)}


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "International Payment Processor",
    }
