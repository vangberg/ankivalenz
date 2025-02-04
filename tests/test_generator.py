from datetime import datetime, timezone
import json
import pathlib
from ankivalenz.generator import (
    package,
    load_cards,
    create_basic_note,
    create_cloze_note,
)
from ankivalenz.anki_models import (
    BASIC_MODEL,
    BASIC_AND_REVERSED_CARD_MODEL,
    CLOZE_MODEL,
)
from ankivalenz.types import BasicCard, ClozeCard


class TestCreateBasicNote:
    def test_creates_basic_note(self):
        card = BasicCard(
            question="What is X?",
            answer="X is Y",
            path=["Biology", "Chapter 1"],
            reverse=False,
        )
        note = create_basic_note(card, "test_tag")

        assert note.model == BASIC_MODEL
        assert note.fields == [
            "<p>What is X?</p>",
            "<p>X is Y</p>",
            "Biology > Chapter 1",
        ]
        assert note.tags == ["test_tag"]

    def test_creates_reversed_note(self):
        card = BasicCard(
            question="What is X?",
            answer="X is Y",
            path=["Biology", "Chapter 1"],
            reverse=True,
        )
        note = create_basic_note(card, "test_tag")

        assert note.model == BASIC_AND_REVERSED_CARD_MODEL
        assert note.fields == [
            "<p>What is X?</p>",
            "<p>X is Y</p>",
            "Biology > Chapter 1",
        ]
        assert note.tags == ["test_tag"]

    def test_renders_markdown_emphasis(self):
        card = BasicCard(
            question="What is **bold** and *italic*?",
            answer="This is __bold__ and _italic_",
            path=["Biology", "Chapter 1"],
            reverse=False,
        )
        note = create_basic_note(card, "test_tag")

        assert note.fields == [
            "<p>What is <strong>bold</strong> and <em>italic</em>?</p>",
            "<p>This is <strong>bold</strong> and <em>italic</em></p>",
            "Biology > Chapter 1",
        ]

    def test_renders_images(self):
        card = BasicCard(
            question='Image with attributes: ![Flagella](flagella.png){width="150"}',
            answer="Plain image: ![Flagella](flagella.png)",
            path=["Biology", "Chapter 1"],
            reverse=False,
        )
        note = create_basic_note(card, "test_tag")

        assert note.fields == [
            '<p>Image with attributes: <img src="flagella.png" alt="Flagella" width="150" /></p>',
            '<p>Plain image: <img src="flagella.png" alt="Flagella" /></p>',
            "Biology > Chapter 1",
        ]

    def test_renders_inline_math(self):
        card = BasicCard(
            question="What is $x + y$?",
            answer="The sum is $z$",
            path=["Biology", "Chapter 1"],
            reverse=False,
        )
        note = create_basic_note(card, "test_tag")

        assert note.fields == [
            "<p>What is \\(x + y\\)?</p>",
            "<p>The sum is \\(z\\)</p>",
            "Biology > Chapter 1",
        ]

    def test_renders_block_math(self):
        card = BasicCard(
            question="What is:\n\n$$\nx + y = z\n$$",
            answer="The equation\n\n$$a + b = c$$\n\nshows the sum",
            path=["Biology", "Chapter 1"],
            reverse=False,
        )
        note = create_basic_note(card, "test_tag")

        assert note.fields == [
            "<p>What is:</p>\n\\[\nx + y = z\n\\]",
            "<p>The equation</p>\n\\[\na + b = c\n\\]\n<p>shows the sum</p>",
            "Biology > Chapter 1",
        ]


