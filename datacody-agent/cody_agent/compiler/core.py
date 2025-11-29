USAGE_COST = 0.01
from cody_agent.commercial.billing import BillingManager
from cody_agent.agent.compiler import compile_workflow
from typing import Dict

class CommercialCompiler:
    def __init__(self):
        self.billing = BillingManager()

    async def compile_with_billing(self, task: str, user_id: str, tier: str = "developer", project_id: str = None) -> Dict:
        # 记录用量（商业版核心）
        await self.billing.record_usage(user_id, USAGE_COST, task)
        # 直接调用你原有的编译逻辑
        return compile_workflow(task).model_dump()
