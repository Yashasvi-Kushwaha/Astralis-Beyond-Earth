from pathlib import Path
from pypdf import PdfReader


class PDFLoader:

    def load_pdf(self, pdf_path: str):
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)

        reader = PdfReader(pdf_path)

        pages = []

        for i, page in enumerate(reader.pages):

            text = page.extract_text()

            if text:

                pages.append({
                    "page": i + 1,
                    "text": text
                })

        return pages