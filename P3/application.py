# -*- coding: utf-8 -*-
from flask import Flask, flash, render_template, request, session, redirect, \
                    url_for, jsonify, Response
from database_setup import Base, Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import bleach

from xml.etree.ElementTree  import Element, SubElement, Comment, tostring

app = Flask(__name__)
#from app import views

# Set session secret key
app.secret_key = 'app_secret_key'


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
    except Exception as e:
        flash('Unable to retrieve item information.', 'warning')
        return redirect(url_for('index'))

    return render_template('view_item.html',
                           item=item)
    # return 'This will display item %s ' % (item_id)

# Add an item
@app.route('/item/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item = process_post(request.form)
        session.add(item)

        try:
            session.commit()
            flash('Item added.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            session.rollback()
            # print(e)
            categories = session.query(Category).all()
            return render_template('add_item.html',
                           categories=categories)


    else:
        categories = session.query(Category).all()
        return render_template('add_item.html',
                           categories=categories)


# Edit contents of specific item
@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    # item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        post_data = process_post(request.form)
        item.title = post_data.title
        item.description = post_data.description
        item.category_id = post_data.category_id
        try:
            session.commit()
            flash('Item edited successfully.', 'success')
            return redirect(url_for('list_category_items', category_id=item.category_id))
        except Exception as e:
            session.rollback()
            flash('Unable to save data', 'alert')
            return redirect(url_for('edit_item', item_id=item.id))
    else:
        try:
            item = session.query(Item).filter_by(id=item_id).one()
            categories = session.query(Category).all()
        except Exception as e:
            flash('Unable to retrieve item information.', 'warning')
            return redirect(url_for('index'))

        return render_template('edit_item.html', item=item, categories=categories,
                           action=url_for('edit_item', item_id=item.id))


# Delete specific item
@app.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
def delete_item(item_id):

    if request.method == 'POST':

        item = session.query(Item).filter_by(id=item_id).one()
        session.delete(item)

        # print('Item category id')
        # print(item.category.id)
        try:
            session.commit()
            flash('Item deleted.', 'success')
            return redirect(url_for('list_category_items', category_id=item.category_id))
        except Exception as e:
            flash('Unable to delete item', 'alert')
        return redirect(url_for('delete_item', item_id=item.id))
    else:
        try:
            item = session.query(Item).filter_by(id=item_id).one()
        except Exception as e:
            flash('Unable to retrieve item information', 'warning')
            return redirect(url_for('view_item', item_id=item.id))

        return render_template('delete_item.html', item=item)


### ##############################
### API functions
### ##############################
@app.route('/category/all/json', methods=['GET'])
def api_categories():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/category/<int:category_id>/json', methods=['GET'])
def api_category_items(category_id):
    items = session.query(Item).filter_by(category_id=category_id).order_by(Item.id.desc())
    return jsonify(items=[i.serialize for i in items])


@app.route('/category/all/xml', methods=['GET'])
def api_categories_xml():

    categories = session.query(Category).all()

    root = Element('categories')

    comment = Comment('List of categories')
    root.append(comment)

    for category in categories:
        cat_root = SubElement(root, 'category')
        category_id = SubElement(cat_root, 'id')
        category_id.text = str(category.id)
        category_name = SubElement(cat_root, 'name')
        category_name.text = category.name

    return Response(tostring(root), mimetype='application/xml')


### ##############################
### Auth functions
### ##############################

### ##############################
### Helper functions
### ##############################
def process_post(post):
    '''

    Args:
        post: the request.form posted data

    Returns:
        an object of class Item


    '''
    post = dict(post)
    print(post)
    title = bleach.clean(post['title'][0])
    description = bleach.clean(post['description'][0])
    # print(post['category'][0])
    category_id = int(bleach.clean(post['category'][0]))
    # print(post['title'])
    # print(title)
    item = Item(title=title,
                description=description,
                category_id=category_id)

    return item

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
            item = Item(title=i['title'], description=i['description'], category_id=i['category_id'])
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
