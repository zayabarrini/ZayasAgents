class PaymentProcessingError(Exception):
    """Base exception for payment processing errors"""

    pass


class SecurityViolationError(PaymentProcessingError):
    """Raised when security checks fail"""

    pass


class ComplianceCheckFailed(PaymentProcessingError):
    """Raised when compliance checks fail"""

    def __init__(self, reason: str, required_docs: list = None):
        self.reason = reason
        self.required_docs = required_docs or []
        super().__init__(f"Compliance check failed: {reason}")


class CurrencyConversionError(PaymentProcessingError):
    """Raised when currency conversion fails"""

    pass


class InsufficientFundsError(PaymentProcessingError):
    """Raised when user has insufficient funds"""

    pass


class RateLimitExceededError(PaymentProcessingError):
    """Raised when rate limit is exceeded"""

    pass
