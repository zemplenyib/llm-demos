import os
from pypdf import PdfReader

class Ingest:
    def __init__(self, root_dir_path, chunk_size=500, overlap=50):
        self.root_dir_path = root_dir_path
        self.chunk_size = chunk_size
        self.overlap = overlap

    def read_data(self, path):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def read_folder(self, path):
        texts = []
        path = os.path.join(self.root_dir_path, path)
        for file in os.listdir(path):
            if file.lower().endswith(".pdf"):
                filepath = os.path.join(path, file)
                texts.append(self.read_data(filepath))
        return texts
    
    def chunk_text(self, text):
        chunks = []
        separators = ["\n\n", "\n", " ", ""]
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            if end >= len(text):
                chunks.append(text[start:])
                break
            # Find the separator closest to chunk_size, preferring higher-priority separators
            split_pos = None
            for sep in separators:
                if sep == "":
                    split_pos = end
                    break
                pos = text.rfind(sep, start, end)
                if pos > start:
                    split_pos = pos + len(sep)
                    break
            chunks.append(text[start:split_pos])
            # Move back by overlap, but not before the split point
            start = max(split_pos - self.overlap, start + 1)
        return chunks

    def clean_chunks(self, chunks):
        # Filter out duplicates:
        # Chunks are considered duplicates even if there is whitespace or lower/upper case difference
        seen = set()
        deduped = []
        for c in chunks:
            key = c.strip().lower()
            if len(key) < 100:
                continue
            if key not in seen:
                seen.add(key)
                deduped.append(c)
        return deduped

    def process_folder(self, path):
        texts = self.read_folder(path)
        chunks = []
        for text in texts:
            chunks.extend(self.chunk_text(text))
        return self.clean_chunks(chunks)
