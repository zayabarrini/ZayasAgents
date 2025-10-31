from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from decimal import Decimal
from collections import defaultdict
import asyncio

from ..core.models import PaymentRequest
from ..core.constants import PaymentCurrency, PaymentStatus


class PaymentAnalytics:
    def __init__(self):
        self.transaction_data = []
        self.user_behavior = defaultdict(
            lambda: {
                "transaction_count_24h": 0,
                "total_amount_24h": Decimal("0"),
                "last_transaction_time": None,
                "preferred_currencies": defaultdict(int),
                "common_recipients": defaultdict(int),
            }
        )

    async def record_transaction(self, transaction: Dict[str, Any]) -> None:
        """Record a transaction for analytics"""
        self.transaction_data.append(transaction)

        # Update user behavior
        user_id = transaction.get("user_id", "anonymous")
        user_data = self.user_behavior[user_id]

        # Update counts and amounts
        user_data["transaction_count_24h"] += 1
        user_data["total_amount_24h"] += Decimal(str(transaction.get("amount", 0)))
        user_data["last_transaction_time"] = datetime.utcnow()

        # Update preferences
        currency = transaction.get("currency")
        if currency:
            user_data["preferred_currencies"][currency] += 1

        recipient = transaction.get("recipient_country")
        if recipient:
            user_data["common_recipients"][recipient] += 1

        # Clean up old data periodically
        self._clean_old_data()

    async def analyze_payment_patterns(
        self, user_id: str, time_range: str = "30d"
    ) -> Dict[str, Any]:
        """Analyze user's payment patterns"""
        user_transactions = await self._get_user_transactions(user_id, time_range)

        if not user_transactions:
            return {"error": "No transactions found"}

        analysis = {
            "behavior_patterns": self._analyze_behavior_patterns(user_transactions),
            "risk_indicators": await self._detect_risk_indicators(user_transactions),
            "spending_insights": self._generate_spending_insights(user_transactions),
            "anomaly_detection": await self._detect_anomalies(user_transactions),
            "optimization_suggestions": self._generate_optimization_suggestions(
                user_transactions
            ),
        }

        return analysis

    def _analyze_behavior_patterns(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Analyze behavioral patterns in transactions"""
        amounts = [t.get("amount", 0) for t in transactions]
        currencies = [t.get("currency", "") for t in transactions if t.get("currency")]
        countries = [
            t.get("recipient_country", "")
            for t in transactions
            if t.get("recipient_country")
        ]

        return {
            "avg_transaction_amount": sum(amounts) / len(amounts) if amounts else 0,
            "preferred_currencies": self._get_most_common(currencies),
            "common_destinations": self._get_most_common(countries),
            "transaction_frequency": len(transactions),
            "amount_variability": max(amounts) - min(amounts) if amounts else 0,
            "success_rate": len(
                [
                    t
                    for t in transactions
                    if t.get("status") == PaymentStatus.COMPLETED.value
                ]
            )
            / len(transactions),
        }

    async def _detect_risk_indicators(self, transactions: List[Dict]) -> List[str]:
        """Detect potential risk indicators"""
        risk_indicators = []

        if len(transactions) >= 3:
            # Check for rapid successive transactions
            timestamps = [
                datetime.fromisoformat(t["timestamp"])
                for t in transactions
                if t.get("timestamp")
            ]
            if len(timestamps) >= 2:
                time_diffs = [
                    (timestamps[i + 1] - timestamps[i]).total_seconds()
                    for i in range(len(timestamps) - 1)
                ]

                if any(diff < 300 for diff in time_diffs):  # 5 minutes
                    risk_indicators.append("RAPID_SUCCESSIVE_TRANSACTIONS")

        # Check for multiple countries in short period
        if len(transactions) >= 2:
            unique_countries = set(t.get("recipient_country", "") for t in transactions)
            if len(unique_countries) >= 3:
                risk_indicators.append("MULTIPLE_COUNTRIES_SHORT_TIME")

        # Check for unusual amounts
        amounts = [t.get("amount", 0) for t in transactions]
        if amounts:
            avg_amount = sum(amounts) / len(amounts)
            if any(amount > avg_amount * 5 for amount in amounts):
                risk_indicators.append("UNUSUALLY_LARGE_AMOUNT")

        return risk_indicators

    def _generate_spending_insights(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Generate spending insights"""
        total_spent = sum(t.get("amount", 0) for t in transactions)
        currency_distribution = defaultdict(float)

        for transaction in transactions:
            currency = transaction.get("currency", "UNKNOWN")
            amount = transaction.get("amount", 0)
            currency_distribution[currency] += amount

        return {
            "total_spent": total_spent,
            "currency_distribution": dict(currency_distribution),
            "average_transaction_size": (
                total_spent / len(transactions) if transactions else 0
            ),
            "largest_transaction": (
                max([t.get("amount", 0) for t in transactions]) if transactions else 0
            ),
        }

    async def _detect_anomalies(self, transactions: List[Dict]) -> List[Dict[str, Any]]:
        """Detect anomalous transactions"""
        anomalies = []

        if not transactions:
            return anomalies

        amounts = [t.get("amount", 0) for t in transactions]
        avg_amount = sum(amounts) / len(amounts)
        std_amount = (sum((x - avg_amount) ** 2 for x in amounts) / len(amounts)) ** 0.5

        for transaction in transactions[-10:]:  # Check last 10 transactions
            amount = transaction.get("amount", 0)
            if amount > avg_amount + 2 * std_amount:
                anomalies.append(
                    {
                        "transaction_id": transaction.get("transaction_id"),
                        "type": "UNUSUALLY_LARGE_AMOUNT",
                        "amount": amount,
                        "expected_range": f"up to {avg_amount + std_amount:.2f}",
                    }
                )

        return anomalies

    def _generate_optimization_suggestions(self, transactions: List[Dict]) -> List[str]:
        """Generate optimization suggestions"""
        suggestions = []

        # Analyze currency patterns
        currencies = [t.get("currency", "") for t in transactions if t.get("currency")]
        if currencies:
            most_common_currency = self._get_most_common(currencies)
            if most_common_currency and len(set(currencies)) > 1:
                suggestions.append(
                    f"Consider using {most_common_currency} for most transactions to reduce conversion fees"
                )

        # Analyze timing patterns
        if len(transactions) > 5:
            suggestions.append(
                "Consider batching smaller payments to reduce transaction fees"
            )

        return suggestions

    def _get_most_common(self, items: List) -> Any:
        """Get most common item from list"""
        if not items:
            return None
        return max(set(items), key=items.count)

    async def _get_user_transactions(self, user_id: str, time_range: str) -> List[Dict]:
        """Get user transactions for time range (simplified)"""
        # In production, this would query a database
        cutoff_days = int(time_range[:-1]) if time_range.endswith("d") else 30
        cutoff_date = datetime.utcnow() - timedelta(days=cutoff_days)

        return [
            t
            for t in self.transaction_data
            if t.get("user_id") == user_id
            and datetime.fromisoformat(t.get("timestamp", "2000-01-01")) >= cutoff_date
        ]

    def _clean_old_data(self):
        """Clean up data older than 90 days"""
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        self.transaction_data = [
            t
            for t in self.transaction_data
            if datetime.fromisoformat(t.get("timestamp", "2000-01-01")) >= cutoff_date
        ]
