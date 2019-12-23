from flask import render_template, url_for, flash, redirect, request, Response
from worldlibrary import app, db, bcrypt
from worldlibrary.forms import RegistrationForm, LoginForm, RentForm
from worldlibrary.models import User, Library, Rent, Search
from flask_login import login_user, current_user, logout_user, login_required
from flask.json import jsonify
import requests, re, datetime
from sqlalchemy import update
from datetime import date

def getBookInfo(num_book, books):
    i = 0
    book_list = []
    for data in books:
        i = i + 1
        if (i > num_book):
            break

        try:
            title = data['title_suggest']
        except:
            num_book = num_book + 1
            continue
        
        try:
            author = data['author_name'][0]
        except:
            num_book = num_book + 1
            continue

        try:
            public_year = data['publish_year'][0]
        except:
            num_book = num_book + 1
            continue

        try:
            if (data['cover_i'] == "undefined"):
                num_book = num_book + 1
                continue
            else:
                img = 'http://covers.openlibrary.org/b/id/' + str(data['cover_i']) + '-M.jpg'
        except:
            num_book = num_book + 1
            continue

        try:
            contributor = ' -- '.join(data['contributor'][:3])
        except:
            num_book = num_book + 1
            continue

        try:
            subject = ' -- '.join(data['subject'][:5])
        except:
            num_book = num_book + 1
            continue

        try:
            public_place = ' -- '.join(data['publish_place'][:3])
        except:
            num_book = num_book + 1
            continue

        try:
            publisher = ' -- '.join(data['publisher'][:5])
        except:
            num_book = num_book + 1
            continue

        try:
            isbn = ' -- '.join(data['isbn'][:5])
        except:
            num_book = num_book + 1
            continue

        book_list.append({'title': title, 'author': author, 'public_year' : public_year, 'img' : img, 'contributor': contributor, 'subject': subject, 'public_place': public_place, 'publisher': publisher, 'isbn': isbn})
    return book_list

@app.route("/")
@app.route("/home")
def home():
    all_book_list = []
    query_home = (db.session.execute('SELECT * FROM Library ORDER BY Library.id DESC LIMIT 16')).fetchall()
    query_home = query_home[::-1]
    query = (db.session.execute('SELECT * FROM Library')).fetchall()
    for row in query_home:
        all_book_list.append({'title': row.title, 'author': row.author, 'public_year' : row.public_year, 'img' : row.img})

    date = datetime.datetime.today()
    current_date = str(date.strftime("%d-%B-%Y"))
    return render_template('home.html', book_list=all_book_list, date=current_date)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/rent-info", methods=['GET', 'POST'])
@login_required
def show_rental():
    # TODO: Query Rent DB and Library DB based on the user info
    q = (db.session.query(User, Rent, Library)
        .join(Rent)
        .join(Library)
        .order_by(Rent.id)
        ).all()
    
    # create dictionary list for the user rent list
    user_rent_list = []
    for info in q:
        #check if current user and book availability
        if (info.User.id == current_user.id) and (info.Library.availability == False)\
            and (info.Rent.return_time == None):
            dict={}
            dict['title'] = info.Library.title
            dict['author'] = info.Library.author
            dict['public_year'] = info.Library.public_year
            dict['img'] = info.Library.img
            dict['start_time'] = info.Rent.start_time
            dict['end_time'] = info.Rent.end_time
            dict['return_time'] = info.Rent.return_time
            dict['cost'] = info.Rent.cost
            dict['overdue_rate'] = info.Rent.overdue_rate
            user_rent_list = [dict]+ user_rent_list  #add new rent book the the begining of the list
        
    # create dictionary list for the user return list
    user_return_list= []
    for info in q:
        #check if current user and book availability
        if (info.User.id == current_user.id)\
            and (info.Rent.return_time != None):
            dict={}
            dict['title'] = info.Library.title
            dict['author'] = info.Library.author
            dict['public_year'] = info.Library.public_year
            dict['img'] = info.Library.img
            dict['start_time'] = info.Rent.start_time
            dict['end_time'] = info.Rent.end_time
            dict['return_time'] = info.Rent.return_time
            dict['cost'] = info.Rent.cost
            if ((info.Rent.return_time-info.Rent.end_time).days > 0): #if do not return the book on time
                dict['overdue_cost'] = info.Rent.overdue_rate*(info.Rent.return_time-info.Rent.end_time).days
            else: 
                dict['overdue_cost']= 0 #return book before or on due date
            user_return_list = [dict]+ user_return_list #add new return book the the begining of the list
    return render_template('rent_detail.html', title='Rented Book', user_rent_list = user_rent_list, user_return_list = user_return_list)

