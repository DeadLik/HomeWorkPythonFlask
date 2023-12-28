from flask import Flask, render_template, request, redirect, make_response, url_for

app = Flask(__name__)


@app.route("/", methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        resp = make_response(redirect(url_for("hello")))
        resp.set_cookie("name", name)
        resp.set_cookie("email", email)
        return resp
    return render_template("index.html")


@app.route("/hello", methods=['GET', "POST"])
def hello():
    if request.method == 'POST':
        response = make_response(redirect(url_for("index")))
        response.delete_cookie("name")
        response.delete_cookie("email")
        return response
    name = request.cookies.get("name")
    email = request.cookies.get("email")
    return render_template("hello.html", name=name, email=email)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
