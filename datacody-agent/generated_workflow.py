import pandas as pd
import os

def run_workflow():
    # 1. LOAD_DATA: cody_agent/data/input.csv
    df = pd.read_csv("cody_agent/data/input.csv")
    # 2. FILTER_ROWS: amount > 1000
    df = df.query("amount > 1000")
    # 3. GROUP_AGGREGATE by ['department']
    df = df.groupby(['department']).agg(avg_age=("age", "mean"), total_sales=("amount", "sum")).reset_index()
    # 4. SAVE_DATA to cody_agent/data/top_sales.parquet
    os.makedirs(os.path.dirname("cody_agent/data/top_sales.parquet"), exist_ok=True)
    df.to_parquet("cody_agent/data/top_sales.parquet", index=False)
    print("保存成功 → cody_agent/data/top_sales.parquet")
    print("任务完成！")
    return df
if __name__ == "__main__":
    run_workflow()