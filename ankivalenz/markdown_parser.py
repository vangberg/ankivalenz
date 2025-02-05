import itertools
import re
from typing import List, Sequence, Tuple
from ankivalenz.html_parser import HtmlParser
from markdown_it import MarkdownIt
from mdit_py_plugins.attrs import attrs_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token
from markdown_it.utils import OptionsDict, EnvType

from .types import ClozeNode, Delimeter, Node

BASIC_REGEXP = r"(.*?)\s*(::\?|\?::|::)\s*(.*)"
STANDALONE_REGEXP = r"^(::\?|\?::|::)\s*(.*)"
CLOZE_REGEXP = r".*{{c\d+::.*"


class MarkdownParser:
    def __init__(self):
        self.md = MarkdownIt()

    def parse(self, text: str) -> Tuple[List[Node], List[str]]:
        md = MarkdownIt().use(attrs_plugin).use(dollarmath_plugin, double_inline=True)

        def render_math_inline(
            self: RendererProtocol,
            tokens: Sequence[Token],
            idx: int,
            options: OptionsDict,
            env: EnvType,
        ) -> str:
            content = str(tokens[idx].content).strip()
            return f"\\({content}\\)"

        # Override render rules for math to use \( and \[
        md.add_render_rule("math_inline", render_math_inline)

        # Parse and render the markdown
        html = md.render(text).strip()

        return HtmlParser().parse(html)
