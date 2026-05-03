from flowbeast.legacy_workflows.ir.models import DataWorkflow
import os

def generate_code(workflow: DataWorkflow) -> str:
    code = ["import pandas as pd", "import os\n", "def run_workflow():"]
    df = "df"

    for step in workflow.steps:
        step_type = step.step_type 

        if step_type == "load_data":
            path = step.params.get("path", "flowbeast/data/input.csv")
            code.append(f'    # 1. LOAD_DATA: {path}')
            code.append(f'    {df} = pd.read_csv("{path}")')

        elif step_type == "filter_rows":
            cond = step.params.get("condition", "True")
            code.append(f'    # 2. FILTER_ROWS: {cond}')
            code.append(f'    {df} = {df}.query("{cond}")')

        elif step_type == "group_aggregate":
            group_by = step.params.get("group_by", ["department"])
            if not isinstance(group_by, list):
                group_by = [group_by]
            
            agg_dict = step.params.get("aggregations", {})
            
            parts = []
            if isinstance(agg_dict, dict):
                for new_name, (old_col, func) in agg_dict.items():
                    parts.append(f'{new_name}=("{old_col}", "{func}")') 
            
            agg_str = ", ".join(parts)
            
            code.append(f'    # 3. GROUP_AGGREGATE by {group_by!r}')
            if agg_str:
                code.append(f'    {df} = {df}.groupby({group_by!r}).agg({agg_str}).reset_index()')

        elif step_type == "save_data":
            path = step.params.get("path", "flowbeast/data/top_sales.parquet") 
            code.append(f'    # 4. SAVE_DATA to {path}')
            code.append(f'    os.makedirs(os.path.dirname("{path}"), exist_ok=True)')
            code.append(f'    {df}.to_parquet("{path}", index=False)')

    code.append('    print("任务完成！")')
    code.append('    return df')
    code.append('if __name__ == "__main__":')
    code.append('    run_workflow()')
    return "\n".join(code)

# Keep compile_workflow for backward compatibility
def compile_workflow(user_prompt: str, model: str = "qwen-turbo") -> DataWorkflow:
    """Legacy compile_workflow - kept for backward compatibility only."""
    # This is a placeholder - original logic moved to agent/compiler.py
    raise NotImplementedError(
        "compile_workflow has moved to flowbeast.agent.compiler.compile_workflow. "
        "This legacy version is deprecated."
    )
