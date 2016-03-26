# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session
from database_setup import Base, Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json


app = Flask(__name__)
#from app import views


engine = create_engine('postgresql+psycopg2://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
def index():
# Populate an empty database
    populate_database()
    categories, items = all_query()
    page = {'h5_title': 'Latest items'}
    return render_template('index.html',
                           categories=categories,
                           items=items,
                           page=page)

@app.route('/login')
def login():
    return 'Show login'

# Edit category
@app.route('/category/<int:category_id>/edit')
def edit_category(category_id):
    return 'This functions allows editing of category %s' % category_id


# Show all items of a specific category
@app.route('/category/<int:category_id>/')
def list_category_items(category_id):
    categories, items = all_query()
    page = {'h5_title': 'Category items'}
    try:
        items = session.query(Item).filter_by(category_id=category_id).all()
    except:
        print('Error in view_item')
    return render_template('index.html',
                           categories=categories,
                           items=items,
                           page=page)

# Show contents of specific item
@app.route('/item/<int:item_id>')
def view_item(item_id):
    try:
        item = session.query(Item).filter_by(id=item_id).one()
    except:
        print('Error in view_item')

    return render_template('view_item.html',
                           item=item)
    # return 'This will display item %s ' % (item_id)

# Add an item
@app.route('/item/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        test=1
    else:
        test=2

    categories = session.query(Category).all()
    return render_template('add_item.html',
                           categories=categories)


# Edit contents of specific item
@app.route('/item/<int:item_id>/edit')
def edit_item(category_id,item_id):
    return 'This will edit item %s in category %s' % (item_id, category_id)

# Delete specific item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def delete_item(category_id,item_id):
    return 'This will delete item %s in category %s' % (item_id, category_id)



def populate_database():
    '''
    Add some initial data in an empty database from a json file
    '''
    res = session.query(Category).all()
    # If some data already present, do nothing
    if (len(res)>0):
        return

    with open('data.json', 'rb') as datafile:
        data = json.load(datafile)

        category_data = data['category']
        for c in category_data:
            category = Category(id=c['id'], name=c['name'])
            session.add(category)

        item_date = data['item']
        for i in item_date:
            item = Item(id=i['id'], title=i['title'], description=i['description'], category_id=i['category_id'])
            session.add(item)

        try:
            session.commit()
            # print('Database populated')
        except Exception as e:
            print('Exception while populating database')
            session.rollback()

def all_query():
    categories = session.query(Category).all()
    # To list the latest X items, order by item_id in descening order
    # quick and dirty, but does the job.
    # An ideal approach would be to use a date/time column in the DB
    # and order by that column
    items = session.query(Item).order_by(Item.id.desc()).limit(10)
    return categories, items

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
