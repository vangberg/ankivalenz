from datetime import datetime
import pathlib
import typer
from importlib import metadata
from . import generator

app = typer.Typer()


@app.command()
def help():
    typer.echo("Ankivalenz is a tool for converting Markdown files to Anki decks.")
    typer.echo("Usage: ankivalenz [OPTIONS] COMMAND [ARGS]...")
    typer.echo("Commands:")
    typer.echo("  init    Initialize an ankivalenz.json file")
    typer.echo("  run    Run Ankivalenz")
    typer.echo("  version    Show the version of Ankivalenz")
    typer.echo("  help    Show this message and exit.")


@app.command()
def version():
    typer.echo(f"Ankivalenz version {metadata.version('ankivalenz')}")


@app.command()
def run(path: str):
    time = datetime.now()
    full_path = pathlib.Path(path)
    package = generator.package(full_path, time=time)

    apkg_path = package.decks[0].name + ".apkg"
    package.write_to_file(apkg_path)

    typer.echo(
        "- Added {} notes to deck {} in {}".format(
            len(package.decks[0].notes), package.decks[0].name, apkg_path
        )
    )
    typer.echo("- Import the .apkg file into Anki (File -> Import)")
    typer.echo("- Find and delete orphaned notes with this filter (Browse):")
    typer.echo(
        '    deck:"{}" -tag:ankivalenz:updated:{}'.format(
            package.decks[0].name, int(time.timestamp())
        )
    )


@app.command()
def init(path: str):
    full_path = pathlib.Path(path).resolve()
    json_path = generator.init(full_path)

    typer.echo("Created ankivalenz.json at {}".format(json_path))
