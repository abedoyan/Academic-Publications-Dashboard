from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

# Connect to MongoDB
def connect_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['academicworld']
    return db

# Create a view to get # of publications by year
def create_pubs_year_view():
    db = connect_mongodb()
    try:
        db.create_collection(
            "pubs_year_view",
            codec_options=None,
            viewOn="publications",
            pipeline=[
                {"$group": {"_id": "$year", "count": {"$sum": 1}}}
            ]
        )
        print("New Collection Created.")
    except CollectionInvalid:
        print("Collection 'pubs_year_view' already exists.")

# Get the topline summary of # of publications by year USING VIEW FROM ABOVE
def pubs_year(pub_year):
    db = connect_mongodb()
    view_result = db.pubs_year_view.find_one({"_id": pub_year})
    year_count = view_result.get("count", 0) if view_result else 0
    return year_count

# Total # of publications
def total_pubs():
    db = connect_mongodb()
    total = db.publications.count_documents({})
    return total

# Get the topline summary of # of publications by university
def pubs_uni(pub_uni):
    db = connect_mongodb()
    uni = db.faculty.count_documents({"affiliation.name": pub_uni})
    return uni

# Total # of universities
def total_uni():
    db = connect_mongodb()
    unique_uni = db.faculty.distinct("affiliation")
    total_uni = len(unique_uni)
    return total_uni

# Get the topline summary of # of publications by author
def pubs_author(pub_auth):
    db = connect_mongodb()
    author_cursor = db.faculty.find({"name": pub_auth})
    publications = []

    for author in author_cursor:
        publications.extend(author.get("publications", []))

    auth = len(publications)
    return auth

# Total # of authors
def total_authors():
    db = connect_mongodb()
    unique_auth = db.faculty.distinct("name")
    total_auth = len(unique_auth)
    return total_auth

# Delete a publication
def delete_pub(pub_name):
    db = connect_mongodb()
    result = db.publications.delete_one({"title": pub_name})
    return result.deleted_count

# Get publication details
def get_pub_details(pub_name):
    db = connect_mongodb()
    publication = db.publications.find_one({"title": pub_name})

    if publication:
        id = publication.get("id", "")
        venue = publication.get("venue", "")
        year = publication.get("year", "")
        numCitations = publication.get("numCitations", "")

        return {"id": id, "venue": venue, "year": year, "numCitations": numCitations}
    else:
        return None
    
# to run automatically when this file is imported into app.py
create_pubs_year_view()