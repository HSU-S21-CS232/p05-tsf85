from flask import Flask, jsonify, request, session, render_template
import database
import os
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "suiper secret key"
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

def return_as_json(associative_array):
    json_data = [dict(ix) for ix in associative_array]
    return jsonify(json_data)

#base route (home page)
@app.route('/')
def home():
    return '<h1>Hello, World!</h1>'

@app.route('/about')
def about():
    return '<h1>About Me</h1><p>My name is Adam and I\'m an assistant professor at HSU</p>'

@app.route('/tracks')
def get_all_tracks():
    result = database.run_query("SELECT * FROM tracks")
    return return_as_json(result)

@app.route('/tracks/html')
def get_all_tracks_html():
    result = database.run_query("SELECT * FROM tracks")
    return render_template("all_tracks.html", data=result)

@app.route('/tracks/byName/<search_string>')
def search_tracks_name(search_string):
    sql = "SELECT * FROM tracks WHERE instr(GenreId, ?)>0"
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

#Looks up the ID number for a genre to enter into the next function
@app.route('/idLookUp/byGenre/<search_string>')
def search_tracks_genre(search_string):
    sql = "SELECT * FROM genres WHERE instr(Name, ?)>0"
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

#Enter genreID to search by previously found genreId
@app.route('/tracks/byGenreId/<search_string>')
def search_tracks_genre_id(search_string):
    sql = "SELECT * FROM tracks WHERE instr(GenreId, ?)>0"
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

@app.route('/tracks/byArtist/<search_string>')
def search_tracks_artist(search_string):
    sql = "SELECT * FROM tracks WHERE instr(Composer, ?)>0"
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

#searches for an album Id
@app.route('/idLookUp/album/<search_string>')
def search_album_id(search_string):
    sql = "SELECT * FROM albums WHERE instr(Title, ?)>0"
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

#searches tracks by an album id - make search specific
@app.route('/tracks/byAlbumId/<search_string>')
def search_tracks_album(search_string):
    sql = "SELECT * FROM tracks WHERE instr(AlbumId, ?)>0"
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['logged_in'] = False

    #request.method determines route type
    if request.method == 'POST':
        
        #request.values contains a dictionary of variables sent to the server
        if request.values['user_name'] == 'user' and request.values['password'] == 'password':

            #remember log in state through session
            session['logged_in'] = True
            return jsonify({'logged_in': session['logged_in'] })

        else:
            session['logged_in'] = False
            return jsonify({'logged_in': session['logged_in']})
    else:
        return jsonify({'logged_in': session['logged_in']})

@app.route('/customer', methods=['POST'])
def create_customer():
    sql = """INSERT INTO customers (
                          FirstName,
                          LastName,
                          Company,
                          Address,
                          City,
                          State,
                          Country,
                          PostalCode,
                          Phone,
                          Fax,
                          Email,
                          SupportRepId
                      )
                      VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)"""
    params = (request.values['FirstName'], 
              request.values['LastName'], 
              request.values['Company'], 
              request.values['Address'],
              request.values['City'],
              request.values['State'],
              request.values['Country'],
              request.values['PostalCode'],
              request.values['Phone'],
              request.values['Fax'],
              request.values['Email']
              )
    id = database.run_insert(sql, params)
    return jsonify({'id': id }) 