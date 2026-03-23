## Goal

在7天内实现：

输入一句话 → 输出一条短剧视频（30-60秒）

不追求自动化，不追求质量，只验证闭环


## Pipeline (MVP)

1. Prompt → 生成短剧JSON（IP2）
2. JSON → 生成配音（ElevenLabs）
3. 图片 + 音频 → 拼视频（CapCut）
4. 输出视频


## Script JSON Schema

```json
{
  "title": "",
  "scenes": [
    {
      "hook": "",
      "emotion": "",
      "dialogue": [
        {"speaker": "A", "text": ""}
      ]
    }
  ]
}


---

## 4. 工具选型（只写最小）

```md
## Tools

- LLM：FlowBeast（IP2）
- Voice：ElevenLabs
- Video：CapCut（手动）


## Success Criteria

- 能生成1条完整视频
- 视频具备基本剧情结构（钩子→冲突→反转）
- 可以发到平台（哪怕质量低）
