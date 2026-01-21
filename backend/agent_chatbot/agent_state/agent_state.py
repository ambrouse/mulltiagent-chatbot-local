from typing import TypedDict, List, Optional, Annotated
import operator

class ContractState(TypedDict):
    user_id: str
    session_id: str
    template_id: str
    user_input: str
    target_schema: dict
    data_history_input: dict
    data_input_null : List[str]
    mess : str
    status: str 