class TestCreateClozeNote:
    def test_creates_cloze_note(self):
        card = ClozeCard(question="{{c1::X}} is Y", path=["Biology", "Chapter 1"])
        note = create_cloze_note(card, "test_tag")

        assert note.model == CLOZE_MODEL
        assert note.fields == [
            "<p>{{c1::X}} is Y</p>",
            "",
            "Biology > Chapter 1",
        ]
        assert note.tags == ["test_tag"]

    def test_renders_markdown_emphasis(self):
        card = ClozeCard(
            question="The {{c1::*important*}} part is **bold**",
            path=["Biology", "Chapter 1"],
        )
        note = create_cloze_note(card, "test_tag")

        assert note.fields == [
            "<p>The {{c1::<em>important</em>}} part is <strong>bold</strong></p>",
            "",
            "Biology > Chapter 1",
        ]

    def test_renders_images(self):
        card = ClozeCard(
            question='The {{c1::image}} shows: ![Flagella](flagella.png){width="150"} and ![Flagella](flagella.png)',
            path=["Biology", "Chapter 1"],
        )
        note = create_cloze_note(card, "test_tag")

        assert note.fields == [
            '<p>The {{c1::image}} shows: <img src="flagella.png" alt="Flagella" width="150" /> and <img src="flagella.png" alt="Flagella" /></p>',
            "",
            "Biology > Chapter 1",
        ]

    def test_renders_inline_math(self):
        card = ClozeCard(
            question="The {{c1::sum}} of $x + y$ is $z$",
            path=["Biology", "Chapter 1"],
        )
        note = create_cloze_note(card, "test_tag")

        assert note.fields == [
            "<p>The {{c1::sum}} of \\(x + y\\) is \\(z\\)</p>",
            "",
            "Biology > Chapter 1",
        ]

    def test_renders_block_math(self):
        card = ClozeCard(
            question="The {{c1::equation}} is:\n\n$$\nx + y = z\n$$",
            path=["Biology", "Chapter 1"],
        )
        note = create_cloze_note(card, "test_tag")

        assert note.fields == [
            "<p>The {{c1::equation}} is:</p>\n\\[\nx + y = z\n\\]",
            "",
            "Biology > Chapter 1",
        ]


class TestLoadCards:
    def test_loads_cards(self):
        (cards, _) = load_cards(pathlib.Path("sample/Biology"))
        assert sorted(
            [
                BasicCard(
                    question="Covalent bond",
                    answer="electrons are shared",
                    path=["Chemistry", "Bonds"],
                    reverse=True,
                ),
                BasicCard(
                    question="Ionic bond",
                    answer="electrons are transferred",
                    path=["Chemistry", "Bonds"],
                    reverse=True,
                ),
                BasicCard(
                    question="$A + B$",
                    answer="$\\dfrac{C}{D}$",
                    path=["Chemistry", "Reaction"],
                    reverse=False,
                ),
                BasicCard(
                    question="Math",
                    answer='![Flagella](flagella.png){width="150"}\n$$\n1 + 2 = \\dfrac{3}{4}\n$$',
                    path=["Chemistry", "Reaction"],
                    reverse=False,
                ),
                BasicCard(
                    question="Prokaryotic",
                    answer="does **not** contain a nucleus",
                    path=["Cell", "Types"],
                    reverse=True,
                ),
                BasicCard(
                    question="Domains",
                    answer="Eukarya",
                    path=["Cell", "Types", "Prokaryotic"],
                    reverse=False,
                ),
                BasicCard(
                    question="Eukaryotic",
                    answer="contains a nucleus",
                    path=["Cell", "Types"],
                    reverse=True,
                ),
                BasicCard(
                    question="Domains",
                    answer="Bacteria, Archaea",
                    path=["Cell", "Types", "Eukaryotic"],
                    reverse=False,
                ),
                BasicCard(
                    question='![Prokaryotic Capsule](prokaryotic-capsule.png){width="150"}',
                    answer="Capsule",
                    path=["Cell", "Prokaryotic"],
                    reverse=False,
                ),
                BasicCard(
                    question="a",
                    answer="Monotrichous",
                    path=["Cell", "Flagella", "![Flagella](flagella.png)"],
                    reverse=False,
                ),
                BasicCard(
                    question="b",
                    answer="Lophotrichous",
                    path=["Cell", "Flagella", "![Flagella](flagella.png)"],
                    reverse=False,
                ),
                BasicCard(
                    question="c",
                    answer="Amphitrichous",
                    path=["Cell", "Flagella", "![Flagella](flagella.png)"],
                    reverse=False,
                ),
                BasicCard(
                    question="d",
                    answer="Peritrichous",
                    path=["Cell", "Flagella", "![Flagella](flagella.png)"],
                    reverse=False,
                ),
            ]
        ) == sorted(cards)


class TestPackage:
    def setup_method(self):
        self.time = datetime.fromtimestamp(12345, tz=timezone.utc)
        self.package = package(pathlib.Path("sample/Biology"), time=self.time)
        self.deck = self.package.decks[0]

    def test_deck_id(self):
        assert 1956515595 == self.deck.deck_id

    def test_deck_name(self):
        assert "Sample::Biology" == self.deck.name

    def test_media_files(self):
        paths = [
            "sample/Biology/images/flagella.png",
            "sample/Biology/images/prokaryotic-capsule.png",
        ]

        # convert paths in self.package.media_files to posix
        # to make the test work on windows
        media_files = [pathlib.Path(p).as_posix() for p in self.package.media_files]

        # sort the paths to make the test deterministic
        assert sorted(paths) == sorted(media_files)

    def test_tag(self):
        assert "ankivalenz:updated:12345" == self.deck.notes[0].tags[0]
