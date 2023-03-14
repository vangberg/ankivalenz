import textwrap

from bs4 import BeautifulSoup
from ankivalenz import HtmlParser, Node
from ankivalenz.html_parser import is_descendant
from ankivalenz.types import Delimeter


class TestIsHeaderWithEqualOrHigherLevel:
    def setup_method(self):
        self.header = BeautifulSoup("<h3>Header 3</h3>", "html.parser").h3

    def test_h2_vs_h3(self):
        assert is_descendant("h2", self.header) == True

    def test_h3_vs_h3(self):
        assert is_descendant("h3", self.header) == False

    def test_h4_vs_h3(self):
        assert is_descendant("h4", self.header) == False


class TestHeaders:
    def test_nested_headers(self):
        md = textwrap.dedent(
            """
        <h1>Header A-1</h1>

        <h2>Header A-2</h2>

        <h1>Header B-1</h1>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Header A-1", [("Header A-2", [])]), ("Header B-1", [])] == nodes

    def test_header_with_markup(self):
        md = textwrap.dedent(
            """
        <h1>Header <em>A</em></h1>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Header <em>A</em>", [])] == nodes


class TestList:
    def test_list(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>A :: B</li>
            <li>C ?:: D</li>
            <li>E ::? F</li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [
            ("A", Delimeter("::"), "B"),
            ("C", Delimeter("?::"), "D"),
            ("E", Delimeter("::?"), "F"),
        ] == nodes

    def test_list_with_paragraph(self):
        md = textwrap.dedent(
            """
        <ul>
            <li><p>A :: B</p></li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("A", Delimeter("::"), "B")] == nodes

    def test_list_with_html(self):
        md = textwrap.dedent(
            """
        <ul>
            <li><p>A <i>italic</i> :: B <strong>strong</strong></p></li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [
            ("A <i>italic</i>", Delimeter("::"), "B <strong>strong</strong>")
        ] == nodes

    def test_list_with_image(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>A ?:: B<br><img src="image.png"></li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("A", Delimeter("?::"), 'B<br/><img src="image.png"/>')] == nodes

    def test_list_with_cloze(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>Cloze {{c1::deletion}}</li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Cloze {{c1::deletion}}")] == nodes

    def test_list_with_cloze_with_html(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>Cloze {{c1::<sup>deletion</sup>}}</li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Cloze {{c1::<sup>deletion</sup>}}")] == nodes

    def test_list_with_cloze_and_image_after_cloze(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>Cloze {{c1::deletion}}<br><img src="image.png"></li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [('Cloze {{c1::deletion}}<br/><img src="image.png"/>')] == nodes

    def test_list_with_cloze_and_image_before_cloze(self):
        md = textwrap.dedent(
            """
        <ul>
            <li><img src="image.png"><br>Cloze {{c1::deletion}}</li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [('<img src="image.png"/><br/>Cloze {{c1::deletion}}')] == nodes


class TestImages:
    def test_strips_path_from_image(self):
        md = textwrap.dedent(
            """
        <li>Question ?:: Answer <img src="foo/bar.png"/></li>
        """
        )

        (nodes, image_paths) = HtmlParser().parse(md)

        assert [("Question", Delimeter("?::"), 'Answer <img src="bar.png"/>')] == nodes
        assert ["foo/bar.png"] == image_paths


class TestNestedList:
    def test_nested_list(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>
                <p>A</p>
                <ul>
                    <li>B :: C</li>
                </ul>
            </li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("A", [("B", Delimeter("::"), "C")])] == nodes

    def test_nested_list_without_paragraph(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>
                A
                <ul>
                    <li>B :: C</li>
                </ul>
            </li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("A", [("B", Delimeter("::"), "C")])] == nodes

    def test_multiple_nested_lists(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>
                <p>List 1</p>
                <ul>
                    <li>Question 1 ?:: Answer 1</li>
                </ul>
            </li>
            <li>
                <p>List 2</p>
                <ul>
                    <li>Question 2 ?:: Answer 2</li>
                </ul>
            </li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [
            ("List 1", [("Question 1", Delimeter("?::"), "Answer 1")]),
            ("List 2", [("Question 2", Delimeter("?::"), "Answer 2")]),
        ] == nodes

    def test_nested_list_and_standalone_answer(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>
                <p>Question</p>
                <ul>
                    <li>?:: Standalone answer</li>
                </ul>
            </li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Question", [(Delimeter("?::"), "Standalone answer")])] == nodes

    def test_nested_list_and_image(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>
                <p><img src="bar.png"/></p>
                <ul>
                    <li>Question ?:: Answer</li>
                </ul>
            </li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [
            ('<img src="bar.png"/>', [("Question", Delimeter("?::"), "Answer")])
        ] == nodes


class TestStandalone:
    def test_header_and_standalone_answer(self):
        md = textwrap.dedent(
            """
        <h1>Header</h1>
        <ul>
            <li>?:: Standalone answer</li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Header", [(Delimeter("?::"), "Standalone answer")])] == nodes

    def test_header_and_standalone_question(self):
        md = textwrap.dedent(
            """
        <h1>Header</h1>
        <ul>
            <li>::? Standalone question</li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Header", [(Delimeter("::?"), "Standalone question")])] == nodes

    def test_header_and_standalone_two_way(self):
        md = textwrap.dedent(
            """
        <h1>Header</h1>
        <ul>
            <li>:: Standalone two-way</li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Header", [(Delimeter("::"), "Standalone two-way")])] == nodes


class TestMath:
    def test_inline_math(self):
        md = textwrap.dedent(
            """
        <ul>
            <li>Question ?:: Answer \\(\\sin^2\\)</li>
        </ul>
        """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Question", Delimeter("?::"), "Answer \\(\\sin^2\\)")] == nodes

    def test_block_math(self):
        md = textwrap.dedent(
            """
            <ul>
            <li>Question ?::
            Answer
            \\[
            \\sin^2
            \\]
            </li>
            </ul>
            """
        )

        (nodes, _) = HtmlParser().parse(md)

        assert [("Question", Delimeter("?::"), "Answer\n\\[\n\\sin^2\n\\]")] == nodes
