import utils

client = utils.connect_to_my_db()  # Connect to the demo database

movies = client.collections.get("Movie")

# Vector search + generate answer
# single_prompt: generate for each returned entry separately
response = movies.generate.near_text(
    query="science fiction",
    limit=3,
    single_prompt="""
    Summarize the description in 12 words exactly:
    {description} for this movie {title}.
    """
)

for o in response.objects:
    print(o.properties["title"])    # Show which titles were found
    print(o.generative.text)              # RAG output
    print()


# grouped_task: read all returned entries and generate one answer
response = movies.generate.near_text(
    query="science fiction",
    limit=10,
    grouped_task="""
    Are there any common themes in these movies?
    Explain 2 in very short points,  and list the relevant movies:
    """
)

print(response.generative.text)  # Print the generated text


client.close()
