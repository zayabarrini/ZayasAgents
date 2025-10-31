import asyncio
import logging
from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime
import secrets

from .models import PaymentRequest, PaymentResponse, SecurityContext
from .constants import PaymentCurrency, Language, PaymentStatus
from .exceptions import (
    PaymentProcessingError,
    SecurityViolationError,
    ComplianceCheckFailed,
)
from ..services.exchange_service import RealTimeExchangeRateService
from ..services.rate_limiter import RateLimiter
from ..regional.compliance_rules import RegionalComplianceRules
from ..regional.localization import MultiLanguageSupport
from ..agents.payment_agent import PaymentAgent
from .security_manager import SecurityManager


class InternationalPaymentProcessor:
    def __init__(self):
        self.security_manager = SecurityManager()
        self.exchange_service = RealTimeExchangeRateService()
        self.compliance_rules = RegionalComplianceRules()
        self.localization = MultiLanguageSupport()
        self.payment_agent = PaymentAgent(self.exchange_service, self.compliance_rules)
        self.rate_limiter = RateLimiter()
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("InternationalPaymentProcessor")
        logger.setLevel(logging.INFO)
        return logger

    async def process_payment(
        self,
        payment_request: PaymentRequest,
        security_context: Optional[SecurityContext] = None,
    ) -> PaymentResponse:
        try:
            # Validate input
            self._validate_payment_request(payment_request)

            # Rate limiting
            if security_context:
                self.rate_limiter.check_limit(security_context.user_ip, "payment")

            # Security checks
            security_result = await self._perform_security_checks(
                payment_request, security_context
            )
            if not security_result["approved"]:
                return self._create_error_response(
                    security_result["reason"], payment_request.language
                )

            # Currency conversion
            converted_amount = await self._convert_currency(
                payment_request.amount,
                payment_request.currency,
                payment_request.target_currency,
            )

            # Compliance checks
            compliance_result = await self._check_compliance(payment_request)
            if not compliance_result.aml_check:
                return self._create_compliance_error_response(
                    compliance_result, payment_request.language
                )

            # Execute payment
            payment_result = await self._execute_payment(
                payment_request, converted_amount
            )

            # Create success response
            return self._create_success_response(
                payment_result, payment_request.language
            )

        except PaymentProcessingError as e:
            self.logger.error(f"Payment processing failed: {str(e)}")
            return self._create_error_response(str(e), payment_request.language)
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return self._create_error_response(
                "INTERNAL_ERROR", payment_request.language
            )

    def _validate_payment_request(self, payment_request: PaymentRequest) -> None:
        """Validate payment request data"""
        if payment_request.amount <= Decimal("0"):
            raise PaymentProcessingError("Amount must be positive")

        required_sender = ["name", "account_number", "country"]
        for field in required_sender:
            if field not in payment_request.sender_data:
                raise PaymentProcessingError(f"Missing sender field: {field}")

        required_recipient = ["name", "account_number", "country"]
        for field in required_recipient:
            if field not in payment_request.recipient_data:
                raise PaymentProcessingError(f"Missing recipient field: {field}")

    async def _perform_security_checks(
        self,
        payment_request: PaymentRequest,
        security_context: Optional[SecurityContext],
    ) -> Dict[str, Any]:
        """Perform security checks"""
        # Basic amount check
        if payment_request.amount > Decimal("10000"):
            return {"approved": False, "reason": "AMOUNT_TOO_HIGH"}

        # Country restrictions
        restricted_countries = ["CU", "IR", "SY", "KP"]
        if (
            payment_request.recipient_data["country"] in restricted_countries
            or payment_request.sender_data["country"] in restricted_countries
        ):
            return {"approved": False, "reason": "RESTRICTED_COUNTRY"}

        # Additional security checks would go here
        await asyncio.sleep(0.05)  # Simulate security checks

        return {"approved": True, "reason": "SECURITY_APPROVED"}

    async def _convert_currency(
        self,
        amount: Decimal,
        from_currency: PaymentCurrency,
        to_currency: PaymentCurrency,
    ) -> Decimal:
        """Convert currency using real-time rates"""
        if from_currency == to_currency:
            return amount

        exchange_rate = await self.exchange_service.get_exchange_rate(
            from_currency, to_currency
        )
        return amount * exchange_rate.rate

    async def _check_compliance(self, payment_request: PaymentRequest) -> Any:
        """Check compliance with regulations"""
        sender_country = payment_request.sender_data["country"]
        recipient_country = payment_request.recipient_data["country"]
        amount = float(payment_request.amount)

        # Check sender country rules
        sender_rules = self.compliance_rules.get_country_rules(sender_country)
        if sender_rules and amount > sender_rules.get("max_amount", 0):
            raise ComplianceCheckFailed(
                f"AMOUNT_EXCEEDS_LIMIT_{sender_country}",
                sender_rules.get("required_docs", []),
            )

        # Check recipient country rules
        recipient_rules = self.compliance_rules.get_country_rules(recipient_country)
        if recipient_rules and amount > recipient_rules.get("max_amount", 0):
            raise ComplianceCheckFailed(
                f"AMOUNT_EXCEEDS_LIMIT_{recipient_country}",
                recipient_rules.get("required_docs", []),
            )

        # Simulate compliance check
        await asyncio.sleep(0.05)

        # Return compliance result (simplified)
        from ..core.models import ComplianceResult
        from ..core.constants import RiskLevel

        return ComplianceResult(
            aml_check=True,
            kyc_verified=True,
            sanction_screening=True,
            risk_level=RiskLevel.LOW,
            required_documents=[],
        )

    async def _execute_payment(
        self, payment_request: PaymentRequest, converted_amount: Decimal
    ) -> Dict[str, Any]:
        """Execute the payment transaction"""
        # Simulate payment processing
        await asyncio.sleep(0.1)

        transaction_id = f"TXN{secrets.token_hex(8).upper()}"

        return {
            "transaction_id": transaction_id,
            "status": PaymentStatus.COMPLETED,
            "amount": float(converted_amount),
            "currency": payment_request.target_currency.value,
            "timestamp": datetime.utcnow().isoformat(),
            "sender_reference": self.security_manager.encrypt_sensitive_data(
                payment_request.sender_data["account_number"]
            ),
            "recipient_reference": self.security_manager.encrypt_sensitive_data(
                payment_request.recipient_data["account_number"]
            ),
        }

    def _create_success_response(
        self, payment_result: Dict[str, Any], language: Language
    ) -> PaymentResponse:
        """Create success response"""
        message = self.localization.get_message(
            "payment_success",
            language,
            {
                "amount": payment_result["amount"],
                "currency": payment_result["currency"],
                "transaction_id": payment_result["transaction_id"],
            },
        )

        return PaymentResponse(
            success=True,
            transaction_id=payment_result["transaction_id"],
            status=payment_result["status"].value,
            amount=payment_result["amount"],
            currency=payment_result["currency"],
            message=message,
            timestamp=payment_result["timestamp"],
        )

    def _create_error_response(
        self, error_reason: str, language: Language
    ) -> PaymentResponse:
        """Create error response"""
        message = self.localization.get_message(
            "payment_failed", language, {"reason": error_reason}
        )

        return PaymentResponse(
            success=False,
            error_code=error_reason,
            message=message,
            timestamp=datetime.utcnow().isoformat(),
        )

    def _create_compliance_error_response(
        self, compliance_result: Any, language: Language
    ) -> PaymentResponse:
        """Create compliance error response"""
        documents_str = ", ".join(compliance_result.required_documents)
        message = self.localization.get_message(
            "compliance_check_failed", language, {"documents": documents_str}
        )

        return PaymentResponse(
            success=False,
            error_code="COMPLIANCE_CHECK_FAILED",
            message=message,
            timestamp=datetime.utcnow().isoformat(),
        )
