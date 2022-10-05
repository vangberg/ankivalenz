import itertools
import re
from typing import List
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag

from .types import Delimeter, Node

BASIC_REGEXP = r'(.*?)\s*(::\?|\?::|::)\s*(.*)'
STANDALONE_REGEXP = r'^(::\?|\?::|::)\s*(.*)'
CLOZE_REGEXP = r'.*{{c\d+::.*?}}.*'
HEADER_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

# Returns `True` if `element` is a non-header or a header with
# a lower priority than `header`, i.e. a "descendant", hierarchically
# speaking
def is_descendant(header: str, element: PageElement) -> bool:
    if not(isinstance(element, Tag)):
        return True
    
    if not(element.name in HEADER_TAGS):
        return True

    return element.name > header

class HtmlParser:
    def parse(self, text: str) -> List[Node]:
        soup = BeautifulSoup(text, 'html.parser')

        self.strip_image_paths(soup)

        return self.find_nodes(soup.contents)
    
    # recursively traverse the tree, and modify all image srcs to be the basename only:
    def strip_image_paths(self, elements: List[PageElement]) -> None:
        for i, e in enumerate(elements):
            if isinstance(e, Tag):
                if e.name == 'img':
                    e['src'] = e['src'].split('/')[-1]
                self.strip_image_paths(e.contents)
    
    def find_nodes(self, elements: List[PageElement]) -> List[Node]:
        nodes = []
        
        for idx, element in enumerate(elements):
            if isinstance(element, Tag):
                if element.name in HEADER_TAGS:
                    header = ''.join(map(str, element.contents))

                    children = [*itertools.takewhile(
                        lambda x: is_descendant(element.name, x),
                        elements[idx+1:]
                    )]
                    rest = [*itertools.dropwhile(
                        lambda x: is_descendant(element.name, x),
                        elements[idx+1:]
                    )]

                    nodes.append((header, self.find_nodes(children)))
                    nodes.extend(self.find_nodes(rest))
                    break
                elif element.name == 'li':
                    head = [
                        *itertools.takewhile(
                            lambda x: not(isinstance(x, Tag) and x.name in ['ul', 'ol']),
                            element.children
                        )
                    ]
                    tail = [
                        *itertools.dropwhile(
                            lambda x: not(isinstance(x, Tag) and x.name in ['ul', 'ol']),
                            element.children
                        )
                    ]

                    # if there are any elements in `tail`, it means there is a nested list.
                    if len(tail) > 0:
                        # in the case of a nested list, the header is the content of
                        # the first tag in `head`. If we do not find a tag in `head`,
                        # we do not consider the nested list, and simply skip it.
                        for e in head:
                            if isinstance(e, Tag):
                                header = ''.join(map(str, e.contents))
                                nodes.append((header, self.find_nodes(tail)))
                                break
                    else:
                        nodes.extend(self.find_nodes(head))
                else:
                    nodes.extend(self.find_nodes(element.contents))
            elif isinstance(element, NavigableString):
                if match := re.match(CLOZE_REGEXP,  str(element)):
                    nodes.append((str(element)))
                    break
                elif match := re.match(STANDALONE_REGEXP, str(element)):
                    delimeter_type, after_match = match.groups()

                    after = after_match + ''.join(map(str, elements[idx+1:]))

                    nodes.append((Delimeter(delimeter_type), after))
                    break
                elif match := re.match(BASIC_REGEXP, str(element)):
                    before_match, delimeter_type, after_match = match.groups()

                    before = ''.join(map(str, elements[:idx])) + before_match
                    after = after_match + ''.join(map(str, elements[idx+1:]))

                    nodes.append((before, Delimeter(delimeter_type), after))
                    break

        return nodes