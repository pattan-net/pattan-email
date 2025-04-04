from pydantic import BaseModel, model_validator
from typing import Dict, List


class From(BaseModel):
    email: str
    name: str


class Sender(BaseModel):
    from_address: From
    nickname: str
    reply_to: From
    address: str
    address_2: str
    city: str
    state: str
    zip: str


class UnSubscribeGroup(BaseModel):
    id: int


class EmailTemplate(BaseModel):
    id: str
    name: str
    variables: List[str]

class IpPool(BaseModel):
    name: str

class Config(BaseModel):
    api_key: str
    senders: Dict[str, Sender]
    unsubscribe_groups: Dict[str, UnSubscribeGroup]
    email_templates: Dict[str, EmailTemplate]
    ip_pools: Dict[str, IpPool]

    @model_validator(mode='before')
    def check_default_key(cls, values):
        if 'DEFAULT' not in values['email_templates']:
            raise ValueError("The 'DEFAULT' key missing from the 'email_templates' list.")
        if 'DEFAULT' not in values['senders']:
            raise ValueError("The 'DEFAULT' key missing from the 'senders' list.")
        if 'DEFAULT' not in values['unsubscribe_groups']:
            raise ValueError("The 'DEFAULT' key missing from the 'unsubscribe_groups' list.")
        return values