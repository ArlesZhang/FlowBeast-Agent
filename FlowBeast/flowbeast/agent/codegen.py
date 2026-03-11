from flowbeast.ir.models import DataWorkflow
import os

def generate_code(workflow: DataWorkflow) -> str:
    code = ["import pandas as pd", "import os\n", "def run_workflow():"]
    df = "df"

    for step in workflow.steps:
        # 修复：直接比较 step_type (它是一个继承了 str 的 Enum/Literal)
        step_type = step.step_type 

        # LOAD_DATA
        if step_type == "load_data":
            path = step.params.get("path", "flowbeast/data/input.csv")
            code.append(f'    # 1. LOAD_DATA: {path}')
            code.append(f'    {df} = pd.read_csv("{path}")')

        # FILTER_ROWS
        elif step_type == "filter_rows":
            cond = step.params.get("condition", "True")
            code.append(f'    # 2. FILTER_ROWS: {cond}')
            code.append(f'    {df} = {df}.query("{cond}")')

        # GROUP_AGGREGATE (最终修复的关键)
        elif step_type == "group_aggregate":
            group_by = step.params.get("group_by", ["department"])
            if not isinstance(group_by, list):
                group_by = [group_by]
            
            # compiler.py 已经将 aggregations 修复为 {'new_name': ('old_col', 'func')}
            agg_dict = step.params.get("aggregations", {})
            
            parts = []
            # 确保 agg_dict 是一个字典 (compiler.py 应该已经保证了)
            if isinstance(agg_dict, dict):
                for new_name, (old_col, func) in agg_dict.items():
                    # 核心修复：生成正确的 Pandas agg 参数: new_name=('old_col', 'func')
                    parts.append(f'{new_name}=("{old_col}", "{func}")') 
            
            agg_str = ", ".join(parts)
            
            code.append(f'    # 3. GROUP_AGGREGATE by {group_by!r}')
            if agg_str:
                code.append(f'    {df} = {df}.groupby({group_by!r}).agg({agg_str}).reset_index()')
            else:
                code.append(f'    # 警告：未找到聚合函数，跳过聚合步骤。')


        # SAVE_DATA
        elif step_type == "save_data":
            path = step.params.get("path", "flowbeast/data/top_sales.parquet") 
            code.append(f'    # 4. SAVE_DATA to {path}')
            # 添加 os.makedirs 确保执行环境能创建目录
            code.append(f'    os.makedirs(os.path.dirname("{path}"), exist_ok=True)')
            code.append(f'    {df}.to_parquet("{path}", index=False)')
            code.append(f'    print("保存成功 → {path}")')

    code.append('    print("任务完成！")')
    code.append('    return df')
    code.append('if __name__ == "__main__":')
    code.append('    run_workflow()')
    return "\n".join(code)
