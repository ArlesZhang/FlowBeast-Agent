# 外部入口:这个文件让你能从命令行轻松操作，支持处理单文件或整个文件夹

import argparse
import asyncio
from pathlib import Path
from flowbeast.fp3.feedback import FP3Feedback
from flowbeast.core.config import settings


def main():
    parser = argparse.ArgumentParser(description="FlowBeast FP3 自动回流工具（经 QualityGate）")
    parser.add_argument("--file", type=str, help="指定回流的剧本 JSON 文件路径")
    parser.add_argument("--dir", type=str, help="批量处理文件夹下的所有剧本")
    parser.add_argument("--yes", action="store_true", help="跳过人工确认，自动进化")

    args = parser.parse_args()
    feedback = FP3Feedback()

    async def run():
        if args.file:
            await feedback.process_file_async(Path(args.file), auto_confirm=args.yes)
        elif args.dir:
            target_dir = Path(args.dir)
            for json_file in sorted(target_dir.glob("*.json")):
                await feedback.process_file_async(json_file, auto_confirm=args.yes)
        else:
            default_dir = Path(settings.FLOWBEAST_OUTPUT_DIR)
            print(f"未指定路径，是否处理默认输出目录? {default_dir} (y/n)")
            if input().lower() == 'y':
                for json_file in sorted(default_dir.glob("*.json")):
                    await feedback.process_file_async(json_file, auto_confirm=args.yes)

    asyncio.run(run())


if __name__ == "__main__":
    main()
