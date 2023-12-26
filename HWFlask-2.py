from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name")
    email = request.form.get("email")

    resp = make_response(redirect("/hello"))
    resp.set_cookie("name", name)
    resp.set_cookie("email", email)
    return resp


@app.route("/hello")
def hello():
    name = request.cookies.get("name")
    email = request.cookies.get("email")
    return render_template("hello.html", name=name, email=email)


@app.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie("name")
    response.delete_cookie("email")
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8000)
