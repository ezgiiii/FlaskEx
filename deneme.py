from flask import Flask, render_template

# Flask Instance
app = Flask(__name__)



# def index():
#     return "<h1> Hi Flask </h1>"

# Route Decorator

@app.route('/')
def index():

    first_name = "ezgi eftekin"
    stuff = "This is <strong> bold </strong> text"
    fav_pizza = ["Veggy", "mushroom", "peperoni", "margarita", "cin fizz", "manhattan", "martini", 23]

    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           fav_pizza=fav_pizza)

# localhost:5000/user/Slowpoke
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# <h1>Hi {{user_name|upper}}-san!!</h1>
# <h1>Hi {{user_name|lower}}-san!!</h1>
# <h1>Hi {{user_name|capitalize}}-san!!</h1>
# safe: it passes the html code that we write
# striptags: it removes the html code we wanna pass
# if someone try to pass html to your code you add this to message or comment parts and prevent them to hack your web site
# title:
# trim:

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500



