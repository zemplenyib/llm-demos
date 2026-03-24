import os
import utils
import weaviate.classes as wvc
from weaviate.util import generate_uuid5
import pandas as pd

client = utils.connect_to_my_db()
batch_importer = utils.BatchImporter()

movies = client.collections.get("Movie")
reviews = client.collections.get("Review")
synopses = client.collections.get("Synopsis")

movie_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data/movies_data.csv"))

# Import reviews
review_objs = list()
for i, row in movie_df.iterrows():
    for c in [1, 2, 3]:  # There are three reviews per movie in this dataset
        col_name = f"Critic Review {c}"
        if len(row[col_name]) > 0:
            props = {
                "body": row[col_name],
            }
            review_uuid = generate_uuid5(row[col_name])
            data_obj = wvc.data.DataObject(properties=props, uuid=review_uuid)
            review_objs.append(data_obj)

batch_importer.insert_data_in_batch(reviews, review_objs)

# Import movies
movie_objs = list()
for i, row in movie_df.iterrows():
    props = {
        "title": row["Movie Title"],
        "description": row["Description"],
        "rating": row["Star Rating"],
        "director": row["Director"],
        "movie_id": row["ID"],
        "year": row["Year"],
    }
    # Add references to reviews
    review_uuids = list()
    for c in [1, 2, 3]:
        col_name = f"Critic Review {c}"
        if len(row[col_name]) > 0:
            review_uuid = generate_uuid5(row[col_name])  # Identify the review IDs to refer to
            review_uuids.append(review_uuid)  # Collect the review IDs

    movie_uuid = generate_uuid5(row["ID"])
    data_obj = wvc.data.DataObject(
        properties=props,
        uuid=movie_uuid,
        references={"hasReview": review_uuids},
    )
    movie_objs.append(data_obj)

batch_importer.insert_data_in_batch(movies, movie_objs)

# Import synopses
synopses_objs = list()
for i, row in movie_df.iterrows():
    props = {
        "body": row["Synopsis"]
    }
    synopsis_uuid = generate_uuid5(row["ID"]) # this is okay as the synopsis and movie are in different collections
    # Create a reference to the movie in the "forMovie" property
    synopsis_obj = wvc.data.DataObject(
        properties=props,
        uuid=synopsis_uuid,
        references={"forMovie": synopsis_uuid}
    )

    synopses_objs.append(synopsis_obj)

batch_importer.insert_data_in_batch(synopses, synopses_objs)

# Add references from movies to synopses
synopsis_refs = list()
for i, row in movie_df.iterrows():
    movie_uuid = generate_uuid5(row["ID"])

    # Create a reference object with the "hasSynopsis" property
    synopsis_ref = wvc.data.DataReference(
        from_property="hasSynopsis",
        from_uuid=movie_uuid,
        to_uuid=movie_uuid
    )

# Add the references to the collection
# Hint: use the "movies.data.reference_add_many" method
batch_importer.insert_ref_in_batch(movies, synopsis_refs)
# for i in range(0, len(synopsis_refs), BATCH_SIZE):
#     batch = synopsis_refs[i:i+BATCH_SIZE]
#     response = movies.data.reference_add_many(batch)
# 
#     print(f"Insertion complete with {len(response.uuids)} objects for 'synopsis' collection.")
#     print(f"Insertion errors: {len(response.errors)}.")
# 
#     if i + BATCH_SIZE < len(synopsis_refs):
#         time.sleep(60)

client.close()
