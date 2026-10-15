# Current Goal: 拿到第一笔真实付费证据

> **⚠️ 商业化定位（2026-10-15）。** 完整论证见
> [commercialization_playbook.zh.md](commercialization_playbook.zh.md)。
>
> 市场反馈表明，静态语料壁垒、低价抽取服务、特定品牌命名以及提示词包等四条早期创业路径已被证伪。
> AI 2.0 时代轻资产模式已难以为继，从业者需要转向更深层的系统级工作流集成与业务结果交付。
>
> **新方向：** 面向中国小型短剧团队的陪跑式 AI 短剧制作，**按交付成片集数收费**（服务，不是 SaaS）。
> 免费公开评分器是获客入口，不是产品。

**唯一验收标准：有真实付费证据。** 在客户为一集成片付过钱之前，一切都不算数。

**Phase:** 商业化验证（取代原 Phase 0 语料库阶段）
**Timeline:** 30 天

---

## Mission

用**现有代码**交付一集成片给一个真实客户，并收到钱。

不是把系统做完美，而是证明「**这套流程能换钱**」。

---

## 这个阶段的三个任务

### 1. 打通交付路径（本地即可）

端到端跑通并产出一份可交给客户的成片包：

```
话题 → FP3 检索 → 剧本 → 分镜 → 配音 → episode_audio.mp3 + prompt_package.json
```

**验收：** 拿一个真实话题，跑完，产物能放进客户手里，不需要我在旁边解释每一步。

### 2. 找到第一个客户

面向已经在小规模做短剧、但卡在产能或成本上的团队。**不做公开 SaaS，不谈 API**，谈的是：
「你给我一个方向，我给你一集成片。」

**验收：** 有人愿意为「一集成片」报价，且不是「先免费试用看看」。

### 3. 把免费评分器做成获客入口

公开的短剧开场评分器 —— 输入开场文案，得到可解释的反馈。它不赚钱，它**换来对话**。

**验收：** 有陌生人用过，并留下联系方式。

---

## 明确不做

- ❌ 不再建静态语料壁垒 / 逆向工程流水线（已证伪，代码已删）
- ❌ 不再写 VTO 算子（GRAFT/PARASITE/DISTORT/MISDIRECT/THEFT，已证伪）
- ❌ 不做提示词包生意（已证伪）
- ❌ 不做低价抽取服务（已证伪）
- ❌ 不完美化 QualityGate、不追求架构完整
- ❌ **不重复造轮子** —— 市场上能找到替代的，一律集成 / 借鉴（见 [CLAUDE.md](../../CLAUDE.md) 规则 0）
- ❌ 项目定型前不修镜像、不修 CI、不写部署文档

---

## 已知的、暂时接受的欠账

不是不管，是**排在这三件事之后**：

| 欠账 | 影响 | 什么时候修 |
|------|------|-----------|
| QualityGate 从未给出 ACCEPT，权重未标定 | 质量分不可信，但不阻塞交付 | 有付费客户后 |
| FP3 只有约 20 条手写演示数据 | 换话题后结果雷同 | 有付费客户后，用真实交付内容反哺 |
| Docker 内缺 ffmpeg/字体，音频拼接失败 | 容器内跑不通 | 本地跑不受影响，定型后再说 |

细节见 [commercialization_playbook.zh.md](commercialization_playbook.zh.md) Part 0。

---

## Reference Documents

- [commercialization_playbook.zh.md](commercialization_playbook.zh.md) — 商业化手册（**先读这份**）
- [status.md](status.md) — 代码现状：能跑的 vs 桩的
- [roadmap.md](roadmap.md) — 阶段路线图
- [decisions/001_project_positioning.md](decisions/001_project_positioning.md) — 定位决策记录
- [decisions/002_what_we_do_not_do.md](decisions/002_what_we_do_not_do.md) — 硬边界
