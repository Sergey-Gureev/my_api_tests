from pydantic import BaseModel, Field, ConfigDict

class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description="Login")
    password: str = Field(..., description="password")
    remember_me: str = Field(..., description="Remember Me", alias="rememberMe")