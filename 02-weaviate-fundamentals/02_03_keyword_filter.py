import utils
from weaviate.classes.query import Filter

client = utils.connect_to_my_db()

movies = client.collections.get("Movie")

# Define the filter - look for the word "forget" in the description
# "forget" -> exact match
# "forget*" -> forget, forgetful (wildcard)
# only * wildcard, no regex
filter = Filter.by_property("description").like("forget*")

response = movies.query.fetch_objects(
    filters=filter,
    limit=3
)

for o in response.objects:
    print(o.properties["title"])                # Show which titles were found
    print(o.properties["description"], "\n")    # Show the description


client.close()
