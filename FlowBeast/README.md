# Text_scripts

一句话：一流项目用 pytest + 清晰目录/标记 + pyproject 约定 + CI 分档 + 文档 解决「又全又快」和「脚本 vs 测」的边界；很少靠「一个统一入口文件」。你若要对齐，最小的一步仍是：把能 pytest 的放进 tests/，在 pyproject 里声明 markers，在 CI 里只跑默认子集。