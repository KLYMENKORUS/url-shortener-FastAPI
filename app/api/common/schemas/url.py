from pydantic import BaseModel, Field, ConfigDict


class URLBase(BaseModel):
    target_url: str = Field(
        ...,
        examples=["http://example.com"],
    )


class URLCreate(URLBase):
    key: str


class URL(URLBase):
    model_config = ConfigDict(from_attributes=True)

    is_active: bool = Field(
        ...,
        examples=["True"],
    )
    clicks: int = Field(
        ...,
        examples=["0"],
    )


class URLInfo(URL):
    short_url: str


class URLUpdate(URLBase):
    short_url: str
