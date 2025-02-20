from datetime import datetime
import json
import os
import pathlib
import random
from typing import List, Optional, Tuple

from ankivalenz.markdown_parser import MarkdownParser
from ankivalenz.node_parser import NodeParser
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

    ts = time.timestamp()
    ts_int = int(ts)

    updated_tag = "ankivalenz:updated:{}".format(ts_int)

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


def load_cards(
    path: pathlib.Path, extension: str = "md"
) -> Tuple[List[Card], List[str]]:
    cards = []
    image_paths = []

    for file_path in path.glob("**/*.{}".format(extension)):
        with file_path.open() as f:
            (nodes, ips) = MarkdownParser().parse(f.read())
            cards.extend(NodeParser().parse(nodes))

            for ip in ips:
                # Resolve e.g. "a/../b" to "b"
                ip = (
                    file_path.parent.joinpath(ip)
                    .resolve()
                    .relative_to(pathlib.Path.cwd())
                )

                image_paths.append(ip)

    return (cards, image_paths)


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

    input_path = path / settings.get("input_path", "")
    input_ext = settings.get("input_ext", "md")

    (cards, image_paths) = load_cards(input_path, extension=input_ext)

    deck = genanki.Deck(
        settings["deck_id"],
        settings["deck_name"],
    )

    for note in cards_to_notes(cards, time=time):
        deck.add_note(note)

    package = genanki.Package(deck)

    for image_path in list(set(image_paths)):
        package.media_files.append(image_path)

    return package
