
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"

class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class Info(BaseModel):
    value: str = Field(None, alias='value')
    parse_mode: str = Field(None, alias='parseMode')


class Paging(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')


class Settings(BaseModel):
    color_schema: str = Field(..., alias='colorSchema')
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: Paging


class Resource(BaseModel):
    login: str
    roles: list[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias="status")
    rating: Rating
    online: datetime = Field(None, alias="online")
    name: str = Field(None, alias="name")
    location: str = Field(None, alias="location")
    registration: str
    icq: str = Field(None, alias="icq")
    skype: str = Field(None, alias="skype")
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: str = Field(None, alias="info")
    settings: Settings


class UserDetailsEnvelope(BaseModel):
    resource: Optional[Resource] = None
    metadata: Optional[str] = None
