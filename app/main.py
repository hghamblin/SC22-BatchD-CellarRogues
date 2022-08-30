# Run by typing python3 main.py

# import basics
import os
import pathlib

# import stuff for our web server
import flask
from flask import Flask, request, redirect, render_template, session, jsonify
from utils import get_base_url
from random import choice, randint
# import json

import csv
from math import ceil

# import login stuff
import flask_login
from flask_login import current_user
from hashlib import sha256

# import stuff for our models
from aitextgen import aitextgen

# import our own functions
# from helpers import fix_headline, get_headline_info, save_json
from helpers import fix_headline, add_headline_txt, get_mugshot, get_date

# load up a model from memory. Note you may not need all of these options.
ai = aitextgen(model_folder="model/", to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 8080
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url + 'static')

app.secret_key = os.urandom(64)

# login stuff
accounts_file = "./accounts.txt"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


def create_user(username):
    user = User()
    user.id = username
    return user


@login_manager.user_loader
def user_loader(username):
    username = username.strip()

    with open(accounts_file, 'r') as f:
        f.seek(0)
        lines = f.readlines()
        for l in lines:
            u, s, p = l.split("$")
            if username == u:
                return create_user(username)
    return


@login_manager.request_loader
def request_loader(request):
    if request.form.get('username'):
        username = request.form.get('username').strip()
        with open(accounts_file, 'r') as f:
            f.seek(0)
            lines = f.readlines()
            for l in lines:
                u, s, p = l.split("$")
                if username == u:
                    return create_user(username)
    return


pepper = "alligator"

CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


@app.route(f'{base_url}/signup', methods=['GET', 'POST'])
def signup():
    if flask.request.method == 'GET':
        return render_template('login.html',
                               type="SIGN UP",
                               action="signup",
                               otherA="./login",
                               otherT="Already have an account? Login")
    elif flask.request.method == 'POST':
        username = flask.request.form['username'].strip()
        password = flask.request.form['password'].strip()

        if '$' in username:
            return 'stop'

        with open(accounts_file, 'a+') as f:
            f.seek(0)
            lines = f.readlines()
            for l in lines:
                u, s, p = l.split("$")
                if username == u:
                    return 'Username already taken'

            salt = ''.join(choice(CHARS) for i in range(16))
            hashedPassword = sha256(
                (password + salt + pepper).encode('utf-8')).hexdigest()
            f.write("{}${}${}\n".format(username, salt, hashedPassword))
        with open(f'./votes/{username}.txt', 'w') as f:
            f.write('$')
        return redirect('../login')


#         return 'Sign up successful'

    return 'Bad signup'


@app.route(f'{base_url}/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html',
                               type="LOGIN",
                               action="login",
                               otherA="./signup",
                               otherT="New user? Sign up")
    elif flask.request.method == 'POST':
        username = flask.request.form['username'].strip()
        password = flask.request.form['password'].strip()

        with open(accounts_file, 'r') as f:
            f.seek(0)
            lines = f.readlines()
            for l in lines:
                u, s, p = l.split("$")
                if username == u:
                    hashedPassword = sha256(
                        (password + s + pepper).encode('utf-8')).hexdigest()
                    if hashedPassword == p.strip('\n'):
                        user = User()
                        user.id = username
                        flask_login.login_user(user)
                        f.close()
                        return redirect('../profile')
                    break
            return redirect('../login')
    return 'Bad login'


@app.route(f'{base_url}/logout')
def logout():
    flask_login.logout_user()
    return redirect('./')

@flask_login.login_required
@app.route(f'{base_url}/profile/')
def profile():
    args = dict(request.args)

    headlines = []
    if current_user.is_authenticated:
        user = current_user.get_id()
        with open(f'./votes/{user}.txt', 'r') as f:
            likes, dislikes = f.read().split('$')

            likes = likes.split(',')[1:]
            dislikes = dislikes.split(',')[1:]

        for fn in likes:
            with open(f'./headlines/{fn}.txt', 'r') as hf:
                headline = hf.read().split('\n')

                headline.append(1)
                headline.append(fn)
                headlines.append(headline)

        headlines = headlines[::-1]
        
        for i in range(len(headlines)):
            headlines[i].append(i + 1)

        if 'page' in args:
            if int(args['page']) > ceil(len(headlines) / 20):
                return redirect(f'?page={ceil(len(headlines)/20)}')
            elif int(args['page']) < 1:
                return redirect('?page=1')
            return render_template(
                'headline_explorer.html',
                headlines=headlines[20 * (int(args["page"]) - 1):20 *
                                    (int(args["page"]) - 1) + 20],
                page=int(args["page"]),
                pages=ceil(len(headlines) / 20))
        return render_template('profile.html',
                               headlines=headlines[0:20],
                               page=1,
                               pages=ceil(len(headlines) / 20),
                               base_url=base_url)
    else:
        return redirect('../login')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('florida_man_generator.html')


