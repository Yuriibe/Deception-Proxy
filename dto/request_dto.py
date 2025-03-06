from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict
import json

class RequestDTO(BaseModel):
    method: str
    url: HttpUrl  # Pydantic will validate that this is a valid URL
    user_agent: Optional[str] = None
    sec_ch_ua: Optional[str] = None
    sec_ch_ua_platform: Optional[str] = None
    client_ip: str
    cookies: Optional[Dict[str, str]] = None  # Optional, in case there are no cookies
    attack_type: str
    attacker_id: int

    def dict(self, **kwargs):
        """Override dict() to ensure URL is a string and cookies are stored as JSON"""
        data = super().dict(**kwargs)
        data["url"] = str(data["url"])  # Convert HttpUrl to string
        data["cookies"] = json.dumps(data["cookies"]) if self.cookies else None  # Convert cookies dict to JSON
        return data
