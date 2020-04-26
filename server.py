from flask import Flask, render_template, url_for, request, redirect
from operator import itemgetter
import csv

app = Flask(__name__)

# set the following env variables
# export FLASK_APP=server.py
# export FLASK_ENV=development

# run the following command to start the server
# flask run


# define end points

def write_to_db(data):
    with open("db.txt", "a") as db:
        email,subject,message = itemgetter("email", "subject", "message")(data)
        db.write(f"{email},{subject},{message}\n")


def write_to_csv(data):
    with open("db.csv", "a") as db:
        email,subject,message = itemgetter("email", "subject", "message")(data)
        csv_writer = csv.writer(db, delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/<string:page_name>')
def html_page(page_name=None):
    print(page_name)
    return render_template(f"{page_name if page_name else index}.html")

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect("/thankyou")
        except:
            return "db save error"
    else:
        return "something went wrong. Try again"
