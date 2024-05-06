import mysql.connector

# Establish a connection to the MySQL database
def connect_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", #update to your own password
            database="academicworld"
        )
        #print("Database connection established successfully.")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None

# Query to find top authors based on keyword
def authors_by_keyword(keyword):
    connection = connect_mysql()
    cursor = connection.cursor()

    query = """
            SELECT a.name, sum(d.score * c.num_citations) as KRC
            FROM faculty a
            JOIN faculty_publication b ON a.id = b.faculty_id
            JOIN publication c ON b.publication_id = c.id
            JOIN publication_keyword d ON c.id = d.publication_id
            JOIN keyword e ON d.keyword_id = e.id
            WHERE e.name = %s
            GROUP BY a.name
            ORDER BY KRC DESC
            LIMIT 10;
            """

    cursor.execute(query, (keyword,))
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    return results

# Query to get top publications based on keyword
def pubs_by_keyword(keyword):
    connection = connect_mysql()
    cursor = connection.cursor()

    query = """
            SELECT DISTINCT a.title, b.score
            FROM publication a
            JOIN publication_keyword b ON a.id = b.publication_id
            JOIN keyword c ON b.keyword_id = c.id
            WHERE c.name = %s
            ORDER BY b.score DESC
            LIMIT 15;
            """

    cursor.execute(query, (keyword,))
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    return results
