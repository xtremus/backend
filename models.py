from pydantic import BaseModel
from datetime import datetime
from typing import List


class User(BaseModel):
    user_id: int
    name: str
    email: str
    role: str
    created_at: datetime


class Users(BaseModel):
    users: List[User]


# Model for insering wfh requests
class WFH_Request(BaseModel):
    user_id: int
    from_datetime: str
    to_datetime: str
    approver_id: int


class Edit_WFH_Request(BaseModel):
    request_id: int
    from_datetime: str
    to_datetime: str
    approver_id: int


class WFH_Request_User(BaseModel):
    request_id: int
    from_datetime: str
    to_datetime: str
    status: str
    created_at: datetime
    approver_id: int
    approver_name: str
    approver_email: str


class WFH_Requests_User(BaseModel):
    requests: List[WFH_Request_User]


class WFH_Request_Admin(BaseModel):
    request_id: int
    name: str
    email: str
    from_datetime: datetime
    to_datetime: datetime
    status: str
    created_at: datetime


class WFH_Requests_Admin(BaseModel):
    requests: List[WFH_Request_Admin]
