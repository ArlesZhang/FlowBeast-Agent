"""Real-time trending topic fetcher for creative topic seeding.

Current sources:
- Weibo hot search (free, no API key, China-accessible)

Usage:
    from flowbeast.drama.trending import fetch_trending_context
    ctx = await fetch_trending_context()
    print(ctx.creative_brief())
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime

import httpx
from loguru import logger


@dataclass
class TrendingItem:
    title: str
    hot_score: int = 0
    source: str = ""
    rank: int = 0
    url: str = ""


@dataclass
class TrendContext:
    platform: str = ""
    fetched_at: str = ""
    topics: list[TrendingItem] = field(default_factory=list)

    def creative_brief(self) -> str:
        """Compress into a compact text block for prompt injection."""
        if not self.topics:
            return ""
        lines = [f"  #{t.rank} [热{t.hot_score}] {t.title}" for t in self.topics[:10]]
        header = f"### 实时热搜话题（来源：{self.platform}）\n"
        return header + "\n".join(lines)


async def fetch_weibo_trending(limit: int = 20) -> list[TrendingItem]:
    """Fetch Weibo hot search list. No auth required."""
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://weibo.com",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    items = data.get("data", {}).get("realtime", [])
    if not items:
        logger.warning("⚠️ 微博热搜返回空结果")
        return []

    results = []
    for i, entry in enumerate(items[:limit]):
        title = entry.get("word", "").strip()
        if not title:
            continue
        results.append(
            TrendingItem(
                title=title,
                hot_score=int(entry.get("raw_hot", 0)),
                source="weibo",
                rank=i + 1,
                url=f"https://s.weibo.com/weibo?q={title}",
            )
        )

    logger.info(f"🔥 微博热搜获取成功 | {len(results)} 条")
    return results


async def fetch_trending_context(
    platforms: list[str] = ["weibo"],
    limit: int = 10,
) -> TrendContext:
    """Fetch trending topics from specified platforms."""
    topics: list[TrendingItem] = []

    if "weibo" in platforms:
        try:
            topics = await fetch_weibo_trending(limit=limit)
        except Exception as e:
            logger.warning(f"⚠️ 微博热搜抓取失败: {e}")

    return TrendContext(
        platform=",".join(platforms),
        fetched_at=datetime.now().isoformat(),
        topics=topics,
    )
