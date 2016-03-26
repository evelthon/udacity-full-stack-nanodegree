#!/usr/bin/env python

import os

print('Running application setup')
print('-------------------------')

# Drop existing database with given name
os.system('sudo -u postgres  -H -- dropdb catalog')
# Drop existing user with given name
os.system('sudo -u postgres  -H -- dropuser catalog')

# Create a user named 'catalog' with password 'catalog'
os.system('sudo -u postgres -H -- psql  -U postgres -c "create user catalog with password \'catalog\';"')

# Create a database named 'catalog', owned by user 'catalog'
os.system('sudo -u postgres -H -- psql  -U postgres -c "CREATE DATABASE catalog owner catalog;"')

# Create table category
os.system('sudo -u postgres -H -- psql  -U postgres -d catalog -c "'
          'CREATE TABLE category ('
          'id SERIAL PRIMARY KEY,'
          ' name TEXT );"')

# Create table item
os.system('sudo -u postgres -H -- psql  -U postgres -d catalog -c "'
          'CREATE TABLE item ('
          'id SERIAL PRIMARY KEY, '
          'title TEXT, '
          'description TEXT, '
          'category_id INTEGER REFERENCES category(id) );"')

# Set the owner of the above two tables to user 'catalog'
os.system('sudo -u postgres -H -- psql  -U postgres -d catalog -c '
          '"ALTER TABLE category OWNER TO catalog;"')
os.system('sudo -u postgres -H -- psql  -U postgres -d catalog -c '
          '"ALTER TABLE item OWNER TO catalog;"')



print('-------------------------')
print('Finished!')
