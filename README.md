# Data-centric milestone project

This is a data-driven web application which provides users with a free resource whereby they can browse, list and advertise items of 
clothing online. Users must be registered and logged into their own personal account in order to list items, and update and remove 
listings. Users are also able to browse items on site using one of two search functions. 'Search by gender' categorises all items on 
site by gender, allowing the user to browse all available mens, womens and unisex items. 'Search by brand' incorporates a keyword 
search function, enabling users to find items by entering specific brand names into a search bar.

## UX

This application was developed with the needs of various types of users in mind, namely buyers and sellers of clothing items, looking
for an easy and free-to-use platform to do so. The site provides a simple way to browse items, and create, update and delete listings.

- As a retailer, I want to advertise my stock online, to heighten its exposure and increase my sales
- As a retailer, I want a quick and simple means of listing stock online, to increase efficiency
- As an individual seller, I want a straightforward and cost-effective means of selling my items, to maximise my profit
- As an individual buyer, I want a simple way of browsing for items, so that I can easily identify items that I like

Mockups created for this project can be found within the 'planning' folder.

## Features

The promary feature of this application is that it provides CRUD (Create, Read, Update, Delete) functionality to an SQL database 
via the browser. Users can:

- Create a secure user account, enabling them to list items online
- Search for items, either by entering keywords into a search bar, or by searching items categorised by gender
- List items by entering information into a form and uploading an image to be stored in the database displayed on site 
- Manage, update and delete listings within their own secure account page

Other features include:

- Secure, password-protected register and login function 
- Javascript-powered image carousel
- View listing page with lightbox feature to zoom in on images

## Technologies used

- **Python**: The underlying code, including views, models and routes, was written in Python.
- **Flask**: This application was written using the Flask framework, and incorporates various Flask extensions, including Msearch to support the search bar function, and Flask Login to support the login function.
- **HTML**: HTML was used to structure the website.
- **CSS**: CSS was used to enhance the appearance of the website. 
- **Javascript**: The image carousel was developed using custom Javascript logic.
- **SQL**: All data entered is stored in an SQL database. The application also makes use of SQLAlchemy's object-relational mapper (ORM) through a foreign key which groups items listed by the ID of 
the user who listed them.
- **MaterializeCSS**: The front-end framework was used to simplify the design process. Custom MaterializeCSS jQuery logic was also used for features such as tabs and accordions.

## Testing

Many of the key features of this project, including views and the application's login function, were subject to unit-testing. This is documented 
within the 'tests.py' file, which can be run within the terminal. At the top of the test page, there are instructions on how to run the file.

Additional code which has since been removed was also used to ensure that the database was being updated upon the submission of forms via 
the browser. For example, I would add a print statement to the edit listing function, so that the terminal would return the updated product 
details, confirming that the database was being updated as intended. Regularly accessing the SQL database via the bash terminal also helped 
me ensure that everything was working as planned.

Testing within the browser was conducted to ensure that error messages were being returned as required, and that visual features such as the 
image carousel and lightbox were fully functional. Examining the image carousel via the developers tools console within the browser also 
helped confirm that the Javascript code was working as intended.

This project was developed using a mobile-first approach. A Google Chrome screen resolution tester was used throughout development to ensure 
that pages and functionalities were easy to navigate and use via different platforms and screen sizes. The app was tested across a range of 
browsers on both Windows and Mac operating systems, including Chrome, IE, Firefox, Microsoft Edge, and Opera, using CrossBrowserTesting.com's 
free service.

## Deployment

The final project was pushed to Github, before being deployed to Heroku by way of connecting to the Github workspace. A Heroku Postgres database 
was included as an add-on when setting up the app in Heroku. Heroku came with its own database URL within config variables, which I used to replace 
the database config variables that I had used during development. 'gunicorn' was installed via the bash terminal to allow the project to connect 
to Heroku, and 'psycopg2' was installed to enable the project to interact with the SQL database. The requirements.txt file was duly updated. A 
Procfile was added to let Heroku know the type of app that it is hosting.

## Credits

### Content

- Some CSS elements were lifted from MaterialiseCSS, although the majority of these have been customised
- The application also incorporates some jQuery logic taken from MaterializeCSS which is acknowledged within the script

### Media

- The photos used on this site were obtained via a Google search for images labelled for noncommercial reuse