
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ResetUserPassword(BaseModel):
    login: Optional[str] = None
    email: Optional[str] = None


class ChangeUserPassword(BaseModel):
    login: Optional[str] = None
    token: Optional[str] = None
    oldPassword: Optional[str] = None
    newPassword: Optional[str] = None
