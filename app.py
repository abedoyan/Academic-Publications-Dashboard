import dash
from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import base64
import io
import mysql_utils
import mongodb_utils
import neo4j_utils


# won't change
app = Dash(__name__)


# layout
app.layout = html.Div([
    html.H1(['Academic Research Repository'],
            style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '50px'}),

    # Top level summary results
    html.Div([
        # Year input and button
        html.Div([
            dcc.Input(id='year_input', type='number', placeholder='Enter a year',
                      style={'border': '2px solid purple', 'width': '80%'}),
            html.Button('Search', id='year_search_button', n_clicks=0,
                        style={'border': '2px solid purple', 'background-color': 'purple', 'color': 'white', 'width': '20%'}),
        ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '33.3%', 'margin-right': '10px', 'margin-left': '10px'}),

        # University input and button
        html.Div([
            dcc.Input(id='uni_input', type='text', placeholder='Enter a university',
                      style={'border': '2px solid purple', 'width': '80%'}),
            html.Button('Search', id='uni_search_button', n_clicks=0,
                        style={'border': '2px solid purple', 'background-color': 'purple', 'color': 'white', 'width': '20%'}),
        ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '33.3%', 'margin-right': '10px', 'margin-left': '10px'}),

        # Author input and button
        html.Div([
            dcc.Input(id='author_input', type='text', placeholder='Enter an author',
                      style={'border': '2px solid purple', 'width': '80%'}),
            html.Button('Search', id='author_search_button', n_clicks=0,
                        style={'border': '2px solid purple', 'background-color': 'purple', 'color': 'white', 'width': '20%'}),
        ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '33.3%', 'margin-right': '10px', 'margin-left': '10px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px'}),

    # Year, University, and Author results
    html.Div([
        html.Div(id='year_results', style={'flex': '1', 'border': '2px solid purple', 'margin-right': '10px'}),
        html.Div(id='uni_results', style={'flex': '1', 'border': '2px solid purple', 'margin-right': '10px'}),
        html.Div(id='author_results', style={'flex': '1', 'border': '2px solid purple'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '50px'}),

    # Keyword input/results
    html.Div([
        html.H1('Top Publications and Authors by Keyword', style = {'display': 'flex', 'justify-content': 'center', 'font-size': '18px', 'color': 'rgb(255, 102, 0)'}),
        html.Div([
            dcc.Input(id='keyword_input', type='text', placeholder='Enter a keyword',
                    style={'border': '2px solid rgb(255, 102, 0)', 'width': '80%', 'margin-left': '500px'}),
            html.Button('Search', id='keyword_search_button', n_clicks=0,
                        style={'border': '2px solid rgb(255, 102, 0)', 'background-color': 'rgb(255, 102, 0)', 'color': 'white', 'width': '20%', 'margin-right': '500px'}),
        ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px'}),

        html.Div(id='keyword_results', style={'display': 'flex', 'flexDirection': 'row'}),
    ], style={'border': '2px solid rgb(255, 102, 0)', 'margin-bottom': '50px'}),

    # University popular keyword results
    html.Div([
        html.H1('Find Top Keywords by University', style = {'display': 'flex', 'justify-content': 'center', 'font-size': '18px', 'color': 'green'}),
        html.Div([
            dcc.Input(id='unikey_input', type='text', placeholder='Enter a university',
                    style={'border': '2px solid green', 'width': '80%', 'margin-left': '500px'}),
            html.Button('Search', id='unikey_search_button', n_clicks=0,
                        style={'border': '2px solid green', 'background-color': 'green', 'color': 'white', 'width': '20%', 'margin-right': '500px'}),
        ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px'}),

        html.Div(id='unikey_results', style={'display': 'flex', 'flexDirection': 'row'})
    ], style={'border': '2px solid green', 'margin-bottom': '50px'}),

    html.Div([
        # Delete publication results
        html.Div([
            html.H1('Delete a Publication', style = {'display': 'flex', 'justify-content': 'center', 'font-size': '18px', 'color': 'red'}),
            html.Div([
                dcc.Input(id='delete_input', type='text', placeholder='Enter a publication to delete',
                        style={'border': '2px solid red', 'width': '80%', 'margin-left': '100px'}),
                html.Button('Search', id='delete_search_button', n_clicks=0,
                            style={'border': '2px solid red', 'background-color': 'red', 'color': 'white', 'width': '20%', 'margin-right': '100px'}),
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-right': '10px', 'margin-left': '10px'}),
        
            html.Div([html.Div(id='delete_results', style={'flex': '1'}),], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px'}),
        ], style={'border': '2px solid red', 'width': '50%', 'margin-bottom': '50px', 'margin-right': '5px'}),

        # Add new author to existing publication
        html.Div([
            html.Div([
                html.H1('Add New Faculty to a Publication', style = {'display': 'flex', 'justify-content': 'center', 'font-size': '18px', 'color': 'blue'}),
                html.Div([
                    # Input field for publication title
                    html.Label('Enter Publication Title:', style = {'margin-right': '10px'}),
                    dcc.Input(id='pub_title_input', type='text', value=''),
                    html.Button('Check Publication', id='check_pub_button', n_clicks=0, style = {'border': '2px solid blue', 'background-color': 'blue', 'color': 'white'}),
                ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px'}),
                
                # Inputs for author and affiliation
                html.Div([
                    html.Div(id='author_info', style={'display': 'none'}, children=[
                        html.Label('Author Name:', style = {'margin-right': '10px'}),
                        dcc.Input(id='author_name_input', type='text', value='', style = {'margin-right': '10px', 'margin-bottom': '25px'}),

                        html.Label('University Affiliation:', style = {'margin-right': '10px'}),
                        dcc.Input(id='affiliation_input', type='text', value='', style = {'margin-bottom': '25px'}),

                        html.Button('Add Author', id='add_author_button', n_clicks=0, style = {'margin-bottom': '25px', 'border': '2px solid blue', 'background-color': 'blue', 'color': 'white'})
                    ]),
                ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px'})      
            ]),
            html.Div(id='add_author_output', style={'float': 'center'})
        ], style={'width': '50%', 'float': 'left', 'border': '2px solid blue', 'margin-bottom': '50px', 'margin-left': '5px'})
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '50px'})

])


# callback for MongoDB queries for publications by year
@app.callback(
    Output('year_results', 'children'),
    [Input('year_search_button', 'n_clicks')],
    [dash.dependencies.State('year_input', 'value')]
)

# MongoDB queries to get number of publications by year
def pubs_by_year(n_clicks, year):
    if n_clicks > 0 and year:
        pubs = mongodb_utils.pubs_year(year)
        if pubs is not None:
            children = [
                html.Div(f"{pubs:,}", style={'textAlign': 'center', 'font-size': '50px', 'font-weight': 'bold'}),
                html.Div(f"Publications in {year}", style={'textAlign': 'center', 'font-size': '18px', 'margin-bottom': '5px'})
            ]
            return children
        else:
            return "No results found. Try a different year!"
    else:
        pubs = mongodb_utils.total_pubs()
        children = [
            html.Div(f"{pubs:,}", style={'textAlign': 'center', 'font-size': '50px', 'font-weight': 'bold'}),
            html.Div(f"Publications in total", style={'textAlign': 'center', 'font-size': '18px', 'margin-bottom': '5px'})
            ]
        return children
    
# callback for MongoDB queries for publications by university
@app.callback(
    Output('uni_results', 'children'),
    [Input('uni_search_button', 'n_clicks')],
    [dash.dependencies.State('uni_input', 'value')]
)

# MongoDB queries to get number of publications by university
def pubs_by_uni(n_clicks, uni):
    if n_clicks > 0 and uni:
        pubs = mongodb_utils.pubs_uni(uni)
        if pubs is not None:
            children = [
                html.Div(f"{pubs:,}", style={'textAlign': 'center', 'font-size': '50px', 'font-weight': 'bold'}),
                html.Div(f"Publications at {uni}", style={'textAlign': 'center', 'font-size': '18px', 'margin-bottom': '5px'})
            ]
            return children
        else:
            return "No results found. Try a different university!"
    else:
        unis = mongodb_utils.total_uni()
        children = [
            html.Div(f"{unis:,}", style={'textAlign': 'center', 'font-size': '50px', 'font-weight': 'bold'}),
            html.Div(f"Universities in total", style={'textAlign': 'center', 'font-size': '18px', 'margin-bottom': '5px'})
            ]
        return children
    
# callback for MongoDB queries for publications by author
@app.callback(
    Output('author_results', 'children'),
    [Input('author_search_button', 'n_clicks')],
    [dash.dependencies.State('author_input', 'value')]
)

# MongoDB queries to get number of publications by author
def pubs_by_author(n_clicks, author):
    if n_clicks > 0 and author:
        pubs = mongodb_utils.pubs_author(author)
        if pubs is not None:
            children = [
                html.Div(f"{pubs:,}", style={'textAlign': 'center', 'font-size': '50px', 'font-weight': 'bold'}),
                html.Div(f"Publications by {author}", style={'textAlign': 'center', 'font-size': '18px', 'margin-bottom': '5px'})
            ]
            return children
        else:
            return "No results found. Try a different author!"
    else:
        authors = mongodb_utils.total_authors()
        children = [
            html.Div(f"{authors:,}", style={'textAlign': 'center', 'font-size': '50px', 'font-weight': 'bold'}),
            html.Div(f"Authors in total", style={'textAlign': 'center', 'font-size': '18px', 'margin-bottom': '5px'})
            ]
        return children

# callback for MySQL queries for keywords
@app.callback(
    Output('keyword_results', 'children'),
    [Input('keyword_search_button', 'n_clicks')],
    [dash.dependencies.State('keyword_input', 'value')]
)

# MySQL queries to get top publications and authors by the entered keyword
def search_keywords(n_clicks, keyword):
    if n_clicks > 0 and keyword:
        authors = mysql_utils.authors_by_keyword(keyword)
        pubs = mysql_utils.pubs_by_keyword(keyword)

        if authors or pubs:
            children = []

            if pubs:
                df_pubs = pd.DataFrame(pubs, columns=['Publications', 'Keyword Score'])
                df_pubs = df_pubs[['Publications']]
                table = dash_table.DataTable(
                    id='table',
                    columns=[{'name': col, 'id': col} for col in df_pubs.columns],
                    data=df_pubs.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'center',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'font_size': '14px',
                        'border': '1px solid rgb(255, 204, 153)'
                    },
                    style_header={'backgroundColor': 'rgb(255, 204, 153)', 'fontWeight': 'bold'}
                )
                children.append(html.Div(table, style={'flex': '1', 'border': '2px solid rgb(255, 102, 0)'}))

            if authors:
                df_authors = pd.DataFrame(authors, columns=['Author', 'Relevance Score'])
                bar = dcc.Graph(figure=px.bar(df_authors, x='Author', y='Relevance Score', color_discrete_sequence=['rgb(255, 102, 0)']).update_layout(plot_bgcolor='rgba(0, 0, 0, 0)'))
                children.append(html.Div(bar, style={'flex': '1', 'border': '2px solid rgb(255, 102, 0)'}))

            return children
        
        else:
            return html.Div("No results found. Try a different keyword!", style={'font-size': '18px', 'font-weight': 'bold', 'color': 'rgb(255, 102, 0)', 'margin-top': '5px', 'margin-bottom': '5px'})
    else:
        return ""

# callback for Neo4j query to get most popular keywords by university
@app.callback(
    Output('unikey_results', 'children'),
    [Input('unikey_search_button', 'n_clicks')],
    [dash.dependencies.State('unikey_input', 'value')]
)

# Neo4j query to get popular keywords by university
def add(n_clicks, university):
    if n_clicks > 0 and university:
        df = neo4j_utils.uni_keyword_score(university)

        if not df.empty:
            keyword_scores = dict(zip(df['keyword'], df['keyword_score']))
            wordcloud = WordCloud(width = 800, height = 300, background_color = 'white').generate_from_frequencies(keyword_scores)
            img_data = io.BytesIO()
            wordcloud.to_image().save(img_data, format='PNG')
            img_base64 = base64.b64encode(img_data.getvalue()).decode()
            children = html.Img(src='data:image/png;base64,{}'.format(img_base64), style={'width': '100%', 'height': 'auto'})
            return children

        else:
            children = html.Div(f"No results found. Try a different university!", style={'textAlign': 'center', 'font-size': '18px', 'font-weight': 'bold', 'color': 'green', 'margin-top': '5px', 'margin-bottom': '5px'})
            return children
    else:
        return ""

# callback for MongoDB query to delete publication
@app.callback(
    Output('delete_results', 'children'),
    [Input('delete_search_button', 'n_clicks')],
    [dash.dependencies.State('delete_input', 'value')]
)

# MongoDB query to delete a publication
def delete(n_clicks, pub_name):
    if n_clicks > 0 and pub_name:
        pub_details = mongodb_utils.get_pub_details(pub_name)
        children = []

        if pub_details:
            children = [
                html.Div(f"Publication Details:", style={'textAlign': 'center', 'font-size': '18px', 'font-weight': 'bold', 'margin-top': '10px', 'margin-bottom': '10px'}),
                html.Div(f"ID: {pub_details['id']}", style={'textAlign': 'center', 'font-size': '16px', 'margin-bottom': '5px'}),
                html.Div(f"Title: {pub_name}", style={'textAlign': 'center', 'font-size': '16px', 'margin-bottom': '5px'}),
                html.Div(f"Venue: {pub_details['venue']}", style={'textAlign': 'center', 'font-size': '16px', 'margin-bottom': '5px'}),
                html.Div(f"Year: {pub_details['year']}", style={'textAlign': 'center', 'font-size': '16px', 'margin-bottom': '15px'}),
            ]

        result = mongodb_utils.delete_pub(pub_name)
        if result == 1:
            children.append(html.Div(f"Publication deleted successfully!", style={'textAlign': 'center', 'font-size': '18px', 'font-weight': 'bold', 'color': 'red', 'margin-top': '10px', 'margin-bottom': '5px'}))
            return children
        else:
            children.append(html.Div(f"Publication not found.", style={'textAlign': 'center', 'font-size': '18px', 'font-weight': 'bold', 'color': 'red', 'margin-top': '10px', 'margin-bottom': '5px'}))
            return children
    else:
        return ""

# Callback to show/hide author info container based on pub title input (Neo4j)
@app.callback(
    Output('author_info', 'style'),
    [Input('check_pub_button', 'n_clicks')],
    [dash.dependencies.State('pub_title_input', 'value')]
)

# After new faculty is entered, show their info (Neo4j)
def show_author_info(n_clicks, pub_title):
    if n_clicks > 0 and pub_title:
        # Check if the publication exists
        result = neo4j_utils.check_publication_exists(pub_title)
        if result:
            return {'display': 'block'}
    return {'display': 'none'}

# Callback to add author to the database (Neo4j)
@app.callback(
    Output('add_author_output', 'children'),
    [Input('add_author_button', 'n_clicks')],
    [dash.dependencies.State('pub_title_input', 'value'),
     dash.dependencies.State('author_name_input', 'value'),
     dash.dependencies.State('affiliation_input', 'value')]
)

# Add author to the database (Neo4j)
def add_new_author(n_clicks, pub_title, author_name, affiliation):
    if n_clicks > 0:
        neo4j_utils.add_author(pub_title, {'name': author_name, 'affiliation': affiliation})
        author = neo4j_utils.get_author(author_name)
    
        df_auth = pd.DataFrame(author, columns={'name': 'Name', 'email': 'Email', 'phone': 'Phone', 'position': 'Position', 'university': 'University'})
        df_auth = df_auth.T.reset_index()
        df_auth.columns = ['Attribute', 'Value']

        table = dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in df_auth.columns],
            data=df_auth.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'center',
                'whiteSpace': 'normal',
                'height': 'auto',
                'font_size': '14px',
                'border': '1px solid blue'
            },
            style_header={'backgroundColor': 'rgb(173, 216, 230)', 'fontWeight': 'bold'}
        )
        result = html.Div(table, style={'flex': '1'})
        return result
    
    return ""


# won't change 
if __name__ == '__main__':
    app.run(debug=True)
