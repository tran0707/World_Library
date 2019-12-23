1. Project Type: Plan A
2. Group Members Name: Khoa Tran (tran0707) && Thao Nguyen (nguy3524)
3. Link to live Application: https://world-library-web.herokuapp.com/
4. Link to Github Code Repository: https://github.umn.edu/tran0707/World_Library
5. List of Technologies/API's Used: 
    API Link1 : http://openlibrary.org/search.json?q=the+lord+of+the+rings
    API Link2 : http://openlibrary.org/search.json?subject=love
    Technologies Used:  
        + Bootstrap
        + Flask-SqlAchemy
        + Jinja2
        + Flask-Bcrypt
        + Flask-Login
        + Flask-WTF
        + requests
        + JQuery
        + Proper.js

6. Detailed Description of the project (No more than 500 words)
    Our project is called World Library (a book rental application). The user can look for books by author,
    subject, or name. If the book is not found, the app will notify 
    there is no book available. If a book is found the user can look at more detail of the book and 
    rent it if no body rent it yet. To rent a book, the user is required to log in. There will be a form allowing the 
    user to fill in the renting date range.The user can see the list of the current rented book and the returned book 
    in rent detail with detail such as start date, end date, cost...

    We use an API that has a big data set of book information. We will assume the library has all the
    books available in API. However, there is just one copy of specific book available in the library. For example, there 
    is only one copy of book with title "White Fang". If someone rent it, noone else can). 
    For the database, For User table, we start adding record when user create an account. 
    Initial library table, we will have 16 books record at the beginning for display purpose. If the user searches for a book,
    the result will be added into library table (if the book is not in the library yet) with defaul availability True.
     If the user rent a book the availability of the book in lirary table will be update to false. A record of book id,
    user id, start date, end date, cost will be added into Rent table too. If the user return the book, the availability
    in library table wil be updated to True and the return date in Rent table of that record will updated with current return date.
    
7. List of Controllers and their short description (No more than 50 words for each controller)
    + @app.route("/")
        Query 16 books in library table for display purpose.

    + @app.route("/about")
        Return about.html page.

    + @app.route("register")
        Check if the form is validate on submit and add infomation to user table.

    + @app.route("/login")
        It allows a user to login in if they already have an account and manage their books rented.

    + @app.route("/logout")
        It allows a user to logout. This button only shows when a user already login.

    + @app.route("/account")
        It shows the current user account with user name, email, user_id, and a default image.

    + @app.route("/rent-info")
        This route allows user to view what book they currently rented and already returned. It works 
        by querying that joining all Library, User, and Rent database together and add the items in 2 
        lists user_rent_list, user_return_list base on different conditions.
       Then it will pass them to the rent_detail.html using render_template function.

    + @app.route("/rent-book/<title>")
        This route start when the user click the Borrow button. It checks if user is login and the book still 
        available to rent. The user will fill the form to rent the book. Then it will get the book id that user 
        chose to rent and update the availability of book in Lirabry DB to false. Lastly,
        user_id, book_id, start_time, end_time, and cost will be added into the Rent DB and it redirect to rent_detail.

    + @app.route("/search")
        It allows user to search for book using title, subject, author, or any information related to that book.
        It starts with collect the input from user and use an requests function in python to get data from API
        for that specific input. It will check if book is already added in Library DB or not. If not, those books
        will be added in Library DB and Search DB. At the end, it redirects to route "/search_result" to display result.

    + @app.route("/search-result")
        It works by query all books from Search DB. Right after query, it will save the result into a dictionary and 
        drop all rows of Search DB for the next search. The saved dictionary will use to display in search_result.html.

    + @app.route("/display/<title>")
        It works by query book detail when user click on the Detail button underneat of each book. The result is displayed
        in display.html. This route is used to display the detail of books. 

    + @app.route("/returnBook/<title>")
        When the user returnt the book, it will update the availability in Library DB back to True. 
        It also updates the return_time in Rent DB to the current date. At the end, it redirects back to the show rental 
        route "/rent-info".

