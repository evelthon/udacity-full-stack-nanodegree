# Project 3 - Item Catalog
## About
This project is a web application that provides a list of sport items within
a variety of categories.
It implements oauth authentication through GitHub. Authenticated users have
the ability to modify their own items.
The interface is based on Zurb's foundation framework.

Supports API endpoints for JSON and XML.
## Usage
1. Fork the repository  so that you have your own version of the files
2. Change directory to vagrant/catalog
3. Install *GitHub-Flask* python module
4. Obtain a GitHub *Client ID* and a *Client Secret*. Edit *application.py*
and edit *app.config['GITHUB_CLIENT_ID']* and
*app.config['GITHUB_CLIENT_SECRET']* respectively
5. Execute *python setup.py* to setup database schema.
5. Execute *python application.py* to load the catalog application.
6. Open your web browser and visit *http://localhost:5000/*. On first run,
some default items are added to the database.

## Note
The default items added on first run are not editable cause of the item
ownership restrictions. In an ideal scenario, they would be editable by a
root/admin user.
