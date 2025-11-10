from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    detail: str

class SuccessResponse(BaseModel):
    message: str
