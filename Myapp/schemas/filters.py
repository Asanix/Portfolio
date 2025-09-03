from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")

class PaginationFilter(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=5, le=100)
    
    
class PagingationResponse(GenericModel, Generic[T]):
    data: list[T]
    total: int
    page: int
    limit: int
    pages: int
    