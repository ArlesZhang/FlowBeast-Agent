# flowbeast/drama/schema.py

from typing import List, TypedDict


class Dialogue(TypedDict):
    speaker: str
    text: str


class Scene(TypedDict):
    hook: str
    emotion: str
    dialogue: List[Dialogue]


class Script(TypedDict):
    title: str
    scenes: List[Scene]
