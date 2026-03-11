from jinja2 import Template
from ..ir.models import DataWorkflow, StepType

class PandasCodeGenerator:
    def __init__(self):
        # 使用Jinja2模板，更灵活
        self.templates = {
            StepType.LOAD_DATA: Template("df = pd.read_{{ params.format }}('{{ params.path }}')"),
            StepType.FILTER_ROWS: Template("df = df[df['{{ params.column }}'] {{ params.condition }}]"),
            StepType.SELECT_COLUMNS: Template("df = df[{{ params.columns | to_json }}]"),
            StepType.GROUP_AGG: Template("df = df.groupby('{{ params.group_by }}').agg({{ params.aggregations }})"),
            StepType.SAVE_DATA: Template("df.to_{{ params.format }}('{{ params.path }}')"),
        }
    
    def generate_script(self, workflow: DataWorkflow) -> str:
        """生成完整的可执行脚本"""
        code_lines = [
            "import pandas as pd\n",
            "def execute_pipeline():\n",
            "    # 数据工作流管道\n"
        ]
        
        for i, step in enumerate(workflow.steps):
            template = self.templates.get(step.step_type)
            if template:
                step_code = template.render(params=step.params)
                code_lines.append(f"    # 步骤 {i+1}: {step.step_type}\n")
                code_lines.append(f"    {step_code}\n")
        
        code_lines.extend([
            "    return df\n",
            "\nif __name__ == \"__main__\":\n",
            "    result_df = execute_pipeline()\n",
            "    print(\"Pipeline executed successfully!\")\n",
            "    print(f\"Result shape: {result_df.shape}\")"
        ])
        
        return "".join(code_lines)
