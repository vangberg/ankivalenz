from datetime import datetime
import pathlib
from ankivalenz import package

class TestGenerator:
    def setup_method(self):
        self.time = datetime.fromtimestamp(12345)
        self.package = package(pathlib.Path('sample/Biology'), time=self.time)
        self.deck = self.package.decks[0]

    def test_deck_id(self):
        assert 1956515595 == self.deck.deck_id

    def test_deck_name(self):
        assert 'Sample::Biology' == self.deck.name

    def test_media_files(self):
        # sort the array to make the test deterministic

        assert sorted(['sample/Biology/images/flagella.png',
                'sample/Biology/images/prokaryotic-capsule.png']) == \
            sorted(self.package.media_files)

    def test_notes(self):
        for n in self.deck.notes:
            print(n.fields)
        assert 11 == len(self.deck.notes)

    def test_tag(self):
        assert 'ankivalenz:updated:12345' == \
                         self.deck.notes[0].tags[0]
