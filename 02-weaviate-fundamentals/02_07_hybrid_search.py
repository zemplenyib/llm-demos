import utils
import weaviate.classes as wvc

client = utils.connect_to_my_db()

movies = client.collections.get("Movie")

response = movies.query.hybrid(  # Hybrid search
    query="stellar",
    limit=3,
    # Fetch the score and explain_score
    return_metadata=wvc.query.MetadataQuery(score=True, explain_score=True),
)

for o in response.objects:
    print(o.properties["title"])                        # Show which titles were found
    print(f"score: {o.metadata.score:.3f}")             # What was the score
    print(f"explain_score: {o.metadata.explain_score}") # Explain the score
    print()

# alpha = 0.0 -> keyword search (bm25)
# alpha = 1.0 -> vector search
alpha = 0.7
response = movies.query.hybrid(
    query="stellar",
    limit=3,
    alpha=alpha,
    return_metadata=wvc.query.MetadataQuery(score=True, explain_score=True),
)

print(f"===== Results with alpha: {alpha} =====")
for o in response.objects:
    print(o.properties["title"])  # Show which titles were found
    print(f"score: {o.metadata.score:.3f}")  # What was the distance?
    print(f"explain_score: {o.metadata.explain_score}\n")  # What was the distance?


client.close()
