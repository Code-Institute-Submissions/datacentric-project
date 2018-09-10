# Data-centric milestone project

### Purpose

This is a data-driven web application which enables users to browse, list and advertise items of clothing online.
Users must be registered and logged into their own personal account in order to list items, and update and remove listings.

Users can browse items on site using one of two search functions. 'Search by gender' categorises items by gender, whereas
'search by brand' allows users to search for items by entering keywords into a search bar.

### Functionality/technologies used

This application was written in Python using the Flask Framework. It also incorporates HTML and some custom Javascript logic.
Some CSS elements were lifted from MaterialiseCSS, although many aspects have been customised, and feature within a custom CSS file.
The application also incorporates some JQuery logic taken from MaterialiseCSS.

CRUD operations are carried out via HTML forms on site, which are used to enter into and update data stored within a database created
using SQLAlchemy and PostgreSQL. The application makes use of SQLAlchemy's object-relational mapper (ORM) through a foreign key which 
groups items listed by the ID of the user who listed them. This ensures that, while anybody can browse items on site, only users can 
edit and remove listings.

### Testing

Add testing description here.

### Deployment

If deploying this app from github, follow the instructions below:

'git clone https://github.com/samalty/datacentric-project'

Once inside the directory, enter:

'sudo pip3 install -r requirements.txt'

Make sure that the workspace that you are working in is running Python3, or else certain elements of functionality won't work.
Finally, before running the app.py file, ensure that the PostgreSQL server is up and running by entering:

'sudo service postgresql start'