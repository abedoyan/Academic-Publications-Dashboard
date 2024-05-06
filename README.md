# Academic World Dashboard

##### Arda Bedoyan

**Title:** Academic Research Repository

**Purpose:** The purpose of this project was to create a user-friendly dashboard to explore various publications and data related to different research papers from an academic world dataset. The academic world dataset, which was used as the basis for all three databases used in the backend, MySQL, MongoDB, and Neo4j, includes a great amount of information about faculty members at various academic institutions and the publications that are relevant to them. One of the most valuable scenarios for using such a dataset is for research purposes. Therefore, I designed my dashboard with students and researchers as the target users. The objectives of the tool will be to help find important papers, authors, and keywords that are all relevant to what a user might be searching for when doing research for their own academic or professional purposes. 

**Demo:** https://mediaspace.illinois.edu/media/t/1_zb4wy0c0

**Installation:** Installation involved first uploading the given Academic World dataset into the three databases used in the backend application, namely MySQL, MongoDB, and Neo4j. No modifications were made to the dataset before storing the dataset into the databases and therefore, project testers will not need to make any updates on their end before being able to test the application. To start the application, simply run the app.py file and follow the http link.

**Usage:** Usage of the dashboard is meant to be simple and intuitive. Each widget prompts the user to enter an input, which is then used to output some information related to the publications in the dataset.

*Widget 1-3:* Enter either a year, university name, or author’s name to see the corresponding number of publications in that year, at the university, or by the author, respectively.

*Widget 4-5:* These two widgets are triggered by the same user input. A user is prompted to enter a keyword of interest. Then widget 4 will give the top 15 publications relevant to that keyword and widget 5 will provide a bar chart of the top 10 authors whose publications are relevant to that keyword.

*Widget 6:* Enter the name of a university found in the dataset to see a word cloud of the top keywords from that institution.

*Widget 7:* Enter the title of a publication that you want deleted from the database. If successfully deleted, the widget will print out the details of that publication, otherwise it will say that the publication was not found.

*Widget 8:* A user is first prompted to enter the title of a publication that they want to add a new author to. If the publication exists, then the user can enter the new faculty member’s name and affiliated university to add to the database.

**Design:** The dashboard is structured in a way that is easy to understand and navigate. When the webpage initially loads, there are three widget at the top that are meant to provide a high level summary of the publications in the dataset. These widgets connect to the MongoDB database. The following two widget connect to the MySQL database and run off of the same keyword input. Oftentimes, when users are searching through a database for publications, they want to enter a keyword and find the relevant articles and authors for that keyword. The next section is meant to be a visual representation of the most significant keywords coming from a university. This widget connects to the Neo4j database and is useful to help guide a researcher who might be interested in knowing what keywords are most relevant to a certain institution. The following bottom section of the dashboard is where the backend updates happen. These last two widgets ask for a publication title, and one widget deletes that publication through a connection to MongoDB, whereas the other adds a new author to that publication through a Neo4j connection. The dashboard is designed in a way that will have the most useful widgets towards the top. The widgets that update the backed databases will likely be used less, and therefore, they are at the bottom of the webpage.

**Implementation:** The final program is comprised of four main files, app.py, mysql_utils.py, mongodb_utils.py, and neo4j_utils.py. The app.py file imports the Dash Plotly library, the utils files, and other necessary libraries, to run the front-end portion of the website. The three utils.py files each connect to the backend databases in the three different databases and contain the functions that will be used in the app.py file to pull the relevant data and visualize them in the dashboard.

*mysql_utils.py:*  This file imports mysql.connector and forms a connection to the MySQL relational database that houses the academic world dataset. Users will have to update the host, username, and password. If no connection is successfully made, then an error message will be printed out. The file includes two functions to run SQL queries that feed into the dashboard. One function is meant to find the top authors for an inputted keyword. The relevance score for an author to a keyword is determined by how many citations they have and the score of the keyword as related to their work. The other function will fetch the top publications based on the score of the keyword in that publication.

*mongodb_utils.py:* This file imports MongoClient and CollectionInvalid from pymongo and forms a connection to the MongoDB document database which also houses the academic world database. There are multiple functions defined to get the number of publications by year, university, and author. Additionally, the widgets for these functions initially display information even before a user has entered any input. Therefore, there are functions to display the total number of publications, universities, and authors in the database. There is also a function to delete a publication. Finally, there is a function to get the details of a publication based on the entered title, such as id, year, venue, and number of citations.

*neo4j_utils.py:* This file imports GraphDatabase from the neo4j library and pandas, and first forms a connection to the Neo4j database. The user will need to update the URI, username, and password to their information and open the database using the Neo4j Desktop application in order to establish a connection. This file has a function to find the top keywords based on an entered university. It finds the keywords that faculty at the university are interested in and sums the keyword scores. The output is used to create a word cloud of the top keywords. The remaining functions are meant to be used in the widget that adds a new faculty member as an author to a publication. First, one function checks that an entered publication exists in the database and then another adds the author to the database. The final function gets the author’s details and prints them out to screen in the dashboard.

*app.py:* This is the main file that creates the layout of the dashboard and imports all the utility files to run the widgets based on the different databases and their created functions. I imported Dash, html, dcc, dash_table, callback, Output, and Input from dash. The layout section is found near the top of the file and below it are the callbacks and functions for each widget organized in order of how they appear on the dashboard and in the layout section for easy navigating.

**Database Techniques:** The application uses three database techniques, indexing, constraints, and views. Indexes were used in the MySQL database to improve the performance of the MySQL queries. I created indexes for the columns that my queries referred to the most, such as faculty name, publication title, and keyword name. I ran the create index statements directly from the terminal, as opposed to through my python file. 

![image](https://github.com/CS411DSO-SP24/ArdaBedoyan/assets/111945641/9d8aaa36-f188-48f6-b788-01b8d9774e06)

In Neo4j, I implemented constraints to ensure certain properties of some of my nodes in the graph database. The last widget in the dashboard allows a user to add a new author to a publication. To ensure that the new authors being added to the dataset were unique, I created a constraint that the faculty name must be unique. I also created another constraint the name of the affiliated university entered must be a string. These constraints were created in Neo4j desktop.

![image](https://github.com/CS411DSO-SP24/ArdaBedoyan/assets/111945641/78758640-0db8-4269-ba2d-131075daa272)

The final database technique I implemented was a view in my MongoDB database. I created a function directly in the mongodb_utils.py file using the create_collection() function to create a view called “pubs_year_view” of the number of publications by year. This view was used in the pubs_year() function to return the number of publications based on a year that the dashboard user entered.

**Extra-Credit Capabilities:** Not applicable to this project.

**Contributions:** As this was a solo project, I worked on the full end-to-end application development on my own. Below is a breakdown of tasks done and time spent per task.

| Task	| Time Spent |
| ---- | ------- |
| Refamiliarizing myself with the Academic World dataset | 30 minutes |
| Deciding on the objectives of the application and what widgets to include | 30 minutes |
| Reading through documentation and learning to program with Dash	| 2 hours |
| Creating a basic app.py file | 1 hour |
| Creating mysql_utils.py file, connecting to MySQL, and adding MySQL widgets to app.py | 5 hours |
| Creating mongodb_utils.py file, connecting to MongoDB, and adding MongoDB widgets to app.py | 8 hours |
| Creating neo4j_utils.py file, connecting to Neo4j, and adding Neo4j widgets to app.py | 10 hours |
| Deciding on and adding database techniques | 2 hours |
| Fixing the layout of the dashboard | 5 hours |
| Writing the supporting documentation/README | 2 hours |
| Creating the demo video | 2 hours |