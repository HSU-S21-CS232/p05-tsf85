from flask import Flask, jsonify, request, session, render_template, abort
import database
import os
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "super secret key"
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
    sql = "SELECT * FROM tracks WHERE instr(Name, ?)>0"
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

#still not sure I understand all the pieces of this, but it seems to effectively search the genreIds by name and then
#search through the tracks with an exact genreId search.
@app.route('/tracks/byGenre/<search_string>')
def search_tracks_genre(search_string):
    sql = """SELECT tracks.Name, * 
             FROM tracks 
             INNER JOIN genres 
             ON tracks.GenreId = genres.GenreId 
             WHERE INSTR(genres.Name, ?)>0"""
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

#Just used composer for a loose artist search
@app.route('/tracks/byArtist/<search_string>')
def search_tracks_artist(search_string):
    sql = "SELECT * FROM tracks WHERE instr(Composer, ?)>0"
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

#searches for an album name for an albumId and runs that into tracks
@app.route('/tracks/byAlbum/<search_string>')
def search_tracks_album(search_string):
    sql = """SELECT * 
             FROM tracks 
             INNER JOIN albums 
             ON tracks.albumId = albums.albumId 
             WHERE INSTR(albums.Title, ?)>0"""
    params = (search_string, )
    result = database.run_query(sql, params)
    return return_as_json(result)

# adds item to cart folder... wish I'd have found LIMIT earlier for searching.
@app.route('/cart/add/<search_string>', methods=['POST'])
def add_to_cart(search_string):
    sql = """INSERT INTO cart 
             SELECT Name, TrackId, UnitPrice
             From tracks
             WHERE INSTR(TrackId, ?)>0
             LIMIT 1
          """
    params = (search_string, )
    id = database.run_insert(sql, params)
    return jsonify({'id': id }) 

#removes item from card using TrackId
@app.route('/cart/remove/<search_string>', methods=['DELETE'])
def remove_from_cart(search_string):
    sql = """DELETE FROM cart
             WHERE TrackId = ?
          """
    params = (search_string, )
    id = database.run_delete(sql, params)
    return jsonify({'id': id }) 

#clears the cart
@app.route('/cart/clear', methods=['DELETE'])
def clear_cart():
    sql = "DELETE FROM cart"

    id = database.run_clear(sql)
    return jsonify({'id': id })

#checkout. Enter customer ID number, checks if logged in, fill out fields and returns invoices
@app.route('/cart/checkout/<search_string>', methods=['GET', 'POST']) 
def checkout(search_string):
    # if session['logged_in'] == False:
    #     abort(777, description="Not logged in.")
    
    total = database.run_query("""SELECT 
                                    SUM(UnitPrice)
                                  FROM 
                                    cart
                                  LIMIT 1""")
    sql = """INSERT INTO invoices (
                        CustomerId,
                        InvoiceDate,
                        BillingAddress,
                        BillingCity,
                        BillingState,
                        BillingCountry,
                        BillingPostalCode,
                        Total)
                        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)"""
    params = (request.values['CustomerId'], 
              request.values['InvoiceDate'], 
              request.values['BillingAddress'], 
              request.values['BillingCity'],
              request.values['BillingState'],
              request.values['BillingCountry'],
              request.values['BillingPostalCode'],
              total)
              
    database.run_insert(sql, params)

    sql2 = "SELECT * FROM invoices WHERE CustomerId = ?"
    params2 = (search_string, )
    result = database.run_query(sql2, params2)
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