from datetime import datetime
import pathlib
import typer
from . import generator

app = typer.Typer()

@app.command()
def run(path: str):
    time = datetime.now()
    full_path = pathlib.Path(path)
    package = generator.package(full_path, time=time)
    package.write_to_file(package.decks[0].name + '.apkg')

    typer.echo("Find orphaned cards:\n  deck:{} -tag:ankivalenz:updated:{}".format(
        package.decks[0].name, int(time.timestamp())))

