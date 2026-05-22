from flowbeast.fp3.seed_data import get_demo_units
from flowbeast.fp3.builder import build_fp3
from loguru import logger


def run_init():
    """初始化 FP3 向量库（使用 seed_data 中的 15 条种子数据）。"""
    units = get_demo_units()
    build_fp3(units)
    logger.success("✅ FP3 初始基因库构建完成！")


if __name__ == "__main__":
    run_init()
