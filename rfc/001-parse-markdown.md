# Parse Markdown

## Current situation

Ankivalenz currently parses HTML. The user is responsible for converting markdown to HTML.

## Proposal

Ankivalenz should parse Markdown directly.

## Implementation

1. Migrate the tests in `tests/test_html_parser.py` to use Markdown.
2. Create a new `tests/test_markdown_parser.py` file that tests the new Markdown parser.
3. Implement the new Markdown parser in `ankivalenz/markdown_parser.py` using `mistletoe`.