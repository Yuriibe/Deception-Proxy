from pydantic import BaseModel, HttpUrl
from typing import Optional

class RequestDTO(BaseModel):
    method: str
    url: HttpUrl  # ✅ URL is validated by Pydantic

    def dict(self, **kwargs):
        """Override dict() to convert HttpUrl to string"""
        data = super().dict(**kwargs)
        data["url"] = str(data["url"])  # Convert HttpUrl to string before inserting
        return data

    method: str
    url: HttpUrl
    user_agent: Optional[str] = None
    sec_ch_ua: Optional[str] = None
    sec_ch_ua_platform: Optional[str] = None
    client_ip: str
    cookies: Optional[str] = None
    attack_type: str
    attacker_id: int
