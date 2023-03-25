from flask import Flask, render_template, request, redirect, url_for
from validator import validate
import json
import uuid

app = Flask(__name__)


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


@app.post("/users")
def users_post():
    id_user = uuid.uuid4()
    user = request.form.to_dict()
    new_user = {'id': str(id_user),
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

    return redirect(url_for("show_users"), 302)


@app.route("/users")
def show_users():
    with open("data_file.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        users = data["users"]
    return render_template("/users/show_users.html", users=users)


# if __name__ == "__main__":
#     app.run(debug=True)
