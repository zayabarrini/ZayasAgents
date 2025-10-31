from typing import Dict, Any
from ..core.constants import RiskLevel


class RegionalComplianceRules:
    def __init__(self):
        self.rules = self._load_compliance_rules()

    def _load_compliance_rules(self) -> Dict[str, Dict[str, Any]]:
        return {
            "US": {
                "max_amount": 10000,
                "kyc_required": True,
                "required_docs": ["id", "proof_of_address"],
                "risk_level": RiskLevel.MEDIUM,
                "additional_checks": ["ofac_screening", "source_of_funds"],
            },
            "RU": {
                "max_amount": 1000000,
                "kyc_required": True,
                "required_docs": ["passport", "tax_id"],
                "risk_level": RiskLevel.HIGH,
                "additional_checks": ["sanctions_check", "enhanced_kyc"],
            },
            "CH": {
                "max_amount": 10000,
                "kyc_required": True,
                "required_docs": ["id_card", "residence_proof"],
                "risk_level": RiskLevel.LOW,
                "additional_checks": ["bank_reference"],
            },
            "AR": {
                "max_amount": 1000,
                "kyc_required": True,
                "required_docs": ["dni", "cuit"],
                "risk_level": RiskLevel.MEDIUM,
                "additional_checks": ["central_bank_approval"],
            },
            "MX": {
                "max_amount": 2000,
                "kyc_required": True,
                "required_docs": ["ine", "rfc"],
                "risk_level": RiskLevel.MEDIUM,
                "additional_checks": ["sat_notification"],
            },
            "ES": {
                "max_amount": 5000,
                "kyc_required": True,
                "required_docs": ["dni", "nie"],
                "risk_level": RiskLevel.LOW,
                "additional_checks": ["sepblac_report"],
            },
            "JP": {
                "max_amount": 1000000,
                "kyc_required": True,
                "required_docs": ["my_number", "residence_card"],
                "risk_level": RiskLevel.LOW,
                "additional_checks": ["fsa_compliance"],
            },
            "KR": {
                "max_amount": 10000,
                "kyc_required": True,
                "required_docs": ["resident_id", "business_registration"],
                "risk_level": RiskLevel.MEDIUM,
                "additional_checks": ["fss_approval"],
            },
            "DE": {
                "max_amount": 12500,
                "kyc_required": True,
                "required_docs": ["personalausweis", "steuer_id"],
                "risk_level": RiskLevel.LOW,
                "additional_checks": ["bundesbank_report"],
            },
            "FR": {
                "max_amount": 3000,
                "kyc_required": True,
                "required_docs": ["carte_identite", "tax_notice"],
                "risk_level": RiskLevel.LOW,
                "additional_checks": ["tracfin_notification"],
            },
            "IT": {
                "max_amount": 5000,
                "kyc_required": True,
                "required_docs": ["carta_identita", "codice_fiscale"],
                "risk_level": RiskLevel.LOW,
                "additional_checks": ["uif_report"],
            },
            "IN": {
                "max_amount": 250000,
                "kyc_required": True,
                "required_docs": ["aadhaar", "pan_card"],
                "risk_level": RiskLevel.MEDIUM,
                "additional_checks": ["rbi_approval", "fema_compliance"],
            },
        }

    def get_country_rules(self, country_code: str) -> Dict[str, Any]:
        return self.rules.get(country_code, {})

    def get_required_documents(self, country_code: str, amount: float) -> list:
        rules = self.get_country_rules(country_code)
        if amount > rules.get("reporting_threshold", rules.get("max_amount", 0)):
            return rules.get("required_docs", [])
        return []
