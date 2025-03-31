from pydantic import BaseModel, root_validator, ValidationError
from typing import Dict


class From(BaseModel):
    email: str

    @root_validator(pre=True)
    def check_default_key(cls, values):
        if 'DEFAULT' not in values:
            raise ValueError("The 'DEFAULT' key must be defined.")
        return values


class Sender(BaseModel):
    from_address: From
    nickname: str
    reply_to: str
    address: str
    city: str
    state: str
    zip: str


class UnSubscribeGroup(BaseModel):
    group_id: int


class EmailTemplate(BaseModel):
    id: str


class Config(BaseModel):
    api_key: str
    senders: Dict[str, Sender]
    unsubscribe_groups: Dict[str, UnSubscribeGroup]
    email_templates: Dict[str, EmailTemplate]

