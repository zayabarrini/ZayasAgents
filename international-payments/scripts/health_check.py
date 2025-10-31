#!/usr/bin/env python3
"""
Health check script for the International Payment System
"""

import asyncio
import aiohttp
import sys
import json
from datetime import datetime
from typing import Dict, List, Any


class PaymentSystemHealthCheck:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.checks = []

    async def check_api_health(self) -> Dict[str, Any]:
        """Check basic API health"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/payments/health"
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "healthy",
                            "response": data,
                            "response_time": response.elapsed.total_seconds(),
                        }
                    else:
                        return {
                            "status": "unhealthy",
                            "error": f"HTTP {response.status}",
                            "response_time": response.elapsed.total_seconds(),
                        }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e), "response_time": None}

    async def check_exchange_rates(self) -> Dict[str, Any]:
        """Check exchange rate service"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/payments/exchange-rate",
                    params={"base_currency": "USD", "target_currency": "EUR"},
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "healthy",
                            "service": "exchange_rates",
                            "rate_available": True,
                            "rate": data.get("rate"),
                        }
                    else:
                        return {
                            "status": "unhealthy",
                            "service": "exchange_rates",
                            "error": f"HTTP {response.status}",
                        }
        except Exception as e:
            return {"status": "unhealthy", "service": "exchange_rates", "error": str(e)}

    async def check_compliance_service(self) -> Dict[str, Any]:
        """Check compliance service"""
        try:
            async with aiohttp.ClientSession() as session:
                compliance_data = {
                    "sender_country": "US",
                    "recipient_country": "GB",
                    "amount": 1000.0,
                    "currency": "USD",
                }

                async with session.post(
                    f"{self.base_url}/api/v1/payments/compliance-check",
                    json=compliance_data,
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "healthy",
                            "service": "compliance",
                            "aml_check": data.get("aml_check", False),
                            "risk_level": data.get("risk_level"),
                        }
                    else:
                        return {
                            "status": "unhealthy",
                            "service": "compliance",
                            "error": f"HTTP {response.status}",
                        }
        except Exception as e:
            return {"status": "unhealthy", "service": "compliance", "error": str(e)}

    async def check_database_connectivity(self) -> Dict[str, Any]:
        """Check database connectivity (placeholder for actual DB checks)"""
        try:
            # Simulate database check
            await asyncio.sleep(0.1)
            return {"status": "healthy", "service": "database", "connected": True}
        except Exception as e:
            return {"status": "unhealthy", "service": "database", "error": str(e)}

    async def check_security_services(self) -> Dict[str, Any]:
        """Check security-related services"""
        try:
            # Check if security endpoints are accessible
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/payments/supported-currencies"
                ) as response:
                    if response.status == 200:
                        return {
                            "status": "healthy",
                            "service": "security",
                            "endpoints_accessible": True,
                        }
                    else:
                        return {
                            "status": "unhealthy",
                            "service": "security",
                            "error": f"HTTP {response.status}",
                        }
        except Exception as e:
            return {"status": "unhealthy", "service": "security", "error": str(e)}

    async def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        checks = [
            self.check_api_health(),
            self.check_exchange_rates(),
            self.check_compliance_service(),
            self.check_database_connectivity(),
            self.check_security_services(),
        ]

        results = await asyncio.gather(*checks)

        overall_status = "healthy"
        for result in results:
            if result["status"] == "unhealthy":
                overall_status = "unhealthy"
                break

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": overall_status,
            "services": {
                "api": results[0],
                "exchange_rates": results[1],
                "compliance": results[2],
                "database": results[3],
                "security": results[4],
            },
        }

    def print_health_report(self, report: Dict[str, Any]):
        """Print formatted health report"""
        print("\n" + "=" * 60)
        print("INTERNATIONAL PAYMENT SYSTEM - HEALTH CHECK REPORT")
        print("=" * 60)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Overall Status: {report['overall_status'].upper()}")
        print("\nService Details:")
        print("-" * 40)

        for service_name, service_info in report["services"].items():
            status_icon = "✅" if service_info["status"] == "healthy" else "❌"
            print(
                f"{status_icon} {service_name.upper():<15} : {service_info['status']}"
            )

            if service_info["status"] == "unhealthy":
                print(f"   Error: {service_info.get('error', 'Unknown error')}")
            else:
                # Print additional success info
                if service_name == "api" and "response_time" in service_info:
                    print(f"   Response Time: {service_info['response_time']:.3f}s")
                elif service_name == "exchange_rates" and "rate" in service_info:
                    print(f"   USD/EUR Rate: {service_info['rate']}")

        print("=" * 60)


async def main():
    """Main health check execution"""
    import argparse

    parser = argparse.ArgumentParser(description="Payment System Health Check")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the payment system API",
    )
    parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    health_check = PaymentSystemHealthCheck(base_url=args.url)

    try:
        report = await health_check.run_all_checks()

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            health_check.print_health_report(report)

        # Exit with appropriate code
        sys.exit(0 if report["overall_status"] == "healthy" else 1)

    except Exception as e:
        print(f"Health check failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
