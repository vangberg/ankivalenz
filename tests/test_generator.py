from datetime import datetime, timezone
import json
import pathlib
from ankivalenz.generator import (
    package,
    load_cards,
)
from ankivalenz.anki_models import (
    BASIC_MODEL,
    BASIC_AND_REVERSED_CARD_MODEL,
    CLOZE_MODEL,
)
from ankivalenz.types import BasicCard, ClozeCard


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
                    question="\\(A + B\\)",
                    answer="\\(\\dfrac{C}{D}\\)",
                    path=["Chemistry", "Reaction"],
                    reverse=False,
                ),
                BasicCard(
                    question="Math",
                    answer='<img alt="Flagella" src="flagella.png" width="150"/><br/>\n\\(1 + 2 = \\dfrac{3}{4}\\)',
                    path=["Chemistry", "Reaction"],
                    reverse=False,
                ),
                BasicCard(
                    question="Prokaryotic",
                    answer="does <strong>not</strong> contain a nucleus",
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
                    question='<img alt="Prokaryotic Capsule" src="prokaryotic-capsule.png" width="150"/>',
                    answer="Capsule",
                    path=["Cell", "Prokaryotic"],
                    reverse=False,
                ),
                BasicCard(
                    question="a",
                    answer="Monotrichous",
                    path=[
                        "Cell",
                        "Flagella",
                        '<img alt="Flagella" src="flagella.png"/>',
                    ],
                    reverse=False,
                ),
                BasicCard(
                    question="b",
                    answer="Lophotrichous",
                    path=[
                        "Cell",
                        "Flagella",
                        '<img alt="Flagella" src="flagella.png"/>',
                    ],
                    reverse=False,
                ),
                BasicCard(
                    question="c",
                    answer="Amphitrichous",
                    path=[
                        "Cell",
                        "Flagella",
                        '<img alt="Flagella" src="flagella.png"/>',
                    ],
                    reverse=False,
                ),
                BasicCard(
                    question="d",
                    answer="Peritrichous",
                    path=[
                        "Cell",
                        "Flagella",
                        '<img alt="Flagella" src="flagella.png"/>',
                    ],
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
