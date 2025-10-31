import asyncio
import aiohttp
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, Optional
from ..core.models import ExchangeRate, PaymentCurrency
from ..core.exceptions import CurrencyConversionError


class RealTimeExchangeRateService:
    def __init__(self, cache_duration_minutes: int = 5):
        self.cache = {}
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self.providers = ["ecb", "fixer", "openexchangerates"]

    async def get_exchange_rate(
        self, base_currency: PaymentCurrency, target_currency: PaymentCurrency
    ) -> ExchangeRate:
        if base_currency == target_currency:
            return ExchangeRate(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=Decimal("1.0"),
                timestamp=datetime.utcnow(),
                source="internal",
            )

        cache_key = f"{base_currency.value}_{target_currency.value}"
        cached_data = self.cache.get(cache_key)

        if (
            cached_data
            and datetime.utcnow() - cached_data.timestamp < self.cache_duration
        ):
            return cached_data

        # Try multiple providers
        for provider in self.providers:
            try:
                rate = await self._fetch_from_provider(
                    provider, base_currency, target_currency
                )
                if rate:
                    exchange_rate = ExchangeRate(
                        base_currency=base_currency,
                        target_currency=target_currency,
                        rate=rate,
                        timestamp=datetime.utcnow(),
                        source=provider,
                    )
                    self.cache[cache_key] = exchange_rate
                    return exchange_rate
            except Exception as e:
                continue

        # Fallback to cached rates even if expired
        if cached_data:
            return cached_data

        raise CurrencyConversionError(
            f"Could not fetch exchange rate for {base_currency.value} to {target_currency.value}"
        )

    async def _fetch_from_provider(
        self,
        provider: str,
        base_currency: PaymentCurrency,
        target_currency: PaymentCurrency,
    ) -> Optional[Decimal]:
        # Simulate API call - in production, implement actual API integration
        await asyncio.sleep(0.1)

        # Mock exchange rates
        mock_rates = {
            "USD_EUR": Decimal("0.85"),
            "USD_GBP": Decimal("0.73"),
            "USD_JPY": Decimal("110.5"),
            "USD_KRW": Decimal("1180.0"),
            "USD_RUB": Decimal("75.0"),
            "USD_CHF": Decimal("0.92"),
            "USD_ARS": Decimal("95.0"),
            "USD_MXN": Decimal("20.0"),
            "USD_INR": Decimal("74.0"),
            "EUR_USD": Decimal("1.18"),
            "EUR_GBP": Decimal("0.86"),
        }

        rate_key = f"{base_currency.value}_{target_currency.value}"
        return mock_rates.get(rate_key)

    def convert_amount(
        self,
        amount: Decimal,
        from_currency: PaymentCurrency,
        to_currency: PaymentCurrency,
    ) -> Decimal:
        if from_currency == to_currency:
            return amount

        rate_key = f"{from_currency.value}_{to_currency.value}"
        cached_rate = self.cache.get(rate_key)

        if cached_rate:
            return amount * cached_rate.rate

        # For demo purposes - in production, this would always use real rates
        mock_rates = {
            "USD_EUR": Decimal("0.85"),
            "EUR_USD": Decimal("1.18"),
        }

        rate = mock_rates.get(rate_key, Decimal("1.0"))
        return amount * rate
