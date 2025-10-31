from enum import Enum


class PaymentCurrency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    KRW = "KRW"
    RUB = "RUB"
    CHF = "CHF"
    ARS = "ARS"
    MXN = "MXN"
    INR = "INR"


class Language(Enum):
    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"
    IT = "it"
    RU = "ru"
    JA = "ja"
    KO = "ko"
    AR = "ar"
    HI = "hi"
    ZH = "zh"


class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class RiskLevel(Enum):
    MINIMAL = "MINIMAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# Regional codes
SUPPORTED_COUNTRIES = [
    "US",
    "GB",
    "DE",
    "FR",
    "IT",
    "ES",
    "RU",
    "CH",
    "JP",
    "KR",
    "AR",
    "MX",
    "IN",
]
