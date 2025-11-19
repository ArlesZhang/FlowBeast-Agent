
from typing import List, Dict, Any, Literal
from pydantic import BaseModel

StepType = Literal["LOAD_DATA", "FILTER_ROWS", "GROUP_AGGREGATE", "SAVE_DATA"]

class Step(BaseModel):
    name: str = "Unknown Step"
    step_type: StepType
    params: Dict[str, Any] = {}

class DataWorkflow(BaseModel):
    description: str
    steps: List[Step]
