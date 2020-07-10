from application import app, db, api
from flask import render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application.models import User, Seed_urls, Urls_to_crawl, Articles, Topics, Following
from application.forms import LoginForm, RegisterForm
from flask_restplus import Resource
from application.topic_user import *


@api.route('/api','/api/')
class GetAndPost(Resource):

    #GET ALL
    def get(self):
        return jsonify(User.objects.all())

    #POST
    def post(self):
        data = api.payload
        user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))

@api.route('/api/<idx>')
class GetUpdateDelete(Resource):

    #GET ONE
    def get(self,idx):
        return jsonify(User.objects(user_id=idx))
        
    #PUT
    def put(self,idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx)) 
        
    #DELETE
    def delete(self,idx):
        User.objects(user_id=idx).delete()
        return jsonify("User is deleted!")

#######################################

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True )


@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True )

@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('index'))


@app.route("/topics/", methods=['GET','POST'])
def topics():
    if not session.get('username'):
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    tags = get_other_topic(user_id)
    return render_template("topics.html", topicData=tags, topics = True)

@app.route("/register", methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id     = User.objects.count()
        user_id     += 1

        email       = form.email.data
        password     = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)



@app.route("/following", methods=["GET","POST"])
def following():

    if not session.get('username'):
        return redirect(url_for('login'))

    topic_id = request.form.get('topic_id')
    name = request.form.get('name')
    user_id = session.get('user_id')

    if topic_id:
        if Following.objects(user_id=user_id,topic_id=topic_id):
            flash(f"Oops! You are already registered in this Topic {name}!", "danger")
            return redirect(url_for("topics"))
        else:
            Following(user_id=user_id, topic_id=topic_id).save()
            flash(f"You are enrolled in {name}!", "success")

    news = user_feed(user_id)
    topics = user_topics(user_id)
    channels = get_channel()
    # flash(f"Oops! You are already registered in this Topic {news[1]}!", "danger")

    return render_template("following.html", following=True, title="News For You", news=news, topics=topics, channels=channels)    



