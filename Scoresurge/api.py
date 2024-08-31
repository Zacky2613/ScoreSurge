from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from datetime import datetime


# Flask config.
app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database.db"

# Database config.
db = SQLAlchemy(app)

# Api
api = Api(app)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.String(50), nullable=False, unique=True)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Content: {self.content}"


# Defining multiple routes for the same function.
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/notes/<string:page_id>", methods=["POST", "GET"])
def notes(page_id):
    
    note = Notes.query.filter_by(page_id=page_id).first()
    
    
    if (request.method == "POST"):
        # Grabbing the text inside the user's notes.
        note_content = request.form['content']


        if note:
            note.content = note_content
        else:
            note = Notes(page_id=page_id, content=note_content)
            db.session.add(note)

        db.session.commit()
        return redirect(url_for('notes', page_id=page_id))


    return render_template("notes.html", note=note, page_id=page_id)    


        

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)