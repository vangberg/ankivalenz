# Ankivalenz

Ankivalenz is a tool for generating Anki notes from HTML files.

## Tutorial

In this walk-through we will write our notes as Markdown files, use
pandoc[^pandoc] to convert them to HTML, and finally use Ankivalenz to
generate an Anki deck with cards extracted from our notes.

### Installation

Ankivalenz is distributed as a Python package, and requires Python 3.10+. To install:

```
$ pip3 install ankivalenz
```

### Initialize project

Create a folder for your notes:

```
$ mkdir Notes
$ cd Notes
```

Ankivalenz needs a configuration file, containing the name and ID of the
Anki deck. This can be generated with `ankivalenz init`:

```
$ ankivalenz init
```

### Write note

Add the following to a file named `Cell.md`:

```markdown
# Cell

## Types

- Prokaryotic ?:: does not contain a nucleus
- Eukaryotic ?:: contains a nucleus
```

### Generate Anki deck

Convert it to HTML:

```
$ pandoc Cell.md > Cell.html
```

And run Ankivalenz:

```
$ ankivalenz run .
```

This generates a file `Notes.apkg` that can be imported to Anki. Open
Anki and go to File -> Import, and find `Notes.apkg`.

### Review cards

The new Anki deck will have two notes:

// Turn the following table into a Github Flavored Markdown table:

| Question    | Answer                     | Path         |
| ----------- | -------------------------- | ------------ |
| Prokaryotic | does not contain a nucleus | Cell > Types |
| Eukaryotic  | contains a nucleus         | Cell > Types |

This is what the first note looks like in Anki:

![Anki review](images/anki-review.png)

[^pandoc]: https://pandoc.org/
