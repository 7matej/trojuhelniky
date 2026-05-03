from flask import Flask, render_template

import zobrazeni

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def kalkulacka_trojuhelniku():
    return render_template("page.html", zobrazeni=zobrazeni.zbr)

if __name__ == "__main__":
    app.run(debug=True)