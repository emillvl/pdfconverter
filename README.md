# PDFConverter

A small desktop utility for converting images and office documents to PDF through a simple Tkinter file picker.

PDFConverter keeps the workflow intentionally simple:

1. Select one or more files.
2. Enter an output name.
3. The resulting PDF is saved to your desktop.

## Features

- Convert PNG, JPG, JPEG, BMP, and GIF images directly with Pillow.
- Convert office and document formats through LibreOffice.
- Merge multiple converted documents into one PDF.
- Preserve the order in which files were selected.
- Run on Windows, macOS, and Linux.
- Use a native file picker instead of requiring command-line arguments.
- Keep temporary LibreOffice output isolated from your source files.

## Requirements

- Python 3.7+
- Tkinter
- Pillow
- PyPDF2
- LibreOffice for non-image conversion

Tkinter is bundled with many Python distributions. On Linux, it may need to be installed separately through your distribution's package manager.

## Installation

Clone the repository:

```bash
git clone https://github.com/emillvl/pdfconverter.git
cd pdfconverter
```

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

For document conversion, install LibreOffice as well.

### Windows

Install LibreOffice from its official installer. PDFConverter checks common LibreOffice installation locations and also accepts `soffice` or `libreoffice` when available on `PATH`.

### macOS

A common installation method is:

```bash
brew install --cask libreoffice
```

The application also checks the standard LibreOffice application path under `/Applications`.

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install libreoffice python3-tk
```

Other Linux distributions can install the equivalent LibreOffice and Tk packages through their package manager.

## Usage

Run:

```bash
python PDFConverter/converter.py
```

The application will:

1. Open a file-selection dialog.
2. Ask for the output PDF name.
3. Save the result to the detected desktop directory.

If no desktop directory can be detected, PDFConverter falls back to the user's home directory.

## Conversion behavior

### Images

If every selected input is one of the supported image formats, PDFConverter uses Pillow directly and does not require LibreOffice.

Supported image extensions:

- `.png`
- `.jpg`
- `.jpeg`
- `.bmp`
- `.gif`

Images are converted to RGB and written to a single PDF in selection order.

### Documents

If any selected file is not one of the supported image extensions, PDFConverter uses LibreOffice for the conversion flow.

LibreOffice determines which document formats are actually convertible. Typical examples include:

- DOC / DOCX
- XLS / XLSX
- PPT / PPTX
- ODT / ODS / ODP
- RTF

Each source file is converted inside its own temporary directory. This prevents same-named input files from overwriting one another and avoids modifying or deleting PDFs beside the original source files.

When multiple converted PDFs are produced, PyPDF2 merges them in the original selection order.

## Important limitations

- A mixed selection of images and documents is handled through LibreOffice rather than the direct Pillow image path.
- Conversion fidelity for office documents depends on LibreOffice and the fonts available on the machine.
- Password-protected, corrupted, unsupported, or unusually structured files may fail to convert.
- The current GUI is Turkish-language.
- The application does not recursively convert folders.

## Troubleshooting

### LibreOffice could not be found

Confirm that LibreOffice is installed and can be launched normally.

You can also check whether its command is available:

```bash
soffice --version
```

or:

```bash
libreoffice --version
```

On Windows, the executable is commonly located under:

```text
C:\Program Files\LibreOffice\program\soffice.exe
```

### Tkinter is missing

On Ubuntu or Debian:

```bash
sudo apt install python3-tk
```

For other platforms, use the Tk package appropriate for your Python installation.

### Multiple documents do not merge

Reinstall the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

PyPDF2 is required when multiple LibreOffice-generated PDFs need to be merged.

### Output is not on the desktop

PDFConverter uses the configured desktop location when it can detect one. If no valid desktop directory is available, it saves to the user's home directory instead.

## Project structure

```text
pdfconverter/
├── PDFConverter/
│   └── converter.py
├── LICENSE
├── README.md
└── requirements.txt
```

## Development notes

The project deliberately remains lightweight. The conversion logic is contained in a single Python module, while external document rendering is delegated to LibreOffice.

When changing conversion behavior, useful regression cases include:

- one image
- multiple images
- one office document
- multiple office documents
- two files with the same basename from different directories
- a source directory that already contains a PDF with the same basename
- LibreOffice missing
- PyPDF2 missing during a multi-document merge

## License

PDFConverter is licensed under the MIT License. See [LICENSE](LICENSE).

## Author

Emil Veliyev — [@emillvl](https://github.com/emillvl)
