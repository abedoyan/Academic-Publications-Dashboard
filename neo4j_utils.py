from neo4j import GraphDatabase
import pandas as pd

# Neo4j Connection Class
class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self._driver = GraphDatabase.driver(uri, auth=(user, pwd))

    def close(self):
        self._driver.close()

    def run_query(self, query, db=None):
        assert self._driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self._driver.session(
                database=db) if db is not None else self._driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


# Initialize URI, username, and password
connection = Neo4jConnection(uri="bolt://localhost:7687",
                       user="neo4j", pwd="a6B16c95")


# query to get the most popular keywords by # sum of keyword score
def uni_keyword_score(university):
    query = f"""
            MATCH (uni:INSTITUTE) <- [:AFFILIATION_WITH] - (f:FACULTY) - [i:INTERESTED_IN] -> (k:KEYWORD)
            WHERE uni.name = "{university}"
            RETURN k.name as keyword, SUM(i.score) AS keyword_score
            ORDER BY keyword_score DESC
            LIMIT 10
            """
    result = connection.run_query(query, db='academicworld')
    df = pd.DataFrame([dict(_) for _ in result])
    return df


# query to add an author based on chosen publication
def add_author(pub_title, new_author):
    query = f"""
            MATCH (pub:PUBLICATION {{title: "{pub_title}"}})
            MERGE (f:FACULTY {{name: "{new_author['name']}"}})
            MERGE (uni:INSTITUTE {{name: "{new_author['affiliation']}"}})
            MERGE (pub) <- [:PUBLISH] - (f) - [:AFFILIATION_WITH] -> (uni)
            """
    result = connection.run_query(query, db='academicworld')
    df = pd.DataFrame([dict(_) for _ in result])
    return df


# query to get faculty info
def get_author(faculty_name):
    query = f"""
            MATCH (f:FACULTY {{name: "{faculty_name}"}})
            OPTIONAL MATCH (f) - [:AFFILIATION_WITH] -> (uni:INSTITUTE)
            RETURN f.name AS name, f.email AS email, f.phone AS phone, f.position as position, uni.name AS university
            """
    result = connection.run_query(query, db='academicworld')
    df = pd.DataFrame([dict(_) for _ in result])
    return df


def check_publication_exists(pub_title):
    query = f"""
            MATCH (pub:PUBLICATION {{title: "{pub_title}"}})
            RETURN COUNT(pub) AS count
            """
    result = connection.run_query(query, db='academicworld')
    count = result[0]['count']
    return count > 0