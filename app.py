from flask import Flask, flash, get_flashed_messages, render_template, request, redirect, url_for
from validator import validate
import json
import uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = "SECRET"


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
    messages = get_flashed_messages(with_categories=True)
    return render_template("/users/new.html", user=user, errors=errors, messages=messages)


@app.post("/users")
def users_post():
    id_user = uuid.uuid4()
    user = request.form.to_dict()
    new_user = {'id': str(id_user),
                'name': user['name'],
                'email': user['email']}
    errors = validate(new_user)
    if errors:
        flash('Error', category='error')
        messages = get_flashed_messages(with_categories=True)
        return render_template("/users/new.html", user=new_user, errors=errors, messages=messages)
    else:
        with open("data_file.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            data["users"].append(new_user)

        with open("data_file.json", "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, ensure_ascii=False)

        flash('User created successfully', 'success')
        return redirect(url_for("show_users"), 302)


@app.route("/users")
def show_users():
    with open("data_file.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        users = data["users"]

    messages = get_flashed_messages(with_categories=True)

    return render_template("/users/show_users.html", users=users, messages=messages)

# if __name__ == "__main__":
#     app.run(debug=True)
