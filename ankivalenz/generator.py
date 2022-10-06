from datetime import datetime
import json
import os
import pathlib
import random
from typing import List, Optional

from ankivalenz import HtmlParser, NodeParser
from .anki_models import BASIC_AND_REVERSED_CARD_MODEL, BASIC_MODEL, CLOZE_MODEL
from .types import BasicCard, Card, ClozeCard, Path
import genanki


class Note(genanki.Note):
    pass


def format_path(path: Path) -> str:
    return " > ".join(path)


def cards_to_notes(cards: List[Card], time: Optional[datetime]) -> List[Note]:
    if time is None:
        time = datetime.now()

    notes = []

    updated_tag = "ankivalenz:updated:{}".format(int(time.timestamp()))

    for card in cards:
        if isinstance(card, BasicCard):
            note = Note(
                model=BASIC_AND_REVERSED_CARD_MODEL if card.reverse else BASIC_MODEL,
                fields=[card.question, card.answer, format_path(card.path)],
                # Add tag `ankivalenz:updated:<time in epoch>` to note.
                tags=[updated_tag],
            )
            notes.append(note)
        if isinstance(card, ClozeCard):
            note = Note(
                model=CLOZE_MODEL,
                fields=[card.question, "", format_path(card.path)],
                tags=[updated_tag],
            )
            notes.append(note)

    return notes


def load_cards(path: pathlib.Path) -> List[Card]:
    cards = []

    for file in path.glob("**/*.html"):
        with file.open() as f:
            cards.extend(NodeParser().parse(HtmlParser().parse(f.read())))

    return cards


def init(path: pathlib.Path) -> str:
    deck_id = random.randrange(1 << 30, 1 << 31)
    # set deck_name to the name of the directory:
    deck_name = path.name
    json_path = path / "ankivalenz.json"

    with open(json_path, "w") as f:
        json.dump(
            {"deck_id": deck_id, "deck_name": deck_name},
            f,
            indent=4,
            sort_keys=True,
        )

    return json_path


def package(path: pathlib.Path, time: Optional[datetime] = None) -> genanki.Package:
    with open(os.path.join(path, "ankivalenz.json")) as f:
        settings = json.load(f)

    cards = load_cards(path)

    deck = genanki.Deck(
        settings["deck_id"],
        settings["deck_name"],
    )

    for note in cards_to_notes(cards, time=time):
        deck.add_note(note)

    package = genanki.Package(deck)

    for file in path.glob("images/*"):
        package.media_files.append(str(file))

    return package
