from genanki import Model


BASIC_MODEL = Model(
    1456156020,
    "Basic (Ankivalenz)",
    fields=[
        {
            "name": "Front",
            "font": "Arial",
        },
        {
            "name": "Back",
            "font": "Arial",
        },
        {
            "name": "Path",
            "font": "Arial",
        },
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "<small>{{Path}}</small><br><br>{{Front}}",
            "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
        },
    ],
    css=".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n",
)

BASIC_AND_REVERSED_CARD_MODEL = Model(
    2105966946,
    "Basic (and reversed card) (Ankivalenz)",
    fields=[
        {
            "name": "Front",
            "font": "Arial",
        },
        {
            "name": "Back",
            "font": "Arial",
        },
        {
            "name": "Path",
            "font": "Arial",
        },
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "<small>{{Path}}</small><br><br>{{Front}}",
            "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
        },
        {
            "name": "Card 2",
            "qfmt": "<small>{{Path}}</small><br><br>{{Back}}",
            "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}",
        },
    ],
    css=".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n",
)

CLOZE_MODEL = Model(
    1642839314,
    "Cloze (Ankivalenz)",
    model_type=Model.CLOZE,
    fields=[
        {
            "name": "Text",
            "font": "Arial",
        },
        {
            "name": "Back Extra",
            "font": "Arial",
        },
        {
            "name": "Path",
            "font": "Arial",
        },
    ],
    templates=[
        {
            "name": "Cloze",
            "qfmt": "<small>{{Path}}</small><br><br>{{cloze:Text}}",
            "afmt": "<small>{{Path}}</small><br><br>{{cloze:Text}}<br>\n{{Back Extra}}",
        },
    ],
    css=".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n\n"
    ".cloze {\n font-weight: bold;\n color: blue;\n}\n.nightMode .cloze {\n color: lightblue;\n}",
)