8. List of Views and their short description (No more than 50 words for each view)
    + about.html
    This is a about page that shows the developer name and github link to the code of the project.
    It also includes a short description of what this website can do.

    + account.html
        Display the current user information

    + display.html
        Display the Book detail afer user click on the Detail button underneat of each book.

    + home.html
        This is homepage which display always display 16 books that users can see detail or borrow.
        
    + logout.html
        A template layout for all the html files. It contains a header, body, and footer. A body has {%block content%}
        that allows the other viewers to extend from this file.

    + login.html
        A login form that allow user to login. It has email, password, remember, and submit field allows user to enter
        their information into the web page.

    + register.html
        A register form has username, email, password, confirm_password, and submit
        field. 

    + rent_book.html
        A form that allows user to enter the start date and end date of each rent.

    + rent_detail.html
        Display both rented list and returned list. Return button allow user to return a book. The Borrow Again button 
        allow user to borrow the book that they return before.

    + search_result.html
        It displays the result of searching based on the user input into Search Result page. 

9. List of Tables, their Structure and short description
    Total 4 Tables is used in this project. They are User, Library, Rent, and Search. 
    User uses to save data related to a user who use the library. It has 5 columns including id,
        username, email, image_file, and password. User table has id as a primary_key.

    Library uses to save Library book database. When a user search for a book, the system then check
        if thoes books is already in the Libray or not. If not, we will add it to the Library database.
        Library has 11 columns including id, title, author, public_year, availability, img, contributor,
        subject, public_place, publisher, and isbn. In this table, id is the primary_key.

    Rent uses to keep track of what books of each user  and each book rented. It has 8 columns including
        id, user_id, book_id, start_time, end_time, return_time, cost, and overdue_rate. Id is the primary_key,
        user_id is the foreign key back to the id of User table, and book_id is the foreign key back to id of
        Library table.
        
    Search uses to keep track of what the output of user search are and saves it into this database. The system
        then query that back to the correct route and display it. When the display complete, the Search database
        get erased and ready for the next search. Search table has 6 columns including id, title, author,
        public_year, availability, and img.

    Table structure:
    ----------------
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
        password = db.Column(db.String(60), nullable=False)

    class Library(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(500), nullable=False)
        author = db.Column(db.String(100), nullable=False)
        public_year = db.Column(db.Integer, nullable=False)
        availability = db.Column(db.Boolean, nullable=False, default=True)
        img = db.Column(db.String(500), nullable=False)
        contributor = db.Column(db.String(500), nullable=False)
        subject = db.Column(db.String(500), nullable=False, default="Not Available")
        public_place = db.Column(db.String(500), nullable=False, default="Not Available")
        publisher = db.Column(db.String(500), nullable=False)
        isbn = db.Column(db.Integer, nullable=False)

    class Rent(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        book_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)
        start_time = db.Column(db.Date, nullable=False, default=datetime.date(datetime.now()))
        end_time = db.Column(db.Date, nullable=False, default=datetime.date(datetime.now()))
        return_time = db.Column(db.Date, nullable=True)
        cost = db.Column(db.Float, nullable=False)
        overdue_rate = db.Column(db.Float, nullable=False, default=5.0)

    class Search(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(500), nullable=False)
        author = db.Column(db.String(100), nullable=False)
        public_year = db.Column(db.Integer, nullable=False)
        availability = db.Column(db.Boolean, nullable=False, default=True)
        img = db.Column(db.String(500), nullable=False)

10. References/Resources: List all the references, resources or the online templates that were used for the project.
    + Bootstrap: https://getbootstrap.com/docs/4.4/getting-started/introduction/
    + SqlAchemy: https://docs.sqlalchemy.org/en/13/orm/tutorial.html
    + Class Code: https://github.umn.edu/mill0242/CS4131Fall2019/tree/master/09_countries
