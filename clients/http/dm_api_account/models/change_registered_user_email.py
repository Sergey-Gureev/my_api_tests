from pydantic import BaseModel, Field, ConfigDict

class ChangeUserEmail(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description="Login")
    password: str = Field(..., description="password")
    email: str = Field(..., description="email")