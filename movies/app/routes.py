from flask import *
from app import app, db
from app.models import Entry,EntrySearilzer,User


jedi = "of the jedi"

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username = form.get('username')
        password = form.get('password')
        user_data = User.query.filter_by(username='admin').first()
        if user_data.password == password:
            session['user'] = username
            return redirect('/index')
    session['user'] = None
    return render_template('login.html')

@app.route('/index')
def index():
    if session['user'] != None:
        entries = Entry.query.all()
        entries_serializer = EntrySearilzer(many=True)
        entries_data = entries_serializer.dump(entries)
        # return json.jsonify(json_list = entries_data)
        data =  jsonify(json_list =entries_data )
        return render_template('index.html', entries=entries,entries_data=data)
    else:
        return redirect('/')


@app.route('/add', methods=['POST'])
def add():
    if session['user'] != None:
        if request.method == 'POST':
            form = request.form
            title = form.get('title')
            description = form.get('description')
            if not title or description:
                entry = Entry(title = title, description = description)
                db.session.add(entry)
                db.session.commit()
                return redirect('/index')
    else:
        return redirect('/')

@app.route('/update/<int:id>', methods=['GET','POST'])
def updateRoute(id):
    if session['user'] != None:
        if request.method == "POST":
            form = request.form
            title = form.get('title')
            description = form.get('description')
            data = Entry.query.get(id)
            data.title = title
            data.description = description
            db.session.commit()
            return redirect('/index')
        if not id or id != 0:
            entry = Entry.query.get(id)
            if entry:
                return render_template('update.html', entry=entry)
    else:
        return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    if session['user'] != None:
        if not id or id != 0:
            entry = Entry.query.get(id)
            if entry:
                db.session.delete(entry)
                db.session.commit()
            return redirect('/index')
    else:
        return redirect('/')


@app.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            entry.status = not entry.status
            db.session.commit()
        return redirect('/index')
    else:
        return redirect('/')