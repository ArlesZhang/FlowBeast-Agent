import pandas as pd, json, os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

prompt = "请以JSON格式输出：加载 cody_agent/data/input.csv，过滤 amount>1000，按 department 聚合 age 平均值命名为 avg_age，amount 总和命名为 total_sales，保存为 cody_agent/data/top_sales.parquet"

resp = client.chat.completions.create(model="qwen-turbo", temperature=0, messages=[{"role":"user","content":prompt}], response_format={"type":"json_object"})
steps = json.loads(resp.choices[0].message.content)["steps"]

code = "import pandas as pd\ndf=pd.read_csv('cody_agent/data/input.csv')\n"
for s in steps:
    n = s.get("name","").lower()
    p = s.get("params",{})
    if "filter" in n: code += f'df=df.query("{p.get("condition","amount>1000")}")\n'
    if "group" in n or "agg" in n:
        rename = p.get("rename", p.get("renames", {}))
        aggs = p.get("aggregations", {"age":"mean","amount":"sum"})
        parts = [f'{rename.get(k,k)}=("{k}","{v}")' for k,v in aggs.items()]
        by = p.get("group_by") or p.get("columns") or ["department"]
        code += f'df=df.groupby({by}).agg({",".join(parts)}).reset_index()\n'
    if "save" in n: code += f'df.to_parquet("cody_agent/data/top_sales.parquet",index=False)\nprint("成功！文件已保存")\n'

print("生成代码：\n", code)
exec(code)
print(pd.read_parquet("cody_agent/data/top_sales.parquet"))
