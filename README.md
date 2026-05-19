# Snippy

A terminal-based code snippet manager built with [Textual](https://textual.textualize.io).

## Features

- Browse snippets in a sidebar list
- View snippet code in a text area
- Create new snippets
- Save snippets to disk as JSON
- Delete existing snippets
- Copy snippet content to clipboard

## Project Structure

```
snippy/
├── pyproject.toml
├── README.md
├── snippets/                        # 
└── snippy/                          # Package root
    ├── __init__.py
    ├── __main__.py                  # App entry point
    └── services/
        ├── __init__.py
        ├── clipboard.py             # Copy content to clipboard
        ├── search.py
        └── storage.py               # Load/save/delete snippets
```

Each snippet is a JSON file with `title`, `language`, and `content` fields.

## Installation

```bash
pip install -e .
```

## Usage

```bash
snippy
```

Or from the project root:

```bash
python -m snippy
```

## Dependencies

- [Textual](https://textual.textualize.io) — TUI framework
- [pyperclip](https://github.com/asweigart/pyperclip) — clipboard access
