from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

id_user = 0


@app.route("/")
def index():
    return render_template("/users/index.html")


@app.route("/users/new")
def users_new():
    user = {
        'name': '',
        'email': '',
    }
    errors = {}
    return render_template("/users/new.html", user=user, errors=errors)


def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = 'Form cant be empty'
    if not user['email']:
        errors['email'] = 'Form cant be empty'
    return errors


@app.post("/users")
def users_post():
    global id_user
    id_user = id_user + 1
    user = request.form.to_dict()
    new_user = {'id': id_user,
                'name': user['name'],
                'email': user['email']}
    errors = validate(new_user)
    if errors:
        return render_template("/users/new.html", user=new_user, errors=errors)
    with open("data_file.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        data["users"].append(new_user)

    with open("data_file.json", "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False)

    return redirect('/users', 302)


@app.route("/users")
def show_users():
    with open("data_file.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        users = data["users"]
    return render_template("/users/show_users.html", users=users)
