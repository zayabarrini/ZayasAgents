"""
Compliance service for international payments with regional regulations
"""

import asyncio
from typing import Dict, List, Any, Optional
from decimal import Decimal
from datetime import datetime
import logging

from ..core.models import ComplianceResult
from ..core.constants import RiskLevel
from ..regional.compliance_rules import RegionalComplianceRules


class ComplianceService:
    def __init__(self):
        self.compliance_rules = RegionalComplianceRules()
        self.logger = logging.getLogger("ComplianceService")
        self.sanction_lists = self._load_sanction_lists()

    def _load_sanction_lists(self) -> Dict[str, List[str]]:
        """Load sanction lists (simplified - in production, use official sources)"""
        return {
            "OFAC": ["CU", "IR", "KP", "SY", "RU"],  # Example restricted countries
            "EU_SANCTIONS": ["BY", "RU", "SY"],
            "UN_SANCTIONS": ["KP"],
        }

    async def perform_compliance_check(
        self,
        sender_data: Dict[str, Any],
        recipient_data: Dict[str, Any],
        amount: Decimal,
        currency: str,
    ) -> ComplianceResult:
        """Perform comprehensive compliance check"""

        sender_country = sender_data.get("country", "")
        recipient_country = recipient_data.get("country", "")
        amount_float = float(amount)

        # 1. Sanction screening
        sanction_check = await self._check_sanctions(sender_data, recipient_data)

        # 2. AML (Anti-Money Laundering) check
        aml_check = await self._perform_aml_check(
            sender_data, recipient_data, amount_float
        )

        # 3. Regional compliance
        regional_check = self._check_regional_compliance(
            sender_country, recipient_country, amount_float
        )

        # 4. KYC verification status
        kyc_verified = self._check_kyc_status(sender_data)

        # 5. Risk assessment
        risk_level = await self._assess_risk_level(
            sender_country, recipient_country, amount_float, sanction_check, aml_check
        )

        # 6. Determine required documents
        required_documents = self._get_required_documents(
            sender_country, recipient_country, amount_float
        )

        # Overall compliance result
        overall_compliant = (
            sanction_check["approved"]
            and aml_check["approved"]
            and regional_check["approved"]
        )

        return ComplianceResult(
            aml_check=overall_compliant,
            kyc_verified=kyc_verified,
            sanction_screening=sanction_check["approved"],
            risk_level=risk_level,
            required_documents=required_documents,
        )

    async def _check_sanctions(
        self, sender_data: Dict[str, Any], recipient_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check against sanction lists"""

        sender_country = sender_data.get("country", "")
        recipient_country = recipient_data.get("country", "")

        # Check sender country
        sender_restricted = any(
            sender_country in sanctions for sanctions in self.sanction_lists.values()
        )

        # Check recipient country
        recipient_restricted = any(
            recipient_country in sanctions for sanctions in self.sanction_lists.values()
        )

        # Check names against sanction lists (simplified)
        sender_name_restricted = await self._check_name_against_sanctions(
            sender_data.get("name", "")
        )
        recipient_name_restricted = await self._check_name_against_sanctions(
            recipient_data.get("name", "")
        )

        approved = not any(
            [
                sender_restricted,
                recipient_restricted,
                sender_name_restricted,
                recipient_name_restricted,
            ]
        )

        reasons = []
        if sender_restricted:
            reasons.append(f"Sender country {sender_country} is sanctioned")
        if recipient_restricted:
            reasons.append(f"Recipient country {recipient_country} is sanctioned")
        if sender_name_restricted:
            reasons.append("Sender name matches sanctioned entity")
        if recipient_name_restricted:
            reasons.append("Recipient name matches sanctioned entity")

        return {
            "approved": approved,
            "reasons": reasons,
            "check_timestamp": datetime.utcnow().isoformat(),
        }

    async def _check_name_against_sanctions(self, name: str) -> bool:
        """Check name against sanction lists (simplified)"""
        # In production, integrate with actual sanction list APIs
        sanctioned_names = ["EXAMPLE_SANCTIONED_NAME"]  # Placeholder

        # Simple substring matching (in production, use fuzzy matching)
        return any(
            sanctioned_name in name.upper() for sanctioned_name in sanctioned_names
        )

    async def _perform_aml_check(
        self, sender_data: Dict[str, Any], recipient_data: Dict[str, Any], amount: float
    ) -> Dict[str, Any]:
        """Perform Anti-Money Laundering checks"""

        risk_factors = []
        approved = True

        # Amount-based checks
        if amount > 10000:
            risk_factors.append("HIGH_AMOUNT")
            # Large amounts require enhanced due diligence

        # Geographic risk
        high_risk_countries = ["RU", "AR", "MX", "NG", "VE"]
        if recipient_data.get("country") in high_risk_countries:
            risk_factors.append("HIGH_RISK_JURISDICTION")
            approved = False  # Auto-reject for demo purposes

        # PEP (Politically Exposed Person) check
        is_sender_pep = await self._check_pep_status(sender_data)
        is_recipient_pep = await self._check_pep_status(recipient_data)

        if is_sender_pep or is_recipient_pep:
            risk_factors.append("POLITICALLY_EXPOSED_PERSON")
            # PEP transactions require enhanced monitoring

        return {
            "approved": approved,
            "risk_factors": risk_factors,
            "pep_check": {"sender": is_sender_pep, "recipient": is_recipient_pep},
        }

    async def _check_pep_status(self, entity_data: Dict[str, Any]) -> bool:
        """Check if entity is a Politically Exposed Person (simplified)"""
        # In production, integrate with PEP databases
        pep_names = ["EXAMPLE_PEP_NAME"]  # Placeholder

        name = entity_data.get("name", "").upper()
        return any(pep_name in name for pep_name in pep_names)

    def _check_regional_compliance(
        self, sender_country: str, recipient_country: str, amount: float
    ) -> Dict[str, Any]:
        """Check regional compliance requirements"""

        approved = True
        reasons = []

        # Check sender country rules
        sender_rules = self.compliance_rules.get_country_rules(sender_country)
        if sender_rules:
            max_amount = sender_rules.get("max_amount", 0)
            if amount > max_amount:
                approved = False
                reasons.append(f"Amount exceeds {sender_country} limit of {max_amount}")

        # Check recipient country rules
        recipient_rules = self.compliance_rules.get_country_rules(recipient_country)
        if recipient_rules:
            max_amount = recipient_rules.get("max_amount", 0)
            if amount > max_amount:
                approved = False
                reasons.append(
                    f"Amount exceeds {recipient_country} limit of {max_amount}"
                )

        # Check for restricted country pairs
        restricted_pairs = [("US", "CU"), ("US", "IR"), ("US", "SY"), ("US", "KP")]
        if (sender_country, recipient_country) in restricted_pairs:
            approved = False
            reasons.append(
                f"Restricted country pair: {sender_country} -> {recipient_country}"
            )

        return {"approved": approved, "reasons": reasons}

    def _check_kyc_status(self, sender_data: Dict[str, Any]) -> bool:
        """Check KYC verification status"""
        # In production, this would check actual KYC verification status
        kyc_status = sender_data.get("kyc_status", "verified")
        return kyc_status in ["verified", "approved"]

    async def _assess_risk_level(
        self,
        sender_country: str,
        recipient_country: str,
        amount: float,
        sanction_check: Dict[str, Any],
        aml_check: Dict[str, Any],
    ) -> RiskLevel:
        """Assess overall risk level"""

        risk_score = 0

        # Base risk from countries
        sender_rules = self.compliance_rules.get_country_rules(sender_country)
        recipient_rules = self.compliance_rules.get_country_rules(recipient_country)

        if sender_rules:
            risk_score += {"LOW": 0, "MEDIUM": 20, "HIGH": 40}.get(
                sender_rules.get("risk_level", "LOW").upper(), 0
            )

        if recipient_rules:
            risk_score += {"LOW": 0, "MEDIUM": 20, "HIGH": 40}.get(
                recipient_rules.get("risk_level", "LOW").upper(), 0
            )

        # Sanction check risk
        if not sanction_check["approved"]:
            risk_score += 60

        # AML check risk
        risk_score += len(aml_check.get("risk_factors", [])) * 15

        # Amount-based risk
        if amount > 50000:
            risk_score += 30
        elif amount > 10000:
            risk_score += 15

        # Determine risk level
        if risk_score >= 70:
            return RiskLevel.HIGH
        elif risk_score >= 40:
            return RiskLevel.MEDIUM
        elif risk_score >= 20:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL

    def _get_required_documents(
        self, sender_country: str, recipient_country: str, amount: float
    ) -> List[str]:
        """Determine required documents based on countries and amount"""

        required_docs = []

        # Check sender country requirements
        sender_rules = self.compliance_rules.get_country_rules(sender_country)
        if sender_rules:
            sender_docs = self.compliance_rules.get_required_documents(
                sender_country, amount
            )
            required_docs.extend(sender_docs)

        # Check recipient country requirements
        recipient_rules = self.compliance_rules.get_country_rules(recipient_country)
        if recipient_rules:
            recipient_docs = self.compliance_rules.get_required_documents(
                recipient_country, amount
            )
            required_docs.extend(recipient_docs)

        # Additional documents for high amounts
        if amount > 10000:
            required_docs.extend(["source_of_funds", "purpose_of_payment"])

        return list(set(required_docs))  # Remove duplicates

    async def generate_compliance_report(
        self, transaction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""

        compliance_result = await self.perform_compliance_check(
            transaction_data["sender"],
            transaction_data["recipient"],
            Decimal(str(transaction_data["amount"])),
            transaction_data["currency"],
        )

        return {
            "transaction_id": transaction_data.get("transaction_id"),
            "compliance_result": {
                "aml_approved": compliance_result.aml_check,
                "kyc_verified": compliance_result.kyc_verified,
                "sanction_screening_passed": compliance_result.sanction_screening,
                "risk_level": compliance_result.risk_level.value,
                "required_documents": compliance_result.required_documents,
            },
            "recommendations": self._generate_compliance_recommendations(
                compliance_result
            ),
            "next_steps": self._determine_next_steps(compliance_result),
            "report_timestamp": datetime.utcnow().isoformat(),
        }

    def _generate_compliance_recommendations(
        self, result: ComplianceResult
    ) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []

        if not result.aml_check:
            recommendations.append(
                "Transaction requires manual review by compliance team"
            )

        if not result.kyc_verified:
            recommendations.append("Complete KYC verification for sender")

        if result.risk_level == RiskLevel.HIGH:
            recommendations.append("Enhanced due diligence required")
            recommendations.append("Consider declining transaction")

        if result.required_documents:
            recommendations.append(
                f"Collect required documents: {', '.join(result.required_documents)}"
            )

        if not recommendations:
            recommendations.append("Proceed with standard monitoring")

        return recommendations

    def _determine_next_steps(self, result: ComplianceResult) -> List[str]:
        """Determine next steps based on compliance result"""

        if not result.sanction_screening:
            return ["DECLINE_TRANSACTION", "REPORT_TO_REGULATOR"]

        if not result.aml_check:
            return ["MANUAL_REVIEW", "REQUEST_ADDITIONAL_DOCUMENTATION"]

        if result.risk_level == RiskLevel.HIGH:
            return ["ENHANCED_MONITORING", "LIMIT_TRANSACTION_AMOUNT"]

        if result.required_documents:
            return ["REQUEST_DOCUMENTS", "PROCEED_AFTER_VERIFICATION"]

        return ["AUTO_APPROVE", "STANDARD_MONITORING"]
