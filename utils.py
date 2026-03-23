import weaviate
from weaviate.client import WeaviateClient
import os
from dotenv import load_dotenv
import time

# Load environment variables
# From the provided `.env` file
load_dotenv()


class BatchImporter:
    def __init__(self, rpm=100):
        # Requests per minute
        self.rpm = 100
        self.inserted_buffer = 0
    
    def insert_in_batch(self, collection, objs):
        i = 0
        while i < len(objs):
            batch_size = min(self.rpm - self.inserted_buffer, len(objs[i:]))
            batch = objs[i:i+batch_size]
            response = collection.data.insert_many(batch)

            print(f"Insertion complete with {len(response.uuids)} objects for '{collection.name}' collection.")
            if len(response.errors) > 0:
                print(f"Insertion errors: {response.errors}.")

            # Increase inserted buffer by the inserted size
            self.inserted_buffer += batch_size
            if (self.inserted_buffer >= self.rpm):
                print("Sleeping for 60s.")
                time.sleep(60)
                self.inserted_buffer = 0                

            i += batch_size


def connect_to_my_db() -> WeaviateClient:
    """
    Helper function to connect to your own Weaviate Cloud instance
    configured with Gemini (text2vec-google) as the vectorizer.
    Used as a Gemini-based alternative to the demo database.
    """
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("MY_WEAVIATE_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("MY_WEAVIATE_KEY")),

        # Gemini API key for vectorization and generative queries
        headers={"X-Goog-Studio-Api-Key": os.getenv("GEMINI_APIKEY")},
    )
    return client


def connect_to_my_second_db() -> WeaviateClient:
    """
    Helper function to connect to your own Weaviate instance.
    To be used for data loading as well as queries.
    """

    client = weaviate.connect_to_weaviate_cloud(
        # Weaviate URL
        cluster_url=os.getenv("MY_SECOND_WEAVIATE_URL"),

        # Weaviate API Key
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("MY_SECOND_WEAVIATE_KEY")),

        # Gemini API key for queries that require it
        headers={"X-Goog-Studio-Api-Key": os.getenv("GEMINI_APIKEY")},
    )

    # # Or use a local instance - e.g. with Docker
    # client = weaviate.connect_to_local(
    #     headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")}
    # )

    return client


def main():

    # Connect to Weaviate
    client = connect_to_my_db()
    # client = connect_to_my_second_db()

    try:
        # Check whether the client is ready
        assert client.is_ready()  # Check connection status (i.e. is the Weaviate server ready)
        print("Success! You appear to be correctly set up.")
    finally:
        # Close the connection
        client.close()


if __name__ == "__main__":
    main()
