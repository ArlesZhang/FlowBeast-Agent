from cody_agent.ir.models import DataWorkflow, StepType
import json

def generate_code(workflow: DataWorkflow) -> str:
    code = ["import pandas as pd\n", "def run_workflow():"]
    df = "df"

    for step in workflow.steps:
        # LOAD_DATA
        if step.step_type == "LOAD_DATA":
            path = (step.params.get("path") or 
                   step.params.get("file_path") or 
                   step.params.get("source") or 
                   "cody_agent/data/input.csv")
            code.append(f'    {df} = pd.read_csv("{path}")')

        # FILTER_ROWS
        elif step.step_type == "FILTER_ROWS":
            cond = step.params.get("condition", "amount > 0")
            code.append(f'    {df} = {df}.query("{cond}")')

        # GROUP_AGGREGATE
        elif step.step_type == "GROUP_AGGREGATE":
            # group_by
            group_by = (step.params.get("group_by") or 
                       step.params.get("columns") or 
                       step.params.get("by") or 
                       ["department"])
            if not isinstance(group_by, list):
                group_by = [group_by]

            # aggregations
            agg_dict = {}
            raw = step.params.get("aggregations", {})
            rename = step.params.get("rename", {})

            if isinstance(raw, dict):
                for col, func in raw.items():
                    new = rename.get(col, col)
                    agg_dict[new] = (col, func)
            elif isinstance(raw, list):
                for item in raw:
                    col = item.get("column") or item.get("col")
                    func = item.get("function") or item.get("func") or "sum"
                    new = (item.get("rename") or 
                           item.get("new_name") or 
                           item.get("new_col") or 
                           col)
                    if col:
                        agg_dict[new] = (col, func)

            if agg_dict:
                parts = [f'{new}=("{old}", "{func}")' for new, (old, func) in agg_dict.items()]
                agg_str = ", ".join(parts)
                code.append(f'    {df} = {df}.groupby({group_by}).agg({agg_str}).reset_index()')

        # SAVE_DATA
        elif step.step_type == "SAVE_DATA":
            path = (step.params.get("path") or 
                   step.params.get("file_path") or 
                   step.params.get("target") or 
                   "cody_agent/data/output.parquet")
            code.append(f'    {df}.to_parquet("{path}", index=False)')
            code.append(f'    print("保存成功 → {path}")')

    code.append('    print("Workflow 完成！")')
    code.append('if __name__ == "__main__":')
    code.append('    run_workflow()')
    return "\n".join(code)
