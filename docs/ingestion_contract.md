# Ingestion Contract

## Purpose

Person A's ingestion pipeline supports multiple input formats (PDF, DOCX, XLSX, images, email, TXT). Regardless of source format, ingestion outputs **one normalized JSON shape**. This is the only thing Person B (embeddings/RAG) and Person C (backend/API) should ever consume — neither should contain any format-specific branching logic.

## Supported source formats (Week 1–4 scope)

| Type | Extensions | Parser library | Difficulty |
|---|---|---|---|
| Text-based PDF | `.pdf` | `pdfplumber` / `PyMuPDF` | Easy |
| Scanned PDF / image | `.pdf` (image-only), `.png`, `.jpg`, `.tiff` | Tesseract OCR | Medium |
| Word | `.docx` | `python-docx` | Easy |
| Excel/CSV | `.xlsx`, `.csv` | `openpyxl` / `pandas` | Easy |
| PowerPoint | `.pptx` | `python-pptx` | Easy (stretch) |
| Email | `.eml`, `.msg` | `email` (stdlib) / `extract-msg` | Medium |
| Plain text | `.txt` | built-in | Trivial |

## Output schema

```json
{
  "document_id": "uuid",
  "source_type": "pdf | docx | xlsx | image | email | txt",
  "storage_path": "minio://bucket/path/to/file.pdf",
  "ocr_applied": true,
  "pages": [
    { "page_number": 1, "text": "extracted text for page 1..." },
    { "page_number": 2, "text": "extracted text for page 2..." }
  ],
  "metadata": {
    "filename": "invoice_042.pdf",
    "mime_type": "application/pdf",
    "size_bytes": 245880,
    "uploaded_by": "user_uuid",
    "folder": "invoices",
    "created_at": "2026-07-09T10:00:00Z"
  }
}
```

## Field notes

- **`document_id`** — primary key, matches the `documents` table row created at upload time.
- **`source_type`** — tells consumers nothing more than "how was this parsed"; no downstream code should switch on it.
- **`storage_path`** — where the original file lives (local path in dev, `minio://` URI in prod).
- **`ocr_applied`** — `true` if Tesseract ran on this document; lets the frontend show an "OCR processed" indicator.
- **`pages`** — always an array, even for single-page or non-paginated formats (e.g. a `.txt` file is `page_number: 1`, a `.csv` can be treated as `page_number: 1` with the full sheet as text, or split per-sheet for `.xlsx`).
  - Page-level granularity is required, not optional — it's what allows Person B to store `document_id + page_number` next to each vector, which is what makes source citations possible in Module 1.
- **`metadata`** — everything Person C needs to populate the `documents` and `metadata` DB tables directly; no re-parsing required.

## Consumer responsibilities

- **Person B**: chunk `pages[].text`, embed each chunk, store `document_id` + `page_number` as vector metadata in Chroma.
- **Person C**: write `metadata` + `storage_path` into the relational DB; expose `ocr_applied` / processing status to the frontend for upload progress.

## Why this contract matters

Agreeing on this shape before parser code is written prevents rework in Weeks 4–5 when Person B and C's code starts depending on ingestion output. Any new source format added later only requires a new parser that outputs this same shape — no changes required downstream.
