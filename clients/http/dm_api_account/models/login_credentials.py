from pydantic import BaseModel, Field, ConfigDict

class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description="Login")
    password: str = Field(..., description="password")
    remember_me: bool = Field(..., description="Remember Me", serialization_alias="rememberMe")