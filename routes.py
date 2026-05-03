from flask import Flask, render_template

from formular import Formular

formular = Formular(
    {
        "strana" : ("a", "b", "c"),
        "uhel" : ("α", "β", "γ"),
        "r" : "r",
    }
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def kalkulacka_trojuhelniku():
    return render_template("page.html", formular=formular)

if __name__ == "__main__":
    app.run(debug=True)