from flowbeast.fp3.schema import ViralUnit
from flowbeast.fp3.builder import build_fp3

units = [
    ViralUnit(
        hook="她结婚当天，新郎消失",
        pattern="婚礼反转",
        emotion=["shock", "anger"]
    ),
    ViralUnit(
        hook="他死了三年突然出现",
        pattern="死亡反转",
        emotion=["shock", "fear"]
    )
]

build_fp3(units)
