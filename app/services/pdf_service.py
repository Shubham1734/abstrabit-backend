from io import BytesIO

from pypdf import PdfReader


class PdfService:

    @staticmethod
    def extract_text(file_bytes: bytes):

        reader = PdfReader(
            BytesIO(file_bytes)
        )

        full_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                full_text += text + "\n"

        return full_text