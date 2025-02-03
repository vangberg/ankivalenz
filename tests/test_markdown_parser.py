import textwrap

from ankivalenz import MarkdownParser
from ankivalenz.types import Delimeter


class TestHeaders:
    def test_nested_headers(self):
        md = textwrap.dedent("""
            # Header A-1

            ## Header A-2

            # Header B-1
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("Header A-1", [("Header A-2", [])]), ("Header B-1", [])] == nodes

    def test_header_with_markup(self):
        md = textwrap.dedent("""
            # Header *A*
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("Header *A*", [])] == nodes


class TestList:
    def test_list(self):
        md = textwrap.dedent("""
            - A :: B
            - C ?:: D
            - E ::? F
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            ("A", Delimeter("::"), "B"),
            ("C", Delimeter("?::"), "D"),
            ("E", Delimeter("::?"), "F"),
        ] == nodes

    def test_list_with_markup(self):
        md = textwrap.dedent("""
            - A *italic* :: B **strong**
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("A *italic*", Delimeter("::"), "B **strong**")] == nodes

    def test_list_with_image(self):
        md = textwrap.dedent("""
            - A ?:: B  
              ![](image.png)
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("A", Delimeter("?::"), "B\n![](image.png)")] == nodes

    def test_list_with_cloze(self):
        md = textwrap.dedent("""
            - Cloze {{c1::deletion}}
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("Cloze {{c1::deletion}}")] == nodes

    def test_list_with_cloze_with_markup(self):
        md = textwrap.dedent("""
            - Cloze {{c1::^deletion^}}
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("Cloze {{c1::^deletion^}}")] == nodes

    def test_list_with_cloze_and_image_after_cloze(self):
        md = textwrap.dedent("""
            - Cloze {{c1::deletion}}  
              ![](image.png)
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("Cloze {{c1::deletion}}\n![](image.png)")] == nodes

    def test_list_with_cloze_and_image_before_cloze(self):
        md = textwrap.dedent("""
            - ![](image.png)  
              Cloze {{c1::deletion}}
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("![](image.png)\nCloze {{c1::deletion}}")] == nodes


class TestImages:
    def test_strips_path_from_image(self):
        md = textwrap.dedent("""
            - Question ?:: Answer ![](foo/bar.png)
            """)

        (nodes, image_paths) = MarkdownParser().parse(md)

        assert [("Question", Delimeter("?::"), "Answer ![](bar.png)")] == nodes
        assert ["foo/bar.png"] == image_paths


class TestNestedList:
    def test_nested_list(self):
        md = textwrap.dedent("""
            - A
              - B :: C
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("A", [("B", Delimeter("::"), "C")])] == nodes

    def test_multiple_nested_lists(self):
        md = textwrap.dedent("""
            - List 1
              - Question 1 ?:: Answer 1
            - List 2
              - Question 2 ?:: Answer 2
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            ("List 1", [("Question 1", Delimeter("?::"), "Answer 1")]),
            ("List 2", [("Question 2", Delimeter("?::"), "Answer 2")]),
        ] == nodes

    def test_nested_list_and_standalone_answer(self):
        md = textwrap.dedent("""
            - Question
              - ?:: Standalone answer
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("Question", [("", Delimeter("?::"), "Standalone answer")])] == nodes

    def test_nested_list_and_image(self):
        md = textwrap.dedent("""
            - Question
              - ?:: Answer  
                ![](image.png)
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            ("Question", [("", Delimeter("?::"), "Answer\n![](image.png)")])
        ] == nodes


class TestMath:
    def test_inline_math(self):
        md = textwrap.dedent("""
            - Question with $x^2$ :: Answer with $y^2$
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("Question with $x^2$", Delimeter("::"), "Answer with $y^2$")] == nodes

    def test_block_math(self):
        md = textwrap.dedent("""
            - Question with
              $$
              x^2
              $$
              :: Answer with
              $$
              y^2
              $$
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            (
                "Question with\n$$\nx^2\n$$",
                Delimeter("::"),
                "Answer with\n$$\ny^2\n$$",
            )
        ] == nodes
