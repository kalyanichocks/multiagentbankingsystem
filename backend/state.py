from typing import TypedDict, Optional

class AgentState(TypedDict):
    user_query:str|None
    customer_id : int|None
    intent: str
    account_number: int|None
    agent_status: str|None
    sender_account: int|None
    receiver_account: int|None
    ownership_verified: bool|None
    sender_account_status: str|None
    receiver_account_status: str|None
    document_enter:bool|None
    amount: int|None
    balance: float|None
    status: str|None
    user_otp:str|None
    generated_otp:str|None
    otp_status:bool|None
    message: str|None
