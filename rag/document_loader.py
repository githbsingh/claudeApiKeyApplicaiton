from pathlib import Path

from pypdf import PdfReader


class DocumentLoader:

    @staticmethod
    def load_pdf(file_path: str) -> str:
        from pathlib import Path

        path = Path(file_path)

        print("PDF path:", path)
        print("Exists:", path.exists())
        print("Size:", path.stat().st_size if path.exists() else 0)

        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)

    @staticmethod
    def load_text(file_path: str) -> str:

        return Path(
            file_path
        ).read_text(
            encoding="utf-8"
        )

    @classmethod
    def load(cls, file_path: str) -> str:

        path = Path(file_path)

        extension = path.suffix.lower()

        if extension == ".pdf":

            return cls.load_pdf(
                file_path
            )

        if extension == ".txt":

            return cls.load_text(
                file_path
            )

        raise ValueError(
            f"Unsupported file type: {extension}"
        )