class Retriever:
    def __init__(self, documents):
        self.documents = documents

    def search(self, query: str):
        if not self.documents:
            return ""

        # Placeholder: return the first document's content for now
        return self.documents[0]["content"]
