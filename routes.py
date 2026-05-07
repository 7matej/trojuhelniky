from flask import Flask, render_template, request

from formular import Formular


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def kalkulacka_trojuhelniku():
    
    formular = Formular(
    {
        "strana" : ("a", "b", "c"),
        "uhel" : ("α", "β", "γ"),
        "r" : "r",
        "S" : "S",
        "h" : ("h<sub>a</sub>", "h<sub>b</sub>", "h<sub>c</sub>"),
    }
    )
    if request.method == "POST":
        formular.zpracuj_hodnoty(request.form)
    
    return render_template("page.html", formular=formular)



if __name__ == "__main__":
    app.run(debug=True)