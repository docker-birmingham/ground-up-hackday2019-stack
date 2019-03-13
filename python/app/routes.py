from json2table import convert
from flask import jsonify, redirect

from app import app
from app import database

table_attributes = {"style": "width:100%", "class": "table table-striped"}


@app.route('/')
@app.route('/index')
def index():
    return redirect("http://localhost:5000/view", code=302)


@app.route('/create')
def create():
    database.create_accounts()
    return redirect("http://localhost:5000/view", code=302)


@app.route('/view')
def view():
    accounts_dict = {x.id: x.balance for x in database.get_accounts()}

    return """
    <form style:"display:flex" method="get" action="/randomize">
        <button type="submit">Ranzomize</button>
    </form>
    
    <form style:"display:flex" method="get" action="/delete">
        <button type="submit">Delete</button>
    </form>
    
    <form style:"display:flex" method="get" action="/create">
        <button type="submit">Create</button>
    </form>
    """ \
           + convert(accounts_dict, table_attributes=table_attributes)


@app.route('/delete')
def delete_all():
    return """
        <form style:"display:flex" method="get" action="/randomize">
            <button type="submit">Ranzomize</button>
        </form>

        <form style:"display:flex" method="get" action="/delete">
            <button type="submit">Delete</button>
        </form>

        <form style:"display:flex" method="get" action="/create">
            <button type="submit">Create</button>
        </form>
        """ \
           + "Accounts Deleted: " + database.delete_all().__str__()


@app.route('/randomize')
def randomize():
    if len(database.get_accounts()) < 1:
        return redirect("http://localhost:5000/view", code=302)

    for i in range(0, 10):
        database.randomize_accounts()
    return redirect("http://localhost:5000/view", code=302)