@app.route("/rent-book/<title>", methods=['GET', 'POST'])
@login_required
def rent_book(title):
    books = db.session.execute('select * from Library where title = :title',
                             {'title': title})
    book_chosen = books.fetchall()
    if book_chosen[0][4] == False:
        flash('The book is not available to rent now!', 'danger')
        return redirect(url_for('home'))
    form = RentForm()
    if form.validate_on_submit():
        flash('You have rent the book successfully!', 'success')
        # Upadate Library table - avaialability is False now 
        stmt= db.session.query(Library).filter_by(id=book_chosen[0][0]).update({"availability": False})  #Update availability successfully :)
        db.session.commit()
        
        # Update rent DB table 
        user_id = current_user.id  
        book_id = book_chosen[0][0]
        format_str = '%Y-%m-%d' #using to convert to date time
        start_time_str= request.form['startDate'] #load from form
        end_time_str= request.form['endDate']  #load from form
        start_time = datetime.datetime.strptime(start_time_str, format_str).date()  #convert to date time
        end_time = datetime.datetime.strptime(end_time_str, format_str).date()  #convert to date time
        cost = (end_time - start_time).days * 0.5 #calculate from start and end time then conver to int
        rent_record = Rent(user_id = user_id, book_id = book_id, start_time = start_time, end_time = end_time\
           ,cost = cost)
        if rent_record:
            db.session.add(rent_record)
            db.session.commit()
        return redirect(url_for('show_rental'))
    return render_template('rent_book.html', form=form, book_title = title, title='Rent Book')
    
@app.route('/search', methods=['GET', 'POST'])
def GetApiData():
    inputValue = ''
    if request.method == 'POST':
        result = request.form.to_dict()
        inputValue = result['inputValue']
    inputValue= inputValue.strip().replace(" ", '+')
    r = requests.get('http://openlibrary.org/search.json?q=' + inputValue)
    books = r.json()['docs']
    book_list = getBookInfo(16, books)
    if not book_list:
        flash('No Books Have Found With The Current Search Input. Sorry!', 'danger')
        return redirect(url_for('home'))
    else:
        for book in book_list:
            book_search = Search(title = book['title'] , author= book['author'] , public_year = book['public_year'], img = book['img'])
            db.session.add(book_search)
            db.session.commit()

            query_library= (db.session.execute('SELECT * FROM Library WHERE Library.title = :cur_title', {'cur_title': book['title']})).fetchall()
            if not query_library:
                book_library = Library(title = book['title'] , author= book['author'] , public_year = book['public_year'], img = book['img'], contributor = book['contributor'], subject= book['subject'], public_place = book['public_place'], publisher = book['publisher'], isbn = book['isbn'])
                db.session.add(book_library)
                db.session.commit()
        return redirect(url_for('search_result'))

@app.route('/search-result')
def search_result():
    book_list = []
    query_search = (db.session.execute('SELECT * FROM Search')).fetchall()
    for row in query_search:
        book_list.append({'title': row.title, 'author': row.author, 'public_year' : row.public_year, 'img' : row.img})
    
    # Delete all rows of Search DB ready for the next search
    db.session.query(Search).delete()
    db.session.commit()
    return render_template('search_result.html', book_list= book_list, title="Search Result")

@app.route('/display/<title>', methods=['GET','POST'])
def display(title):
    click_book = (db.session.execute('SELECT * FROM Library WHERE Library.title = :cur_title', {'cur_title': title})).fetchall()
    return render_template('display.html', click_book = click_book, title='Display Detail')   

@app.route('/returnBook/<title>', methods=['GET','POST'])
def returnBook(title):
    stmt= db.session.query(Library).filter_by(title= title).update({"availability": True})  #Update availability successfully :)
    #query join 3 table in database 
    q = (db.session.query(User, Rent, Library)
        .join(Rent)
        .join(Library)
        .order_by(Rent.id)
        ).filter(User.id == current_user.id).filter(Library.title == title).all()
    current_rent_id = q[-1].Rent.id
   #Update rerurn date for the book that user return
    stmt = db.session.query(Rent).filter_by(id= current_rent_id).update({"return_time": date.today()})
    db.session.commit()
    FlashStr =  "You return the book "+ str(title)+ ' successflly! Thank you for using our service! Hope you come back'
    flash(FlashStr , 'success')
    return redirect(url_for('show_rental'))

