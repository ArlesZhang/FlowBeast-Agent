import time
from typing import Dict
from cody_agent.agent.compiler import CompilerAgent  # 你原有 CompilerAgent
from cody_agent.commercial.billing import BillingManager
billing_manager = BillingManager()

class CommercialCompiler:
    def __init__(self):
        self.legacy_agent = CompilerAgent()  # 包装你原有逻辑

    async def compile_with_billing(self, task: str, user_id: str, tier: str = "developer", project_id: str = None) -> Dict:
        start = time.time()
        
        # 检查配额
        quota = await billing_manager.check_and_get_remaining(user_id)
        if not quota["allowed"]:
            return {"success": False, "error": f"配额已用尽，剩余 {quota['remaining']:.1f} 单位，请升级套餐"}
        
        # 执行原有编译逻辑
        legacy_result = await self.legacy_agent.arun(task, project_id=project_id)
        
        if legacy_result["status"] != "success":
            return {"success": False, "error": legacy_result.get("explanation", "编译失败")}
        
        # 计算成本
        cost = self._calculate_cost(legacy_result)
        
        # 记录使用
        await billing_manager.record_usage(user_id, cost, task)
        
        response = legacy_result.copy()
        response["cost_units"] = cost
        response["execution_time_sec"] = round(time.time() - start, 2)
        return response

    def _calculate_cost(self, result: Dict) -> float:
        base = 0.1 * result["execution_time_sec"]
        fix_penalty = 0.5 * result["fix_attempts"]
        opt_bonus = -0.2 if result["optimized"] else 0
        return max(base + fix_penalty + opt_bonus, 0.1)
