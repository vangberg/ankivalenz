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

        assert [
            (
                "Header A-1",
                [("Header A-2", [])],
            ),
            ("Header B-1", []),
        ] == nodes

    def test_header_with_markup(self):
        md = textwrap.dedent("""
            # Header *A*
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("Header <em>A</em>", [])] == nodes


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

        assert [
            ("A <em>italic</em>", Delimeter("::"), "B <strong>strong</strong>")
        ] == nodes

    def test_list_with_cloze(self):
        md = textwrap.dedent("""
            - Cloze {{c1::deletion}}
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [("Cloze {{c1::deletion}}")] == nodes

    def test_list_with_cloze_and_image_after_cloze(self):
        md = textwrap.dedent("""
            - Cloze {{c1::deletion}}  
              ![](image.png)
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert ['Cloze {{c1::deletion}}<br/>\n<img alt="" src="image.png"/>'] == nodes

    def test_list_with_cloze_and_image_before_cloze(self):
        md = textwrap.dedent("""
            - ![](image.png)  
              Cloze {{c1::deletion}}
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert ['<img alt="" src="image.png"/><br/>Cloze {{c1::deletion}}'] == nodes


class TestHeadersAndList:
    def test_header_and_list(self):
        md = textwrap.dedent("""
            # Header 1

            ## Header 2

            - Question ?:: Answer
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            ("Header 1", [("Header 2", [("Question", Delimeter("?::"), "Answer")])])
        ] == nodes

    def test_header_and_list_with_multiple_items(self):
        md = textwrap.dedent("""
            # Header 1

            ## Header 2
                             
            - List 1
              - Question 1 ?:: Answer 1

            - List 2
              - Question 2 ?:: Answer 2
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            (
                "Header 1",
                [
                    (
                        "Header 2",
                        [
                            ("List 1", [("Question 1", Delimeter("?::"), "Answer 1")]),
                            ("List 2", [("Question 2", Delimeter("?::"), "Answer 2")]),
                        ],
                    )
                ],
            )
        ] == nodes

    def test_headers_and_lists(self):
        md = textwrap.dedent("""
            # Header 1

            ## Header A

            - Question A ?:: Answer A

            ## Header B

            - Question B ?:: Answer B

            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            (
                "Header 1",
                [
                    ("Header A", [("Question A", Delimeter("?::"), "Answer A")]),
                    ("Header B", [("Question B", Delimeter("?::"), "Answer B")]),
                ],
            ),
        ] == nodes


class TestImages:
    def test_parses_width(self):
        md = textwrap.dedent("""
            - Question ?:: Answer ![](bar.png){width="150"}
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            (
                "Question",
                Delimeter("?::"),
                'Answer <img alt="" src="bar.png" width="150"/>',
            )
        ] == nodes

    def test_parses_alt_text(self):
        md = textwrap.dedent("""
            - Question ?:: Answer ![Alt text](bar.png)
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            (
                "Question",
                Delimeter("?::"),
                'Answer <img alt="Alt text" src="bar.png"/>',
            )
        ] == nodes

    def test_strips_path_from_image(self):
        md = textwrap.dedent("""
            - Question ?:: Answer ![](foo/bar.png)
            """)

        (nodes, image_paths) = MarkdownParser().parse(md)

        assert [
            ("Question", Delimeter("?::"), 'Answer <img alt="" src="bar.png"/>')
        ] == nodes
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

        assert [("Question", [(Delimeter("?::"), "Standalone answer")])] == nodes

    def test_nested_list_and_standalone_answer_with_image(self):
        md = textwrap.dedent("""
            - Question
              - ?:: Answer  
                ![](image.png)
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            (
                "Question",
                [(Delimeter("?::"), 'Answer<br/>\n<img alt="" src="image.png"/>')],
            )
        ] == nodes

    def test_nested_list_with_standalone_answer_with_empty_first_line(self):
        md = textwrap.dedent("""
            - Question
              - ?::
                Answer
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            (
                "Question",
                [(Delimeter("?::"), "Answer")],
            )
        ] == nodes

    def test_nested_list_with_standalone_answer_with_empty_first_line_and_image(self):
        md = textwrap.dedent("""
            - Question
              - ?::
                ![](image.png)
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            (
                "Question",
                [(Delimeter("?::"), '<img alt="" src="image.png"/>')],
            )
        ] == nodes


class TestMath:
    def test_inline_math(self):
        md = textwrap.dedent("""
            - Question with $x^2$ :: Answer with $y^2$
            """)

        (nodes, _) = MarkdownParser().parse(md)

        assert [
            ("Question with \\(x^2\\)", Delimeter("::"), "Answer with \\(y^2\\)")
        ] == nodes
