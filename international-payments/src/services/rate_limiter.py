from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from ..core.exceptions import RateLimitExceededError


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.max_requests_per_minute = 10
        self.max_requests_per_hour = 100

    def check_limit(self, identifier: str, operation: str = "payment") -> bool:
        current_time = datetime.utcnow()
        key = f"{identifier}_{operation}"
        user_requests = self.requests[key]

        # Clean old requests
        recent_requests = [
            req_time
            for req_time in user_requests
            if current_time - req_time < timedelta(hours=1)
        ]

        # Check minute limit
        minute_requests = [
            req for req in recent_requests if current_time - req < timedelta(minutes=1)
        ]

        if len(minute_requests) >= self.max_requests_per_minute:
            raise RateLimitExceededError("Minute rate limit exceeded")

        if len(recent_requests) >= self.max_requests_per_hour:
            raise RateLimitExceededError("Hourly rate limit exceeded")

        # Add current request
        recent_requests.append(current_time)
        self.requests[key] = recent_requests

        return True

    def get_usage_stats(self, identifier: str) -> Dict[str, int]:
        current_time = datetime.utcnow()
        user_requests = self.requests.get(identifier, [])

        minute_requests = [
            req for req in user_requests if current_time - req < timedelta(minutes=1)
        ]

        hourly_requests = [
            req for req in user_requests if current_time - req < timedelta(hours=1)
        ]

        return {
            "minute_usage": len(minute_requests),
            "hourly_usage": len(hourly_requests),
            "minute_limit": self.max_requests_per_minute,
            "hourly_limit": self.max_requests_per_hour,
        }
