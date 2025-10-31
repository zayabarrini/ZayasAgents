"""
AI agent for optimizing international payment routes
"""

import asyncio
from decimal import Decimal
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

from ..core.constants import PaymentCurrency
from ..core.models import PaymentRequest


class RouteOptimizer:
    def __init__(self, exchange_service, compliance_service):
        self.exchange_service = exchange_service
        self.compliance_service = compliance_service
        self.route_cache = {}
        self.cache_duration = timedelta(minutes=30)
        self.logger = logging.getLogger("RouteOptimizer")

    async def find_optimal_route(
        self, payment_request: PaymentRequest, optimization_criteria: List[str] = None
    ) -> Dict[str, Any]:
        """Find optimal payment route based on multiple criteria"""

        if optimization_criteria is None:
            optimization_criteria = ["cost", "speed", "reliability"]

        # Get available routes
        available_routes = await self._get_available_routes(payment_request)

        if not available_routes:
            raise ValueError("No payment routes available for this transaction")

        # Score routes based on optimization criteria
        scored_routes = []
        for route in available_routes:
            score = await self._calculate_route_score(
                route, optimization_criteria, payment_request
            )
            scored_routes.append(
                {
                    **route,
                    "optimization_score": score,
                    "recommendation_reason": self._get_recommendation_reason(
                        route, score
                    ),
                }
            )

        # Sort by optimization score (descending)
        scored_routes.sort(key=lambda x: x["optimization_score"], reverse=True)

        optimal_route = scored_routes[0]

        return {
            "optimal_route": optimal_route,
            "alternative_routes": scored_routes[1:4],  # Top 3 alternatives
            "optimization_criteria": optimization_criteria,
            "route_count": len(available_routes),
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }

    async def _get_available_routes(
        self, payment_request: PaymentRequest
    ) -> List[Dict[str, Any]]:
        """Get available payment routes for the transaction"""

        cache_key = self._generate_route_cache_key(payment_request)
        cached_routes = self.route_cache.get(cache_key)

        if (
            cached_routes
            and datetime.utcnow() - cached_routes["timestamp"] < self.cache_duration
        ):
            return cached_routes["routes"]

        # Simulate route discovery - in production, integrate with actual payment networks
        routes = await self._discover_routes(payment_request)

        # Cache the results
        self.route_cache[cache_key] = {"routes": routes, "timestamp": datetime.utcnow()}

        return routes

    async def _discover_routes(
        self, payment_request: PaymentRequest
    ) -> List[Dict[str, Any]]:
        """Discover available payment routes"""

        sender_country = payment_request.sender_data.get("country", "")
        recipient_country = payment_request.recipient_data.get("country", "")
        amount = payment_request.amount
        currency = payment_request.currency

        # Simulate API calls to various payment networks
        await asyncio.sleep(0.1)

        base_routes = [
            {
                "route_id": "SWIFT",
                "name": "SWIFT International Transfer",
                "provider": "SWIFT",
                "estimated_cost": float(amount * Decimal("0.01")),  # 1%
                "estimated_time_hours": 24,
                "success_rate": 0.98,
                "currencies": [c.value for c in PaymentCurrency],
                "supported_countries": ["ALL"],
                "features": ["tracking", "insurance", "compliance"],
                "limitations": ["higher_fees", "slower_settlement"],
                "reliability": "very_high",
            },
            {
                "route_id": "SEPA",
                "name": "SEPA Credit Transfer",
                "provider": "European Banking",
                "estimated_cost": float(amount * Decimal("0.005")),  # 0.5%
                "estimated_time_hours": 1,
                "success_rate": 0.99,
                "currencies": ["EUR"],
                "supported_countries": ["EU"],
                "features": ["fast_settlement", "low_fees", "standardized"],
                "limitations": ["euro_only", "europe_only"],
                "reliability": "very_high",
            },
            {
                "route_id": "LOCAL_NETWORK",
                "name": "Local Banking Network",
                "provider": "Local Banks",
                "estimated_cost": float(amount * Decimal("0.002")),  # 0.2%
                "estimated_time_hours": 2,
                "success_rate": 0.995,
                "currencies": [currency.value],
                "supported_countries": [sender_country, recipient_country],
                "features": ["lowest_fees", "fast_settlement", "direct"],
                "limitations": ["limited_coverage", "currency_restrictions"],
                "reliability": "high",
            },
            {
                "route_id": "DIGITAL_WALLET",
                "name": "Digital Wallet Transfer",
                "provider": "FinTech Partner",
                "estimated_cost": float(amount * Decimal("0.015")),  # 1.5%
                "estimated_time_hours": 0.5,
                "success_rate": 0.97,
                "currencies": ["USD", "EUR", "GBP"],
                "supported_countries": ["US", "GB", "EU", "CA", "AU"],
                "features": ["instant_settlement", "mobile_friendly", "low_limits"],
                "limitations": ["higher_fees", "country_restrictions"],
                "reliability": "medium",
            },
        ]

        # Filter routes based on compatibility
        compatible_routes = []
        for route in base_routes:
            if self._is_route_compatible(route, payment_request):
                # Adjust estimates based on specific factors
                adjusted_route = await self._adjust_route_estimates(
                    route, payment_request
                )
                compatible_routes.append(adjusted_route)

        return compatible_routes

    def _is_route_compatible(
        self, route: Dict[str, Any], payment_request: PaymentRequest
    ) -> bool:
        """Check if route is compatible with payment request"""

        # Check currency support
        if payment_request.target_currency.value not in route["currencies"]:
            return False

        # Check country support
        sender_country = payment_request.sender_data.get("country", "")
        recipient_country = payment_request.recipient_data.get("country", "")

        if "ALL" not in route["supported_countries"]:
            if (
                sender_country not in route["supported_countries"]
                or recipient_country not in route["supported_countries"]
            ):
                return False

        return True

    async def _adjust_route_estimates(
        self, route: Dict[str, Any], payment_request: PaymentRequest
    ) -> Dict[str, Any]:
        """Adjust route estimates based on specific factors"""

        adjusted_route = route.copy()
        amount = payment_request.amount
        sender_country = payment_request.sender_data.get("country", "")
        recipient_country = payment_request.recipient_data.get("country", "")

        # Adjust cost based on amount (bulk discounts)
        if amount > Decimal("10000"):
            adjusted_route["estimated_cost"] *= 0.8  # 20% discount for large amounts
        elif amount < Decimal("100"):
            adjusted_route["estimated_cost"] *= 1.2  # 20% premium for small amounts

        # Adjust time based on countries
        if sender_country == recipient_country:
            adjusted_route["estimated_time_hours"] *= 0.5  # Domestic is faster

        # Adjust for high-risk countries
        high_risk_countries = ["RU", "AR", "MX", "NG"]
        if recipient_country in high_risk_countries:
            adjusted_route[
                "estimated_time_hours"
            ] *= 1.5  # Additional compliance checks
            adjusted_route["success_rate"] *= 0.95  # Slightly lower success rate

        return adjusted_route

    async def _calculate_route_score(
        self,
        route: Dict[str, Any],
        criteria: List[str],
        payment_request: PaymentRequest,
    ) -> float:
        """Calculate optimization score for a route"""

        score_weights = {"cost": 0.4, "speed": 0.3, "reliability": 0.3}

        # Normalize weights based on provided criteria
        total_weight = sum(score_weights.get(c, 0) for c in criteria)
        normalized_weights = {
            c: score_weights.get(c, 0) / total_weight for c in criteria
        }

        score = 0

        for criterion in criteria:
            if criterion == "cost":
                # Lower cost = higher score
                max_reasonable_cost = float(
                    payment_request.amount * Decimal("0.05")
                )  # 5% as max
                cost_score = 1.0 - min(
                    route["estimated_cost"] / max_reasonable_cost, 1.0
                )
                score += cost_score * normalized_weights[criterion]

            elif criterion == "speed":
                # Faster = higher score (inverse relationship)
                max_reasonable_time = 72  # hours
                speed_score = 1.0 - (
                    route["estimated_time_hours"] / max_reasonable_time
                )
                score += speed_score * normalized_weights[criterion]

            elif criterion == "reliability":
                # Higher reliability = higher score
                reliability_score = route["success_rate"]
                score += reliability_score * normalized_weights[criterion]

        return round(score, 3)

    def _get_recommendation_reason(self, route: Dict[str, Any], score: float) -> str:
        """Generate human-readable recommendation reason"""

        reasons = []

        if route["estimated_cost"] < route.get(
            "average_cost", route["estimated_cost"] * 1.5
        ):
            reasons.append("low cost")

        if route["estimated_time_hours"] < 4:
            reasons.append("fast settlement")

        if route["success_rate"] > 0.98:
            reasons.append("high reliability")

        if not reasons:
            reasons.append("best overall balance")

        return f"Recommended due to {', '.join(reasons)}"

    def _generate_route_cache_key(self, payment_request: PaymentRequest) -> str:
        """Generate cache key for route discovery"""
        key_parts = [
            payment_request.sender_data.get("country", ""),
            payment_request.recipient_data.get("country", ""),
            payment_request.currency.value,
            payment_request.target_currency.value,
            str(payment_request.amount),
        ]
        return "_".join(key_parts)

    async def get_route_comparison(
        self, payment_request: PaymentRequest
    ) -> Dict[str, Any]:
        """Get detailed comparison of all available routes"""

        routes = await self._get_available_routes(payment_request)

        comparison = {
            "route_count": len(routes),
            "comparison_criteria": ["cost", "speed", "reliability", "features"],
            "routes": [],
        }

        for route in routes:
            route_comparison = {
                "route_id": route["route_id"],
                "name": route["name"],
                "provider": route["provider"],
                "cost_rating": self._rate_cost(
                    route["estimated_cost"], payment_request.amount
                ),
                "speed_rating": self._rate_speed(route["estimated_time_hours"]),
                "reliability_rating": self._rate_reliability(route["success_rate"]),
                "key_features": route.get("features", []),
                "limitations": route.get("limitations", []),
                "best_for": self._determine_best_use_case(route),
            }
            comparison["routes"].append(route_comparison)

        return comparison

    def _rate_cost(self, cost: float, amount: Decimal) -> str:
        """Rate cost effectiveness"""
        cost_percentage = (cost / float(amount)) * 100

        if cost_percentage < 0.5:
            return "excellent"
        elif cost_percentage < 1.0:
            return "good"
        elif cost_percentage < 2.0:
            return "fair"
        else:
            return "poor"

    def _rate_speed(self, hours: float) -> str:
        """Rate speed"""
        if hours < 1:
            return "instant"
        elif hours < 4:
            return "fast"
        elif hours < 24:
            return "standard"
        else:
            return "slow"

    def _rate_reliability(self, success_rate: float) -> str:
        """Rate reliability"""
        if success_rate > 0.99:
            return "excellent"
        elif success_rate > 0.97:
            return "good"
        elif success_rate > 0.95:
            return "fair"
        else:
            return "poor"

    def _determine_best_use_case(self, route: Dict[str, Any]) -> List[str]:
        """Determine best use cases for a route"""
        use_cases = []

        if route["estimated_cost"] < route.get(
            "average_cost", route["estimated_cost"] * 1.5
        ):
            use_cases.append("cost_sensitive")

        if route["estimated_time_hours"] < 4:
            use_cases.append("urgent_payments")

        if route["success_rate"] > 0.98:
            use_cases.append("high_value_transactions")

        if "tracking" in route.get("features", []):
            use_cases.append("business_payments")

        return use_cases
