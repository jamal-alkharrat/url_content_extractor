# URL Content Extractor
A Python utility for extracting content from URLs and providing flexible output formats, such as Markdown and TXT. Simplify the retrieval and formatting of web content.

## Table of Contents
- [URL Content Extractor](#url-content-extractor)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
    - [Pip](#pip)
  - [Usage](#usage)
    - [Command Line](#command-line)
  - [Tests](#tests)

## Features
- Extract content from a URL
- Output content in Markdown or TXT format

### Future Features
- Extract content from a list of URLs
- Output content in HTML format
- Output content in PDF format
- Output content in DOCX format
- Output content in JSON format

## Requirements
- [Python](https://www.python.org/downloads/) 3.8+ (tested with 3.12)

## Installation

### Pip

```bash
pip install -r requirements.txt
```


## Usage
Either import the module into your own Python project or use the command line interface.
### Command Line

```bash
python ./url_content_extractor/main.py --url https://www.google.com --output markdown.md
```

## Tests

Run tests in command line with pytest:
```bash
pytest
```

You can also run tests with DEBUG logging enabled:
```bash
pytest --log-cli-level=DEBUG
```