@app.route(f'{base_url}/model/', methods=['GET', 'POST'])
def model():
    if request.method == "GET":
        return render_template('model.html')
    elif request.method == "POST":
        person = request.form['person']
        prompt = request.form['prompt']
        prompt = person + " " + prompt
        if prompt is not None:
            generated = ai.generate(n=1,
                                    batch_size=3,
                                    prompt=str(prompt),
                                    max_length=25,
                                    temperature=0.7,
                                    return_as_list=True)
            generated = fix_headline(generated[0])

        mugshot = get_mugshot(generated)
        date = get_date()
        id = add_headline_txt([
            generated.replace('\r', '').replace('\n', ''), mugshot, date, 0,
            prompt.replace('\r', '').replace('\n', '')
        ])
        return render_template('model.html',
                               result=generated,
                               img=mugshot,
                               date=date,
                               headline_id=id)


@app.route(f'{base_url}/headline_mod/updateLikes/', methods=['POST'])
def update_likes():
    if flask.request.method == 'POST':
        if current_user.is_authenticated:
            user = current_user.get_id()
        else:
            return "LOGIN", 500

        headline_id = request.form['headline_id']

        with open(f'./headlines/{headline_id}.txt', 'r') as f:
            headline = f.read().split('\n')

        with open(f'./votes/{user}.txt', 'r') as f:
            likes, dislikes = f.read().split('$')

        likes = likes.split(',')
        dislikes = dislikes.split(',')

        liked = headline_id in likes
        disliked = headline_id in dislikes

        user_choice = 0
        result = 0

        if request.form['like'] and request.form['like'] == "true":
            if liked:
                likes.remove(headline_id)
                result = -1
            elif disliked:
                dislikes.remove(headline_id)
                likes.append(headline_id)
                user_choice = 1
                result = 2
            else:
                likes.append(headline_id)
                user_choice = 1
                result = 1
        elif request.form['like'] and request.form['like'] == "false":
            if liked:
                dislikes.append(headline_id)
                likes.remove(headline_id)
                user_choice = -1
                result = -2
            elif disliked:
                dislikes.remove(headline_id)
                result = 1
            else:
                dislikes.append(headline_id)
                user_choice = -1
                result = -1

        with open(f'./votes/{user}.txt', 'w') as f:
            f.write('$'.join([','.join(likes), ','.join(dislikes)]))

        with open(f'./headlines/{headline_id}.txt', "w") as f:
            headline[3] = str(int(headline[3]) + result)
            f.write('\n'.join(headline))

        return jsonify({
            'likes': str(int(headline[3])),
            'choice': user_choice,
        }), 200


@app.route(f'{base_url}/headline/<headline_id>')
def headline(headline_id):
    with open(f'./headlines/{headline_id}.txt') as f:
        headline = f.read().split('\n')

    user_choice = 0

    if current_user.is_authenticated:
        user = current_user.get_id()
        username, likes, dislikes = None, None, None
        with open(f'./votes/{user}.txt', 'r') as f:
            likes, dislikes = f.read().split('$')

        likes = likes.split(',')
        dislikes = dislikes.split(',')

        if headline_id in likes:
            user_choice = 1
        elif headline_id in dislikes:
            user_choice = -1
    
    return render_template('headline.html',
                           result=headline[0],
                           img=headline[1],
                           date=headline[2],
                           headline_id=headline_id,
                           likes=headline[3],
                           prompt=fix_headline(headline[4]),
                           base_url=base_url,
                           user_choice=user_choice)


@app.route(f'{base_url}/headline_explorer/')
def headline_explorer():
    args = dict(request.args)

    headlines = []
    user = None
    if current_user.is_authenticated:
        user = current_user.get_id()
        with open(f'./votes/{user}.txt', 'r') as f:
            likes, dislikes = f.read().split('$')

            likes = likes.split(',')
            dislikes = dislikes.split(',')

    for fn in os.listdir('./headlines'):
        with open(f'./headlines/{fn}', 'r') as hf:
            headline = hf.read().split('\n')
            id = fn.strip('.txt')

            user_choice = 0
            if user:
                if id in likes:
                    user_choice = 1
                elif id in dislikes:
                    user_choice = -1

            headline.append(user_choice)
            headline.append(fn.strip('.txt'))
            headlines.append(headline)

    headlines.sort(key=lambda x: x[3], reverse=True)
    for i in range(len(headlines)):
        headlines[i].append(i + 1)

    if 'page' in args:
        if int(args['page']) > ceil(len(headlines) / 20):
            return redirect(f'?page={ceil(len(headlines)/20)}')
        elif int(args['page']) < 1:
            return redirect('?page=1')
        return render_template(
            'headline_explorer.html',
            headlines=headlines[20 *
                                (int(args["page"]) - 1):20 *
                                (int(args["page"]) - 1) + 20],
            page=int(args["page"]),
            pages=ceil(len(headlines) / 20))
    print([len(i) if len(i) == 8 else i for i in headlines])
    return render_template('headline_explorer.html',
                           headlines=headlines[0:20],
                           page=1,
                           pages=ceil(len(headlines) / 20),
                           base_url=base_url)


if __name__ == '__main__':
    website_url = '' # if hosting on production WSGI server, put URL or IP address here

    if website_url != '':
        print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
