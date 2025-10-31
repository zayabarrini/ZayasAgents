"""
AI-powered fraud detection system for international payments
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from decimal import Decimal
from collections import defaultdict
import logging

from ..core.models import PaymentRequest
from ..core.constants import RiskLevel


class FraudDetectionSystem:
    def __init__(self):
        self.transaction_history = defaultdict(list)
        self.suspicious_patterns = self._load_suspicious_patterns()
        self.risk_thresholds = {"high": 70, "medium": 40, "low": 20}
        self.logger = logging.getLogger("FraudDetectionSystem")

    def _load_suspicious_patterns(self) -> Dict[str, Any]:
        """Load known suspicious patterns and rules"""
        return {
            "amount_patterns": {
                "round_numbers": [1000, 5000, 10000],
                "just_below_threshold": [999, 4999, 9999],
            },
            "time_patterns": {
                "off_hours": [0, 1, 2, 3, 4, 5],  # Midnight to 5 AM
                "rapid_successive": 300,  # 5 minutes in seconds
            },
            "geographic_patterns": {
                "high_risk_countries": ["RU", "AR", "MX", "NG", "VE"],
                "unusual_routes": [("US", "RU"), ("GB", "VE"), ("DE", "NG")],
            },
            "behavioral_patterns": {
                "new_recipient_risk": 3,  # Max new recipients per day
                "velocity_limits": {
                    "daily_amount": 50000,
                    "daily_count": 10,
                    "hourly_count": 3,
                },
            },
        }

    async def analyze_transaction_risk(
        self,
        payment_request: PaymentRequest,
        user_behavior: Dict[str, Any],
        security_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Comprehensive fraud risk analysis"""

        risk_score = 0
        risk_factors = []
        recommendations = []

        # 1. Amount-based analysis
        amount_risk = await self._analyze_amount_patterns(payment_request.amount)
        risk_score += amount_risk["score"]
        risk_factors.extend(amount_risk["factors"])

        # 2. Geographic analysis
        geo_risk = await self._analyze_geographic_patterns(payment_request)
        risk_score += geo_risk["score"]
        risk_factors.extend(geo_risk["factors"])

        # 3. Behavioral analysis
        behavior_risk = await self._analyze_behavioral_patterns(user_behavior)
        risk_score += behavior_risk["score"]
        risk_factors.extend(behavior_risk["factors"])

        # 4. Temporal analysis
        temporal_risk = await self._analyze_temporal_patterns()
        risk_score += temporal_risk["score"]
        risk_factors.extend(temporal_risk["factors"])

        # 5. Device and IP analysis
        if security_context:
            device_risk = await self._analyze_device_patterns(security_context)
            risk_score += device_risk["score"]
            risk_factors.extend(device_risk["factors"])

        # Determine risk level
        risk_level = self._calculate_risk_level(risk_score)

        # Generate recommendations
        if risk_level == RiskLevel.HIGH:
            recommendations = [
                "BLOCK",
                "REQUIRE_MANUAL_REVIEW",
                "REQUEST_ADDITIONAL_VERIFICATION",
            ]
        elif risk_level == RiskLevel.MEDIUM:
            recommendations = ["REQUIRE_2FA", "LIMIT_AMOUNT", "ENHANCED_MONITORING"]
        else:
            recommendations = ["PROCEED", "STANDARD_MONITORING"]

        return {
            "risk_score": risk_score,
            "risk_level": risk_level.value,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "confidence": self._calculate_confidence(risk_factors),
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }

    async def _analyze_amount_patterns(self, amount: Decimal) -> Dict[str, Any]:
        """Analyze amount-based risk patterns"""
        risk_score = 0
        factors = []

        amount_float = float(amount)

        # Check for round numbers (common in fraudulent transactions)
        if amount_float in self.suspicious_patterns["amount_patterns"]["round_numbers"]:
            risk_score += 15
            factors.append("ROUND_AMOUNT")

        # Check for amounts just below reporting thresholds
        if (
            amount_float
            in self.suspicious_patterns["amount_patterns"]["just_below_threshold"]
        ):
            risk_score += 20
            factors.append("JUST_BELOW_THRESHOLD")

        # Large amount check
        if amount_float > 10000:
            risk_score += 25
            factors.append("LARGE_AMOUNT")

        return {"score": risk_score, "factors": factors}

    async def _analyze_geographic_patterns(
        self, payment_request: PaymentRequest
    ) -> Dict[str, Any]:
        """Analyze geographic risk patterns"""
        risk_score = 0
        factors = []

        sender_country = payment_request.sender_data.get("country", "")
        recipient_country = payment_request.recipient_data.get("country", "")

        # High-risk country check
        if (
            recipient_country
            in self.suspicious_patterns["geographic_patterns"]["high_risk_countries"]
        ):
            risk_score += 30
            factors.append("HIGH_RISK_COUNTRY")

        # Unusual route check
        route = (sender_country, recipient_country)
        if route in self.suspicious_patterns["geographic_patterns"]["unusual_routes"]:
            risk_score += 25
            factors.append("UNUSUAL_GEOGRAPHIC_ROUTE")

        # Distance-based risk (simplified)
        if sender_country != recipient_country:
            risk_score += 10
            factors.append("CROSS_BORDER_TRANSACTION")

        return {"score": risk_score, "factors": factors}

    async def _analyze_behavioral_patterns(
        self, user_behavior: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        risk_score = 0
        factors = []

        # Transaction velocity
        daily_count = user_behavior.get("transaction_count_24h", 0)
        if (
            daily_count
            > self.suspicious_patterns["behavioral_patterns"]["velocity_limits"][
                "daily_count"
            ]
        ):
            risk_score += 20
            factors.append("HIGH_TRANSACTION_FREQUENCY")

        hourly_count = user_behavior.get("transaction_count_1h", 0)
        if (
            hourly_count
            > self.suspicious_patterns["behavioral_patterns"]["velocity_limits"][
                "hourly_count"
            ]
        ):
            risk_score += 25
            factors.append("RAPID_SUCCESSIVE_TRANSACTIONS")

        # Amount velocity
        daily_amount = user_behavior.get("total_amount_24h", 0)
        if (
            daily_amount
            > self.suspicious_patterns["behavioral_patterns"]["velocity_limits"][
                "daily_amount"
            ]
        ):
            risk_score += 30
            factors.append("HIGH_DAILY_VOLUME")

        # New recipient patterns
        new_recipients = user_behavior.get("new_recipients_today", 0)
        if (
            new_recipients
            > self.suspicious_patterns["behavioral_patterns"]["new_recipient_risk"]
        ):
            risk_score += 15
            factors.append("MULTIPLE_NEW_RECIPIENTS")

        return {"score": risk_score, "factors": factors}

    async def _analyze_temporal_patterns(self) -> Dict[str, Any]:
        """Analyze temporal risk patterns"""
        risk_score = 0
        factors = []

        current_hour = datetime.utcnow().hour

        # Off-hours transaction check
        if current_hour in self.suspicious_patterns["time_patterns"]["off_hours"]:
            risk_score += 15
            factors.append("OFF_HOURS_TRANSACTION")

        # Weekend transactions (higher risk)
        if datetime.utcnow().weekday() >= 5:  # Saturday or Sunday
            risk_score += 10
            factors.append("WEEKEND_TRANSACTION")

        return {"score": risk_score, "factors": factors}

    async def _analyze_device_patterns(
        self, security_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze device and IP patterns"""
        risk_score = 0
        factors = []

        # IP reputation check (simplified)
        ip_address = security_context.get("user_ip", "")
        if self._is_suspicious_ip(ip_address):
            risk_score += 25
            factors.append("SUSPICIOUS_IP")

        # Device fingerprint analysis
        device_fingerprint = security_context.get("device_fingerprint", {})
        if not device_fingerprint:
            risk_score += 10
            factors.append("MISSING_DEVICE_FINGERPRINT")

        return {"score": risk_score, "factors": factors}

    def _is_suspicious_ip(self, ip_address: str) -> bool:
        """Check if IP is suspicious (simplified)"""
        # In production, integrate with IP reputation services
        suspicious_prefixes = ["192.168.", "10.0.", "172.16."]  # Private IPs
        return any(ip_address.startswith(prefix) for prefix in suspicious_prefixes)

    def _calculate_risk_level(self, risk_score: int) -> RiskLevel:
        """Calculate risk level based on score"""
        if risk_score >= self.risk_thresholds["high"]:
            return RiskLevel.HIGH
        elif risk_score >= self.risk_thresholds["medium"]:
            return RiskLevel.MEDIUM
        elif risk_score >= self.risk_thresholds["low"]:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL

    def _calculate_confidence(self, risk_factors: List[str]) -> float:
        """Calculate confidence level in fraud detection"""
        if not risk_factors:
            return 0.95  # High confidence for low risk

        factor_weights = {
            "HIGH_RISK_COUNTRY": 0.8,
            "LARGE_AMOUNT": 0.7,
            "RAPID_SUCCESSIVE_TRANSACTIONS": 0.75,
            "SUSPICIOUS_IP": 0.9,
            "JUST_BELOW_THRESHOLD": 0.6,
        }

        total_weight = sum(factor_weights.get(factor, 0.5) for factor in risk_factors)
        confidence = max(
            0.1, 1.0 - (total_weight / len(risk_factors) if risk_factors else 0)
        )

        return round(confidence, 2)

    async def update_behavior_profile(
        self, user_id: str, transaction_data: Dict[str, Any]
    ) -> None:
        """Update user behavior profile with new transaction"""
        if user_id not in self.transaction_history:
            self.transaction_history[user_id] = []

        self.transaction_history[user_id].append(
            {**transaction_data, "timestamp": datetime.utcnow().isoformat()}
        )

        # Keep only last 100 transactions per user
        if len(self.transaction_history[user_id]) > 100:
            self.transaction_history[user_id] = self.transaction_history[user_id][-100:]

    def get_user_behavior_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user behavior for risk assessment"""
        user_transactions = self.transaction_history.get(user_id, [])

        now = datetime.utcnow()
        last_24h = [
            t
            for t in user_transactions
            if datetime.fromisoformat(t["timestamp"]) > now - timedelta(hours=24)
        ]
        last_1h = [
            t
            for t in user_transactions
            if datetime.fromisoformat(t["timestamp"]) > now - timedelta(hours=1)
        ]

        return {
            "transaction_count_24h": len(last_24h),
            "transaction_count_1h": len(last_1h),
            "total_amount_24h": sum(t.get("amount", 0) for t in last_24h),
            "new_recipients_today": len(
                set(t.get("recipient_country", "") for t in last_24h)
            ),
            "last_transaction_time": (
                user_transactions[-1]["timestamp"] if user_transactions else None
            ),
        }
