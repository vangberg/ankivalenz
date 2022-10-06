from datetime import datetime
import json
import pathlib
from ankivalenz.generator import package, load_cards
from ankivalenz.types import BasicCard


class TestLoadCards:
    def test_loads_cards(self):
        cards = load_cards(pathlib.Path("sample/Biology"))

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
                    answer="\\(C\\)",
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
                    question='<br/>\n<img src="prokaryotic-capsule.png" width="150"/>',
                    answer="Capsule",
                    path=["Cell", "Prokaryotic"],
                    reverse=False,
                ),
                BasicCard(
                    question="a",
                    answer="Monotrichous",
                    path=["Cell", "Flagella", '<img src="flagella.png" width="150"/>'],
                    reverse=False,
                ),
                BasicCard(
                    question="b",
                    answer="Lophotrichous",
                    path=["Cell", "Flagella", '<img src="flagella.png" width="150"/>'],
                    reverse=False,
                ),
                BasicCard(
                    question="c",
                    answer="Amphitrichous",
                    path=["Cell", "Flagella", '<img src="flagella.png" width="150"/>'],
                    reverse=False,
                ),
                BasicCard(
                    question="d",
                    answer="Peritrichous",
                    path=["Cell", "Flagella", '<img src="flagella.png" width="150"/>'],
                    reverse=False,
                ),
            ]
        ) == sorted(cards)


class TestPackage:
    def setup_method(self):
        self.time = datetime.fromtimestamp(12345)
        self.package = package(pathlib.Path("sample/Biology"), time=self.time)
        self.deck = self.package.decks[0]

    def test_deck_id(self):
        assert 1956515595 == self.deck.deck_id

    def test_deck_name(self):
        assert "Sample::Biology" == self.deck.name

    def test_media_files(self):
        # sort the array to make the test deterministic

        assert sorted(
            [
                "sample/Biology/images/flagella.png",
                "sample/Biology/images/prokaryotic-capsule.png",
            ]
        ) == sorted(self.package.media_files)

    def test_notes(self):
        assert 12 == len(self.deck.notes)

    def test_tag(self):
        assert "ankivalenz:updated:12345" == self.deck.notes[0].tags[0]
