# AI Reader

AI Reader is a desktop application that allows you to summarize documents and ask questions about them using a local AI model (Foundry).

## Features

- Load PDF, DOCX, or TXT documents
- Generate concise summaries of documents
- Ask questions about the content
- Works with local AI models (Phi-3.5-mini)
- GUI built with CustomTkinter

## Requirements

- Python 3.10+
- `customtkinter`
- `requests`
- `PyPDF2`
- `python-docx`
- `foundry_local`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Start the Foundry local model server and load the model (phi-3.5-mini).

Run the app:

```bash
python app.py
```

Load a document.

View the summary or ask questions.

## Notes

CPU inference may be slow (~30–60s per request)

Maximum text length per request: ~2000 characters
