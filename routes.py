from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def kalkulacka_trojuhelniku():
    return render_template("page.html")

if __name__ == "__main__":
    app.run(debug=True)