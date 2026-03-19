import weaviate
from weaviate.client import WeaviateClient
import os
from dotenv import load_dotenv

# Load environment variables
# From the provided `.env` file
load_dotenv()

  
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

        # Try a query
        movies = client.collections.get("Movie")
        response = movies.query.near_text(query="time travel", limit=1)
        assert len(response.objects) == 1
        print("Success! You appear to be correctly set up.")
    finally:
        # Close the connection
        client.close()


if __name__ == "__main__":
    main()
