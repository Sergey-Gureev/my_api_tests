from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class UserRole(Enum):
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
    value: str
    parse_mode: str = Field(..., alias='parseMode')


class Paging(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')


class Settings(BaseModel):
    color_schema: str = Field(..., alias='colorSchema')
    nanny_greetings_message: str = Field(..., alias='nannyGreetingsMessage')
    paging: Paging


class User(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias='status')
    rating: Rating
    online: datetime = Field(None, alias="online")
    name: str = Field(None, alias="name")
    location: str = Field(None, alias="location")
    registration: datetime = Field(None, alias="datetime")
    icq: str = Field(None, alias="icq")
    skype: str = Field(None, alias="skype")
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: Info = Field(None, alias="info")
    settings: Settings = Field(None, alias="settings")

class Metadata(BaseModel):
    email: str = Field(None)

class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[User] = None
    metadata: Optional[Metadata] = None