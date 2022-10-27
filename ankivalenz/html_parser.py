import itertools
import re
from typing import List, Tuple
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag

from .types import ClozeNode, Delimeter, Node

BASIC_REGEXP = r"(.*?)\s*(::\?|\?::|::)\s*(.*)"
STANDALONE_REGEXP = r"^(::\?|\?::|::)\s*(.*)"
CLOZE_REGEXP = r".*{{c\d+::.*?}}.*"
HEADER_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]

# Returns `True` if `element` is a non-header or a header with
# a lower priority than `header`, i.e. a "descendant", hierarchically
# speaking
def is_descendant(header: str, element: PageElement) -> bool:
    if not (isinstance(element, Tag)):
        return True

    if not (element.name in HEADER_TAGS):
        return True

    return element.name > header


class HtmlParser:
    def parse(self, text: str) -> Tuple[List[Node], List[str]]:
        soup = BeautifulSoup(text, "html.parser")

        paths = self.strip_image_paths(soup)

        return (self.find_nodes(soup.contents), paths)

    # recursively traverse the tree, and modify all image srcs to be the basename only:
    def strip_image_paths(self, elements: List[PageElement]) -> List[str]:
        paths = []

        for i, e in enumerate(elements):
            if isinstance(e, Tag):
                if e.name == "img":
                    paths.append(e["src"])
                    e["src"] = e["src"].split("/")[-1]
                paths.extend(self.strip_image_paths(e.contents))

        return paths

    def find_nodes(self, elements: List[PageElement]) -> List[Node]:
        nodes: List[Node] = []

        for idx, element in enumerate(elements):
            if isinstance(element, Tag):
                if element.name in HEADER_TAGS:
                    header = "".join(map(str, element.contents))

                    children = [
                        *itertools.takewhile(
                            lambda x: is_descendant(element.name, x),
                            elements[idx + 1 :],
                        )
                    ]
                    rest = [
                        *itertools.dropwhile(
                            lambda x: is_descendant(element.name, x),
                            elements[idx + 1 :],
                        )
                    ]

                    nodes.append((header, self.find_nodes(children)))
                    nodes.extend(self.find_nodes(rest))
                    break
                elif element.name == "li":
                    head = [
                        *itertools.takewhile(
                            lambda x: not (
                                isinstance(x, Tag) and x.name in ["ul", "ol"]
                            ),
                            element.children,
                        )
                    ]
                    tail = [
                        *itertools.dropwhile(
                            lambda x: not (
                                isinstance(x, Tag) and x.name in ["ul", "ol"]
                            ),
                            element.children,
                        )
                    ]

                    # if there are any elements in `tail`, it means there is a nested list.
                    if len(tail) > 0:
                        # <li>Header<ul>...</ul></li>
                        if len(head) == 1 and isinstance(head[0], NavigableString):
                            header = str(head[0]).strip()
                            nodes.append((header, self.find_nodes(tail)))
                        else:
                            # in the case of a nested list, the header is the content of
                            # the first tag in `head`. If we do not find a tag in `head`,
                            # we do not consider the nested list, and simply skip it.
                            for e in head:
                                if isinstance(e, Tag):
                                    if e.name == "p":
                                        header = "".join(map(str, e.contents))
                                    else:
                                        header = str(e)

                                    nodes.append((header, self.find_nodes(tail)))
                                    break
                    else:
                        nodes.extend(self.find_nodes(head))
                else:
                    nodes.extend(self.find_nodes(element.contents))
            elif isinstance(element, NavigableString):
                if match := re.match(CLOZE_REGEXP, str(element), re.DOTALL):
                    before = "".join(map(str, elements[:idx]))
                    after = "".join(map(str, elements[idx + 1 :]))

                    nodes.append(before.strip() + str(element).strip() + after.strip())
                    break
                elif match := re.match(STANDALONE_REGEXP, str(element), re.DOTALL):
                    delimeter_type, after_match = match.groups()

                    after = after_match + "".join(map(str, elements[idx + 1 :]))

                    nodes.append((Delimeter(delimeter_type), after.strip()))
                    break
                elif match := re.match(BASIC_REGEXP, str(element), re.DOTALL):
                    before_match, delimeter_type, after_match = match.groups()

                    before = "".join(map(str, elements[:idx])) + before_match
                    after = after_match + "".join(map(str, elements[idx + 1 :]))

                    nodes.append(
                        (before.strip(), Delimeter(delimeter_type), after.strip())
                    )
                    break

        return nodes
