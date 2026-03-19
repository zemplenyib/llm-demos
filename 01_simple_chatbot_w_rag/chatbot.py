from sentence_transformers import SentenceTransformer
from ollama import chat
from ollama import ChatResponse
import chromadb
from keybert import KeyBERT

class ChatBot:
    def __init__(self, model_name, path, HyDE, query_expansion, keyword_extraction):
        self._model_name = model_name
        self._model = None
        self._collection = None
        self._db_path = path
        self._HyDE = HyDE
        self._query_expansion = query_expansion
        self._keyword_extraction = keyword_extraction

    def load_model(self):
        # Load the model from Hugging Face
        self._model = SentenceTransformer(self._model_name)

    def setup_db(self):
        # Setup the vector database
        self._chroma_client = chromadb.PersistentClient(path=self._db_path)
        self._collection = self._chroma_client.get_or_create_collection(name=f"my_knowledge_base_{self._model_name}")
    
    def add_data(self, chunks):
        if self._model is None:
            self.load_model()
        if self._collection is None:
            self.setup_db()
        # Embed chunks
        embeddings = self._model.encode(chunks, show_progress_bar=True)
        # Add data to database
        batch_size = 5000
        for i in range(0, len(chunks), batch_size):
            self._collection.upsert(
                ids=[f"chunk_{j}" for j in range(i, min(i+batch_size, len(chunks)))],
                embeddings=embeddings[i:i+batch_size].tolist(),
                documents=chunks[i:i+batch_size]
        )
    
    def extract_keywords(self, text):
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text)
        return keywords

    def query(self, text):
        if self._collection is None:
            self.setup_db()
        
        if self._collection.count() == 0:
            return "No context was provided."
        
        if self._model is None:
            self.load_model()

        if self._keyword_extraction:
            # Remove filler words
            keywords = self.extract_keywords(text)
            keywords_list = [k[0] for k in keywords]
            query_text = " ".join(keywords_list)

        if self._HyDE:
            # Apply HyDE (Hypotethical Document Embedding)
            prompt = (f"Write a one sentence answer to: {text}.")
            hypotethical_answer = chat(model="llama3", messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            query_text = hypotethical_answer.message.content
        
        if self._query_expansion:
            prompt = (
                f"Generate 10 related terms to: {text}."
                "Answer only with these words one by one.")
            expansion_answer = chat(model="llama3", messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            query_text = text + " " + expansion_answer.message.content
        
        # Query the database
        query_embedding = self._model.encode([query_text]).tolist()

        retrieved_chunks = self._collection.query(
            query_embeddings=query_embedding,
            n_results=5
        )
        
        context = "\n\n".join(retrieved_chunks["documents"][0])

        prompt = (
            f"Context: {context} \n"
            f"Question: {text} \n"
            "Answer based only on the context above"
        )

        # 6. Print the results
        response: ChatResponse = chat(model="llama3", messages=[
            {
                "role": "user",
                "content": prompt
            }
        ])

        return response.message.content