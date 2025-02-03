from typing import List, Tuple, Optional
from mistletoe import Document
from mistletoe.block_token import Heading, ListItem, List as MistletoeList
from mistletoe.span_token import RawText, Emphasis, Strong, Image, LineBreak
import re
from .types import Node, Delimeter


class MarkdownParser:
    """
    A parser that converts markdown to a structured format suitable for Anki card generation.
    Handles headers, lists, cloze deletions, images, and math expressions.
    """

    def __init__(self):
        # Keep track of image paths to handle image file management
        self.image_paths = []

    def parse(self, text: str) -> Tuple[List[Node], List[str]]:
        """
        Parse markdown text into a structured format.

        Args:
            text: The markdown text to parse

        Returns:
            A tuple of (nodes, image_paths) where:
            - nodes is a list of parsed nodes (headers, lists, etc.)
            - image_paths is a list of original image paths found in the markdown
        """
        doc = Document(text)
        self.image_paths = []
        nodes = self._parse_nodes(doc.children)
        return (nodes, self.image_paths)

    def _get_node_content(self, node) -> str:
        """
        Convert a mistletoe node to its string representation.
        Handles various node types (text, emphasis, strong, images, etc.).

        Special handling for images:
        - Strips paths from image sources
        - Collects original image paths for later use
        """
        if isinstance(node, RawText):
            return node.content
        if isinstance(node, Emphasis):
            return f"*{self._get_node_content(node.children[0])}*"
        if isinstance(node, Strong):
            return f"**{self._get_node_content(node.children[0])}**"
        if isinstance(node, Image):
            # Handle image paths - strip them but remember the original
            if "/" in node.src:
                self.image_paths.append(node.src)
                filename = node.src.split("/")[-1]
                return f"![{node.title or ''}]({filename})"
            return f"![{node.title or ''}]({node.src})"
        if isinstance(node, LineBreak):
            return "\n"
        if hasattr(node, "children"):
            return "".join(self._get_node_content(child) for child in node.children)
        return str(node)

    def _parse_list_item(self, item: ListItem) -> Node:
        """
        Parse a list item, handling both simple items and items with nested lists.

        For nested lists:
        - Extracts the content before the nested list
        - Recursively processes nested items
        - Maintains the correct hierarchy
        """
        content = self._get_node_content(item)

        # If this item has a nested list
        if any(isinstance(child, MistletoeList) for child in item.children):
            # Get the content before the nested list (the parent content)
            prefix_content = "".join(
                self._get_node_content(child)
                for child in item.children
                if not isinstance(child, MistletoeList)
            )
            # Process each nested list item
            nested_items = []
            for child in item.children:
                if isinstance(child, MistletoeList):
                    for nested_item in child.children:
                        if isinstance(nested_item, ListItem):
                            nested_content = self._get_node_content(nested_item)
                            nested_items.append(
                                self._parse_list_content(nested_content)
                            )
            return (prefix_content.strip(), nested_items)

        return self._parse_list_content(content)

    def _parse_list_content(self, content: str) -> Node:
        """
        Parse the content of a list item, handling:
        - Cloze deletions (e.g., {{c1::text}})
        - Delimiters (::, ?::, ::?) for question/answer pairs

        Returns the appropriate node structure based on the content type.
        """
        # Check for cloze deletions first - these should be preserved as-is
        cloze_pattern = r".*{{c\d+::.*?}}.*"
        if re.match(cloze_pattern, content, re.DOTALL):
            return content.strip()

        # Match different delimiter patterns for Q&A pairs
        pattern = r"(.*?)\s*(::\?|\?::|::)\s*(.*)"
        if match := re.match(pattern, content, re.DOTALL):
            before, delimiter_type, after = match.groups()
            return (before.strip(), Delimeter(delimiter_type), after.strip())
        return content

    def _parse_nodes(self, tokens: List) -> List[Node]:
        """
        Parse a list of markdown tokens into our node structure.
        Handles:
        - Headers with proper nesting
        - Lists (simple and nested)
        - Maintains document hierarchy
        """
        nodes: List[Node] = []
        current_node: Optional[Tuple[str, List]] = None
        current_level = 0

        for token in tokens:
            if isinstance(token, Heading):
                content = self._get_node_content(token)

                # Handle headers based on their level and current context
                if token.level == 1:
                    # Top-level header starts a new section
                    if current_node:
                        nodes.append(current_node)
                    current_node = (content, [])
                    current_level = token.level
                elif current_node and token.level > current_level:
                    # Subheading - add to current section
                    current_node[1].append((content, []))
                else:
                    # New section at same or higher level
                    if current_node:
                        nodes.append(current_node)
                    current_node = (content, [])
                    current_level = token.level
            elif isinstance(token, MistletoeList):
                # Process each list item
                for item in token.children:
                    if isinstance(item, ListItem):
                        nodes.append(self._parse_list_item(item))

        # Don't forget the last node
        if current_node:
            nodes.append(current_node)

        return nodes
