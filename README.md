# Kindle Clippings to Markdown Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Optional: Choose a license and update badge -->

A Python script to parse your Amazon Kindle's `My Clippings.txt` file and convert your highlights and notes into individual Markdown files, organized by book. Designed for easy integration with note-taking apps like [Obsidian](https://obsidian.md/), [Logseq](https://logseq.com/), etc.

## Features

*   **Parses `My Clippings.txt`:** Reads the standard Kindle clippings file format.
*   **One File Per Book:** Creates a separate Markdown file for each book found in your clippings.
*   **Markdown Formatting:**
    *   Highlights are formatted as Markdown blockquotes (`>`).
    *   Multi-line highlights are correctly formatted.
    *   Attribution (Page, Location, Date Added) is included below each quote in italics.
    *   A horizontal rule (`---`) separates individual highlights within a file.
*   **Obsidian-Friendly Output:**
    *   **No H1 Title:** The script omits the `# Book Title` heading at the start of the file, as Obsidian typically uses the filename as the main heading.
    *   **Clean Filenames:** Book titles are used for filenames, with spaces preserved, colons (`:`) converted to dashes (`-`), and other invalid filesystem characters removed.
*   **Author Information:** Includes the author's name (`_by Author_`) at the beginning of each file.
*   **Configurable:** Use command-line arguments to specify the input file path and the output directory.
*   **Handles BOM:** Correctly reads `My Clippings.txt` which often starts with a UTF-8 BOM (Byte Order Mark).
*   **Cross-Platform:** Written in Python, should run on macOS, Windows, and Linux.

## Requirements

*   **Python 3.x:** The script uses standard libraries included with Python 3 (`re`, `pathlib`, `collections`, `argparse`). No external packages need to be installed via pip.
*   **Your `My Clippings.txt` file:** You need to get this file from your Kindle device (usually found in the `documents` folder when connected via USB).

## Installation

1.  **Clone or Download:**
    *   Clone the repository:
        ```bash
        git clone https://github.com/czekaj/kindle_clippings_to_markdown_files.git
        cd kindle_clippings_to_markdown_files
        ```
    *   Or, download the `kindle_to_markdown.py` script directly.

2.  **Locate `My Clippings.txt`:** Copy your `My Clippings.txt` file into the same directory as the script, or note its full path.

## Usage

Run the script from your terminal.

**Basic Usage (Defaults):**

Assumes `My Clippings.txt` is in the same directory as the script. Creates an output folder named `Kindle_Markdown_Notes` in the current directory.

```bash
python3 kindle_to_markdown.py
```

**Specify Input File:**

```bash
python3 kindle_to_markdown.py "/path/to/your/My Clippings.txt"
```

**Specify Output Directory:**

```bash
python3 kindle_to_markdown.py -o "/path/to/your/desired/output_folder"
```
*Or using the long flag:*
```bash
python3 kindle_to_markdown.py --output-dir "My Notes/Kindle Imports"
```

**Specify Both Input and Output:**

```bash
python3 kindle_to_markdown.py "/path/to/clippings_backup.txt" -o "Obsidian Vault/Imports/Kindle"
```

### Arguments

*   `input_file` (optional positional argument): Path to the `My Clippings.txt` file. Defaults to `My Clippings.txt` in the script's directory.
*   `-o` or `--output-dir` (optional flag): Path to the directory where the Markdown files will be saved. Defaults to `Kindle_Markdown_Notes` in the current directory.

## Input Format (`My Clippings.txt`)

The script expects the standard format generated by Kindle devices:

```
Book Title (Author Name)
- Your Highlight on page X | Location Y-Z | Added on Day, Month DD, YYYY HH:MM:SS AM/PM

Highlight text content goes here. It can span
multiple lines.
==========
Another Book Title (Another Author)
- Your Note on Location ZZZ | Added on Day, Month DD, YYYY HH:MM:SS AM/PM

This is a note.
==========
```

## Output Format (`[Sanitized Book Title].md`)

Example output file named `The Rosie Project - A Novel (Don Tillman Book 1).md`:

```markdown
_by Simsion, Graeme_

---

> “You’re kidding.” It was an odd response. Why would I make a confusing joke with someone I barely knew?

_– Page 42 | Location 468-469 | Added on Tuesday, April 20, 2021 7:04:34 AM_

---

> “No assistance is required,” I said. “I recommend reading a book.” I watched Rosie walk to the bookshelf, briefly peruse the contents, then walk away. Perhaps she used IBM rather than Apple software, although many of the manuals applied to both.

_– Page 51 | Location 581-583 | Added on Tuesday, April 20, 2021 7:24:01 AM_

---

> “Surreptitiously.”

_– Page 72 | Location 816-816 | Added on Wednesday, April 21, 2021 7:21:05 AM_

```

## Troubleshooting

*   **Encoding Errors:** The script attempts to read the file using `utf-8-sig` to handle the BOM. If you encounter encoding issues, ensure your `My Clippings.txt` is saved in a compatible UTF-8 format.
*   **Parsing Errors:** If Amazon changes the format of `My Clippings.txt` significantly, the regular expressions in the script might need updating. Please open an issue if you encounter consistent parsing problems.
*   **Filename Issues:** Filename sanitization removes common invalid characters (`\ / * ? " < > |`) and replaces colons (`:`) with dashes (`-`). If you have titles with very unusual characters that cause issues on your OS, you might need to adjust the `sanitize_filename` function.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find bugs, please feel free to:

1.  Open an issue to discuss the change or report the bug.
2.  Fork the repository.
3.  Create a new branch (`git checkout -b feature/your-feature-name`).
4.  Make your changes.
5.  Commit your changes (`git commit -m 'Add some feature'`).
6.  Push to the branch (`git push origin feature/your-feature-name`).
7.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
