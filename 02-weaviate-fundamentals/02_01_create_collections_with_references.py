import utils
import weaviate.classes as wvc

client = utils.connect_to_my_db()

# Delete any previously created collections with the same name
client.collections.delete("Movie")
client.collections.delete("Review")
client.collections.delete("Synopsis")

# Add reviews
reviews = client.collections.create(
    name="Review",

    # Set modules to be used
    # Set the vectorizer
    vector_config=wvc.config.Configure.Vectors.text2vec_google_gemini(),
    # Set the generative model
    generative_config=wvc.config.Configure.Generative.google_gemini(model="gemini-3.1-flash-lite-preview"),

    # Define the properties of the collection
    properties=[
        wvc.config.Property(
            name="body",  # Set the name of the property
            data_type=wvc.config.DataType.TEXT,  # Set the data type of the property
        ),
    ],
)
print("'Reviews' collection created.")

# Add movies
movies = client.collections.create(
    name="Movie",

    # Set modules to be used
    # Set the vectorizer
    vector_config=wvc.config.Configure.Vectors.text2vec_google_gemini(),
    # Set the generative model
    generative_config=wvc.config.Configure.Generative.google_gemini(model="gemini-3.1-flash-lite-preview"),

    # Define the properties of the collection
    properties=[
        wvc.config.Property(
            name="title",
            data_type=wvc.config.DataType.TEXT,
        ),
        wvc.config.Property(
            name="description",
            data_type=wvc.config.DataType.TEXT,
        ),
        wvc.config.Property(
            name="movie_id",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="year",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="rating",
            data_type=wvc.config.DataType.NUMBER,
        ),
        wvc.config.Property(
            name="director",
            data_type=wvc.config.DataType.TEXT,
            skip_vectorization=True,
        ),
    ],
    # Set reference properties
    references=[
        wvc.config.ReferenceProperty(
            name="hasReview",           # Set the name of the reference property
            target_collection="Review", # Set the name of the target collection
        )
    ],
)
print("'Movies' collection created.")

# Add synopses
synopses = client.collections.create(
    name="Synopsis",
    vector_config=wvc.config.Configure.Vectors.text2vec_google_gemini(),
    generative_config=wvc.config.Configure.Generative.google_gemini(model="gemini-3.1-flash-lite-preview"),
    properties=[
        wvc.config.Property(
            name="body",
            data_type=wvc.config.DataType.TEXT,
        ),
    ],
    # A reference property with name "forMovie". Points to the "Movie" collection
    references=[
        wvc.config.ReferenceProperty(
            name="forMovie",
            target_collection="Movie",
        )
    ],
)

# Add a reference property to the "Movie" collection with the name "hasSynopsis"
movies.config.add_reference(
    wvc.config.ReferenceProperty(
        name="hasSynopsis",
        target_collection="Synopsis"
    )
)
print("'Synopses' collection created.")

client.close()
