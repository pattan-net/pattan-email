from pydantic import BaseModel
from typing import Dict


class From(BaseModel):
    email: str


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


class Config(BaseModel):
    api_key: str
    senders: Dict[str, Sender]
    unsubscribe_groups: Dict[str, UnSubscribeGroup]
