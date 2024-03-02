from flask import Flask, url_for, request, render_template


app = Flask(__name__)


@app.route("/training/<prof>")
def index(prof):
    if "инженер" in prof or "строитель" in prof:
        return render_template('base.html', prof="Инженерные тренажеры")
    else:
        return render_template('base.html', prof="Научные симуляторы")


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')