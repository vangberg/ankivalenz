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
from markdown_it import MarkdownIt
from mdit_py_plugins.attrs import attrs_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token
from markdown_it.utils import OptionsDict, EnvType
from typing import Sequence


class Note(genanki.Note):
    pass


def format_path(path: Path) -> str:
    return " > ".join(path)


def _render_markdown(text: str) -> str:
    md = MarkdownIt().use(attrs_plugin).use(dollarmath_plugin)

    def render_math_inline(
        self: RendererProtocol,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        content = str(tokens[idx].content).strip()
        return f"\\({content}\\)"

    def render_math_block(
        self: RendererProtocol,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        content = str(tokens[idx].content).strip()
        return f"\\[\n{content}\n\\]\n"

    # Override render rules for math to use \( and \[
    md.add_render_rule("math_inline", render_math_inline)
    md.add_render_rule("math_block", render_math_block)

    # Parse and render the markdown
    return md.render(text).strip()


def create_basic_note(card: BasicCard, updated_tag: str) -> Note:
    return Note(
        model=BASIC_AND_REVERSED_CARD_MODEL if card.reverse else BASIC_MODEL,
        fields=[
            _render_markdown(card.question),
            _render_markdown(card.answer),
            format_path(card.path),
        ],
        tags=[updated_tag],
    )


def create_cloze_note(card: ClozeCard, updated_tag: str) -> Note:
    return Note(
        model=CLOZE_MODEL,
        fields=[
            _render_markdown(card.question),
            "",
            format_path(card.path),
        ],
        tags=[updated_tag],
    )


def get_updated_tag(time: datetime) -> str:
    ts_int = int(time.timestamp())
    return "ankivalenz:updated:{}".format(ts_int)


def cards_to_notes(cards: List[Card], time: Optional[datetime]) -> List[Note]:
    if time is None:
        time = datetime.now()

    notes = []
    updated_tag = get_updated_tag(time)

    for card in cards:
        if isinstance(card, BasicCard):
            notes.append(create_basic_note(card, updated_tag))
        if isinstance(card, ClozeCard):
            notes.append(create_cloze_note(card, updated_tag))

    return notes


def load_cards(
    path: pathlib.Path, extension: str = "md"
) -> Tuple[List[Card], List[str]]:
    cards = []
    image_paths = []

    for file in path.glob("**/*.{}".format(extension)):
        with file.open() as f:
            (nodes, paths) = MarkdownParser().parse(f.read())
            cards.extend(NodeParser().parse(nodes))

            for path in paths:
                image_paths.append(os.path.join(file.parent, path))

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
