# Mineral Catalog 

## TreeHouse project 8

### Instructions:

Add features to a web application that catalogs minerals to build a fully-featured web site. Add the ability to search information and filter it to match user preferences.

### How to use:

You can run python manage.py populatedatabase after you call migrate (found in https://stackoverflow.com/questions/53579677/django-2-1-how-to-import-models-in-a-custom-py-file) to populate the database. It expects mineral.json in mineral_catalog/static/data 


### Comments

You can search by Letter. Group, Category, Streak and text search together.
This search for example shows only one viable mineral - Zircon: 
    Letter: Z
    Group: Silicates
    Category: Nesosilicates
    Streak: White

Going for the Exceeds Expectations grade

#### Project reject n.1

Migration error "django.db.utils.OperationalError: no such table: mineral_catalog_mineral"  

Problem: Tried to populate the options in form just once by calling query outside of form class. Migrate or populatedatabase caused the form to be imported and run query for table that didn't exist.  

Fix: For now the query is called in class init method
