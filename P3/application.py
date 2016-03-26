# -*- coding: utf-8 -*-
from flask import Flask, flash, render_template, request, session, redirect, \
                    session, url_for, jsonify, Response
from flask.ext.github import GitHub
from database_setup import Base, User, Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import json
import bleach

from xml.etree.ElementTree  import Element, SubElement, Comment, tostring

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = '506e2fc17c83f1054317'
app.config['GITHUB_CLIENT_SECRET'] = 'd00c874aff85087d5528cedb6b2ca86736eb67dd'
github = GitHub(app)


# Set session secret key
app.secret_key = 'app_secret_key'


engine = create_engine('postgresql+psycopg2://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


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


# Show all items of a specific category
@app.route('/category/<int:category_id>/', methods=['GET'])
def list_category_items(category_id):
    categories, items = all_query()
    page = {'h5_title': 'Category items'}
    try:
        items = db_session.query(Item).filter_by(category_id=category_id).all()
    except Exception as e:
        flash(str(e), 'warning')
        return redirect(url_for('index'))
    return render_template('index.html',
                           categories=categories,
                           items=items,
                           page=page)

# Show contents of specific item
@app.route('/item/<int:item_id>', methods=['GET'])

# Show contents of specific item
@app.route('/item/<int:item_id>')
def view_item(item_id):
    try:
        item = db_session.query(Item).filter_by(id=item_id).one()
    except Exception as e:
        flash('Unable to retrieve item information.', 'warning')
        return redirect(url_for('index'))

    return render_template('view_item.html',
                           item=item,
                           can_edit=owner)


# Add an item
@app.route('/item/add', methods=['GET', 'POST'])
def add_item():
    if not authenticated():
        return redirect(url_for('login'))

    if request.method == 'POST':
        item = process_post(request.form)
        db_session.add(item)

        try:
            db_session.commit()
            flash('Item added.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db_session.rollback()
            categories = db_session.query(Category).all()
            return render_template('add_item.html',
                           categories=categories)

    else:
        categories = db_session.query(Category).all()
        return render_template('add_item.html',
                            categories=categories)


# Edit contents of specific item
@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):

    # Load the item object, handle exception if none
    try:
        item = db_session.query(Item).filter_by(id=item_id).one()
    except NoResultFound, e:
        flash(str(e), 'warning')
        return redirect(url_for('index'))

    # Make sure the user is logged in and allowed to edit
    if not authenticated():
        return redirect(url_for('login'))
    if not owner(item):
        return redirect(url_for('view_item', item_id=item.id))

    # All OK, Proceed
    if request.method == 'POST':
        post_data = process_post(request.form)
        item.title = post_data.title
        item.description = post_data.description
        item.category_id = post_data.category_id
        try:
            db_session.commit()
            flash('Item edited successfully.', 'success')
            return redirect(url_for('list_category_items', category_id=item.category_id))
        except Exception as e:
            db_session.rollback()
            flash('Unable to save data', 'alert')
            return redirect(url_for('edit_item', item_id=item.id))
    else:
        try:
            # item = db_session.query(Item).filter_by(id=item_id).one()
            categories = db_session.query(Category).all()
        except Exception as e:
            flash('Unable to retrieve item information.', 'warning')
            return redirect(url_for('index'))

        return render_template('edit_item.html', item=item, categories=categories,
                           action=url_for('edit_item', item_id=item.id),
                           can_edit=owner)


# Delete specific item
@app.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
def delete_item(item_id):
    # Load the item object, handle exception if none
    try:
        item = db_session.query(Item).filter_by(id=item_id).one()
    except NoResultFound, e:
        flash(str(e), 'warning')
        return redirect(url_for('index'))

    # Make sure the user is logged in and allowed to edit
    if not authenticated():
        return redirect(url_for('login'))
    if not owner(item):
        return redirect(url_for('view_item', item_id=item.id))

    if request.method == 'POST':
        # item = db_session.query(Item).filter_by(id=item_id).one()
        db_session.delete(item)

        # print('Item category id')
        # print(item.category.id)
        try:
            db_session.commit()
            flash('Item deleted.', 'success')
            return redirect(url_for('list_category_items', category_id=item.category_id))
        except Exception as e:
            flash('Unable to delete item', 'alert')
        return redirect(url_for('delete_item', item_id=item.id))
    else:
        try:
            item = db_session.query(Item).filter_by(id=item_id).one()
        except Exception as e:
            flash('Unable to retrieve item information', 'warning')
            return redirect(url_for('view_item', item_id=item.id))

        return render_template('delete_item.html', item=item, can_edit=owner)


# ############################################
# Authentication & authorization functions
# ############################################

# Login
@app.route('/login', methods=['GET'])
def login():
    return github.authorize()


# Callback function
@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash('Authorization failed.', 'alert')
        return redirect(next_url)

    user = db_session.query(User).filter_by(access_token=oauth_token).first()
    if user is None:
        user = User(oauth_token)
        db_session.add(user)

    user.access_token = oauth_token
    db_session.commit()

    # Store current user details in a session
    session['usr_id'] = user.id
    session['usr_token'] = user.access_token

    flash('Logged in', 'success')
    return redirect(url_for('index'))


@app.route('/logout', methods=['GET'])
def logout():
    # session.
    session.pop('usr_id', None)
    session.pop('usr_token', None)
    flash('Logged out', 'success')
    return redirect(url_for('index'))


# ################################
# API functions
# ################################

# Get all categories in JSON format
@app.route('/category/all/json', methods=['GET'])
def api_categories():
    categories = db_session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# Get items of specific category in JSON format
@app.route('/category/<int:category_id>/json', methods=['GET'])
def api_category_items(category_id):
    items = db_session.query(Item).filter_by(category_id=category_id).order_by(Item.id.desc())
    return jsonify(items=[i.serialize for i in items])


# Get all categories in XML format
@app.route('/category/all/xml', methods=['GET'])
def api_categories_xml():

    categories = db_session.query(Category).all()

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


# ################################
# Helper functions
# ################################

def authenticated():
    """
    Returns: True if user is authenticated, False otherwise

    """

    if 'usr_id' not in session:
        return False
    else:
        return True


def owner(item):
    """

    Args:
        item: The current item

    Returns: True if authenticated user is the owner of the item,
        false otherwise

    """
    # if authenticated():
    if item.usr_id is None:
        return False
    else:
        return 'usr_id' in session and item.usr_id == session['usr_id']

    return False


def process_post(post):
    """

    Args:
        post: the request.form posted data

    Returns:
        an object of class Item


    """
    post = dict(post)
    print(post)
    title = bleach.clean(post['title'][0])
    description = bleach.clean(post['description'][0])
    # print(post['category'][0])
    category_id = int(bleach.clean(post['category'][0]))

    item = Item(title=title,
                description=description,
                category_id=category_id,
                usr_id=session['usr_id'])

    return item


def populate_database():
    # Alter json file to add a root user with ID=1 and reference that user in
    # default items
    """
    Add some initial data in an empty database from a json file
    """
    res = db_session.query(Category).all()
    # If some data already present, do nothing
    if len(res) > 0:
        return

    with open('data.json', 'rb') as datafile:
        data = json.load(datafile)

        usr_data = data['usr']
        for u in usr_data:
            usr = User(id=u['id'], access_token='System_install')
            db_session.add(usr)

        category_data = data['category']
        for c in category_data:
            category = Category(id=c['id'], name=c['name'])
            db_session.add(category)

        item_date = data['item']
        for i in item_date:
            item = Item(title=i['title'], description=i['description'], category_id=i['category_id'])
            db_session.add(item)

        try:
            db_session.commit()
            # print('Database populated')
        except Exception as e:
            print('Exception while populating database')
            db_session.rollback()


def all_query():
    categories = db_session.query(Category).all()
    # To list the latest X items, order by item_id in descending order
    # quick and dirty, but does the job.
    # An ideal approach would be to use a date/time column in the DB
    # and order by that column
    items = db_session.query(Item).order_by(Item.id.desc()).limit(10)
    return categories, items

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
