from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional

# 1. 定义原子操作类型 (StepType)
class StepType(str, Enum):
    """定义数据工作流中的核心原子操作类型 (采用描述性命名)"""
    LOAD_DATA = "load_data"
    SELECT_COLUMNS = "select_columns"
    FILTER_ROWS = "filter_rows"
    GROUP_AGG = "group_aggregate"
    SAVE_DATA = "save_data"

# 2. 定义工作流中的一个步骤 (WorkflowStep)
class WorkflowStep(BaseModel):
    """表示数据工作流中的单个可执行步骤 (IR 节点)"""
    id: str = Field(description="该步骤的唯一标识符。")
    step_type: StepType
    # 采用 default_factory=dict 确保安全的可变默认值
    params: Dict[str, Any] = Field(default_factory=dict, description="该操作所需的具体参数字典。")
    input_df_id: str = Field(default="df", description="该步骤的输入 DataFrame ID。")

# 3. 定义完整的数据工作流 (DataWorkflow - 核心 IR)
class DataWorkflow(BaseModel):
    """数据工作流的中间表示 (IR)，包含流程验证逻辑"""
    description: str = Field(description="用户需求的自然语言描述。")
    steps: List[WorkflowStep] = Field(description="按执行顺序排列的 WorkflowStep 列表。")
    
    # 【DeepSeek 优势集成】：实现静态语义检查
    @validator('steps')
    def validate_flow_integrity(cls, steps):
        if not steps:
            raise ValueError("工作流不能为空 (Flow cannot be empty)")
        
        # 强制要求以 LOAD_DATA 开始
        if steps[0].step_type != StepType.LOAD_DATA:
            raise ValueError("工作流必须以 LOAD_DATA 开始 (Must start with LOAD_DATA)")
        
        # 强制要求以 SAVE_DATA 结束
        if steps[-1].step_type != StepType.SAVE_DATA:
            raise ValueError("工作流必须以 SAVE_DATA 结束 (Must end with SAVE_DATA)")
            
        return steps

# 4. 【您的优势集成】：定义错误反馈结构 (用于自动修复)
class ErrorFeedback(BaseModel):
    """Agent 用于学习和自我修复的反馈结构"""
    original_prompt: str = Field(description="最初的用户指令。")
    failed_code: str = Field(description="执行失败的 Python 代码。")
    error_message: str = Field(description="Python 解释器抛出的详细错误信息。")
    suggested_fix: str = Field(description="由 Agent 提出的修复建议或对 IR 的修改说明。")
