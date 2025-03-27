import re
import os
from collections import defaultdict
import argparse
from pathlib import Path

# Regex patterns to parse the clippings file
# Pattern for the book title and author line
# Handles authors like (Author, Name), (Author), (Author1; Author2)
TITLE_AUTHOR_RE = re.compile(r"^(.*?)\s+\((.*?)\)$")

# Pattern for the metadata line (page/location, date)
METADATA_RE = re.compile(
    r"^- Your Highlight on (page (?P<page>\d+(-?\d+)?) \| )?" # Optional page number/range
    r"(Location (?P<location>\d+(-?\d+)?)\s*\| |"           # Optional location number/range (needs page OR location)
    r"(?P<location_only>Location \d+(-?\d+)?)\s*\| )?"      # Optional location only (alternative format)
    r"Added on (?P<date>.*?)$"                              # Date added
)

# Separator between clippings
SEPARATOR = "=========="

def sanitize_filename(filename):
    """
    Removes or replaces characters invalid in filenames, keeping spaces
    and replacing colons with dashes.
    """
    # Replace colons with dashes first
    sanitized = filename.replace(":", " -")
    # Remove characters invalid in most filesystems (excluding colon now)
    sanitized = re.sub(r'[\\/*?"<>|]', "", sanitized)
    # Replace multiple consecutive whitespace characters with a single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    # Remove leading/trailing whitespace
    sanitized = sanitized.strip()
    # Limit length (optional, but good practice)
    max_len = 150
    if len(sanitized) > max_len:
        # Try to cut at the last space before max_len
        cut_point = sanitized.rfind(' ', 0, max_len)
        if cut_point != -1:
            sanitized = sanitized[:cut_point]
        else:
            # If no space found, just truncate
            sanitized = sanitized[:max_len]
    return sanitized

def parse_clippings(input_file_path):
    """
    Parses the 'My Clippings.txt' file and returns a dictionary
    structured by book.
    """
    try:
        # Use utf-8-sig to handle the BOM (Byte Order Mark) often present
        with open(input_file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file_path}'")
        return None
    except Exception as e:
        print(f"Error reading input file: {e}")
        return None

    clippings = content.split(SEPARATOR)
    print(f"Found {len(clippings)} potential clippings (including separators).")

    # Use defaultdict to easily append highlights to lists
    books = defaultdict(list)
    processed_count = 0

    for clipping in clippings:
        clipping = clipping.strip() # Remove leading/trailing whitespace
        if not clipping:
            continue # Skip empty sections resulting from split

        lines = clipping.split('\n')
        if len(lines) < 3:
            # print(f"Skipping invalid clipping (too few lines): {lines[:1]}...") # Optional: for debugging
            continue

        # --- 1. Parse Title and Author ---
        title_author_match = TITLE_AUTHOR_RE.match(lines[0])
        if not title_author_match:
            # print(f"Skipping clipping - couldn't parse title/author: {lines[0]}") # Optional: for debugging
            continue
        title = title_author_match.group(1).strip()
        author = title_author_match.group(2).strip()
        book_key = (title, author) # Use tuple as dict key

        # --- 2. Parse Metadata ---
        metadata_match = METADATA_RE.match(lines[1])
        if not metadata_match:
            # print(f"Skipping clipping - couldn't parse metadata: {lines[1]}") # Optional: for debugging
            continue
        metadata = metadata_match.groupdict()

        # Construct attribution string
        attribution_parts = []
        if metadata.get('page'):
            attribution_parts.append(f"Page {metadata['page']}")
        # Handle the two possible location formats
        loc = metadata.get('location') or metadata.get('location_only')
        if loc:
            # Remove "Location " prefix if it exists from location_only
            loc_val = loc.replace("Location ", "").strip()
            attribution_parts.append(f"Location {loc_val}")
        if metadata.get('date'):
            attribution_parts.append(f"Added on {metadata['date']}")
        attribution = " | ".join(attribution_parts)

        # --- 3. Extract Highlight Text ---
        highlight_text = "\n".join(lines[2:]).strip()
        if not highlight_text:
            # print(f"Skipping clipping - empty highlight text for: {title}") # Optional: for debugging
            continue

        # Store the parsed data
        books[book_key].append({"text": highlight_text, "attribution": attribution})
        processed_count += 1

    print(f"Successfully processed {processed_count} clippings from {len(books)} books.")
    return books

def create_markdown_files(books, output_dir):
    """
    Creates Markdown files for each book in the specified directory.
    Removes H1 title, uses spaces in filenames, replaces colons with dashes.
    """
    output_path = Path(output_dir)
    # Create the output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"\nWriting Markdown files to: '{output_path.resolve()}'")

    file_count = 0
    for (title, author), highlights in books.items():
        # Create a safe filename from the title using the updated sanitizer
        filename_base = sanitize_filename(title)
        output_filename = output_path / f"{filename_base}.md"

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                # --- MODIFICATION: Removed H1 Title ---
                # f.write(f"# {title}\n") # <-- This line is removed/commented out

                # Write author and separator (placed at the top now)
                f.write(f"_by {author}_\n\n")
                f.write("---\n\n") # Separator after author

                # Sort highlights (optional, e.g., by date or location if needed,
                # but requires more complex parsing of the attribution string)
                # For now, keep the order they appeared in the clippings file.

                for i, highlight in enumerate(highlights):
                    # Format highlight text as a blockquote
                    quote_lines = highlight['text'].split('\n')
                    for line in quote_lines:
                        f.write(f"> {line}\n") # Add blockquote marker to each line

                    # Add attribution below the quote
                    f.write(f"\n_– {highlight['attribution']}_\n")

                    # Add a separator between highlights, but not after the last one
                    if i < len(highlights) - 1:
                        f.write("\n---\n\n")
                    else:
                        f.write("\n") # Just a newline after the last one

            print(f"Created: {output_filename.name}")
            file_count += 1
        except Exception as e:
            print(f"Error writing file '{output_filename.name}': {e}")

    print(f"\nFinished creating {file_count} Markdown files.")


# --- Main Execution ---
if __name__ == "__main__":
    # Set up argument parser for command-line usage
    parser = argparse.ArgumentParser(
        description="Convert Kindle 'My Clippings.txt' to Markdown files per book."
    )
    parser.add_argument(
        "input_file",
        nargs='?', # Make the argument optional
        default="My Clippings.txt", # Default input filename
        help="Path to the 'My Clippings.txt' file (default: My Clippings.txt in the script's directory)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="Kindle_Markdown_Notes", # Default output directory name
        help="Directory to save the generated Markdown files (default: Kindle_Markdown_Notes)",
    )

    args = parser.parse_args()

    input_file_path = args.input_file
    output_directory = args.output_dir

    print(f"Starting Kindle clippings conversion...")
    print(f"Input file: '{input_file_path}'")
    print(f"Output directory: '{output_directory}'")

    # Parse the clippings
    parsed_books = parse_clippings(input_file_path)

    # Create Markdown files if parsing was successful
    if parsed_books:
        create_markdown_files(parsed_books, output_directory)
    else:
        print("Exiting due to parsing errors.")