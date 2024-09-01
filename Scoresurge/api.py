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
    note_name = db.Column(db.String(50), nullable=False, unique=True)
    page_id = db.Column(db.String(50), nullable=False, unique=True)
    content = db.Column(db.Text)
    
    def __repr__(self) -> str:
        return f"Content: {self.content}"


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False, unique=True)
    page_id = db.Column(db.String(50), nullable=False, unique=True)
    content = db.Column(db.Text)
    
    def __repr__(self) -> str:
        return f"Class: {self.content}"


# Defining multiple routes for the same function.
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/create_note_and_class", methods=["POST"])
def create_class():
    note_and_class_title = request.form["class_name"]

    page_id = note_and_class_title.lower().replace(" ", "_")
    note_and_class_title_clean = page_id.replace("_", " ").title()
    
    existing_class = Notes.query.filter_by(page_id=page_id).first()

    # If the new class is unqiue
    if not existing_class:
        new_class = Classes(class_name=note_and_class_title_clean, page_id=page_id)
        db.session.add(new_class)

        new_note = Notes(note_name=note_and_class_title_clean, page_id=page_id, content="")
        db.session.add(new_note)
        
        db.session.commit()
        
    return redirect(url_for('notes', page_id=page_id))



# Note updating
@app.route("/notes/<string:page_id>", methods=["POST", "GET"])
def notes(page_id):
    note = Notes.query.filter_by(page_id=page_id).first()
    
    
    if (request.method == "POST"):
        # Grabbing the text inside the user's notes.
        note_content = request.form['content']


        if note:
            note.content = note_content
            
        else:
            note_name = page_id.replace("_", " ").title()
            note = Notes(note_name=note_name, page_id=page_id, content=note_content)
            db.session.add(note)
            

        db.session.commit()
        return redirect(url_for('notes', page_id=page_id))


    return render_template("notes.html", note=note, page_id=page_id)    


@app.context_processor
def inject_data():
    notes = Notes.query.all()
    classes = Classes.query.all() 
    
    data = {
        "notes": notes,
        "classes": classes,
        "username": "John Doe"
    }
    
    return data


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    
    app.run(debug=True)