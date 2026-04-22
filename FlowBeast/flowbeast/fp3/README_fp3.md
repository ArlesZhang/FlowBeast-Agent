以 v0.2.0-stable 为基准，分步完成 FP3 的闭环：FP3 (知识库) -> 检索 -> 注入 Prompt -> 生成增强。

1. 环境准备 (关键)
在开始写代码前，确保你的环境里有 FAISS（向量数据库的核心）。

2. 第一步：定义数据协议 (flowbeast/fp3/schema.py)
我们需要统一“爆款基因”的格式。

4. 第三步：向量化工具 (flowbeast/fp3/embedding.py)
注意： 这里绝对不要在顶部导入 generator，防止循环引用。

5. 第四步：注入逻辑 (flowbeast/fp3/injector.py)
这是将检索到的东西“缝合”进 Prompt 的地方。

6. 第五步：检索中枢 (flowbeast/fp3/retriever.py)


整体结构:

feedback（产生候选内容）
        ↓
QualityGate（做决策）   # 唯一的“守门人”
        ↓
store（进入长期记忆 FP3）



# ======== 🚀 重新点火：构建知识库 ================ #
现在，我们要写一个脚本来注入第一批数据,即:新建 scripts/init_fp3.py


# ======= 完成后,下一步的,最优执行顺序 ========= #

完成后,下一步的,最优执行顺序:
1.第一优先级：自动回流
2.第二优先级：Hook Library
3.第三优先级：SDK 升级

