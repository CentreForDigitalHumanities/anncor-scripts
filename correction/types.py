from os import PathLike
from typing import Callable, List, NewType, Union

from lxml import etree

ParseTree = NewType('ParseTree', etree._ElementTree)
Element = NewType('Element', etree._Element)
QueryFunction = Callable[[ParseTree], bool]
ReplaceFunction = Callable[[ParseTree], None]
Path = Union[str, PathLike]
