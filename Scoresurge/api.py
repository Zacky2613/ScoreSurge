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
    
    def __repr__(self) -> str:
        return f"Schedule: {self.content}"


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    week_number = db.Column(db.Integer)
    day_of_week = db.Column(db.String(20)) 
    class_name = db.Column(db.Text)
    
    content_title = db.Column(db.String(60))
    content = db.Column(db.Text)
    
    # teacher = db.Column(db.String(40))
    # TODO = db.Column(db.String(40), nullable=True)
    
    
    def __repr__(self) -> str:
        return f"Schedule: {self.content}"



# Defining multiple routes for the same function.
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/classes/<string:page_id>")
def classes(page_id):
    class_data = Classes.query.filter_by(page_id=page_id).first()
    schedule_data = Schedule.query.filter_by(class_name=class_data.class_name).all()
    
    
    return render_template(
        "classes.html", 
        class_data=class_data,
        schedule=schedule_data,
        page_id=page_id
    )


@app.route("/add_to_class_planner/<string:page_id>", methods=["POST"])
def add_to_class_planner(page_id):
    class_data = Classes.query.filter_by(page_id=page_id).first()
    
    week_number = request.form["week_number"]
    day_of_weeks = request.form.getlist("day_of_week[]")
    period_headers = request.form.getlist("period-header[]")
    period_contents = request.form.getlist("period-content[]")
    
    print(day_of_weeks)
    print(period_headers)
    
    # Delete old entries if the user is trying to edit them
    Schedule.query.filter_by(
        class_name=class_data.class_name, 
        week_number=week_number
    ).delete()
    
    # Since these two should be the same length, we can just iterate through one
    for i in range(len(period_headers)):
        header = period_headers[i]
        content = period_contents[i]
        day_of_week = day_of_weeks[i]
        
        print(f"Header: {header}")
        print(f"Content: {content}")
        
        new_week_entry = Schedule(
            class_name=class_data.class_name, 
            week_number=week_number,
            day_of_week=day_of_week,
            content_title=header,
            content=content,
        )
        
        db.session.add(new_week_entry)
        db.session.commit()
        
    
    return redirect(url_for('classes', page_id=page_id))

@app.route("/debug_schedule_data")
def debug_schedule_data():
    # Fetch all schedule data
    all_schedules = Schedule.query.all()
    
    # Print all entries
    for schedule in all_schedules:
        print(f"Week Number: {schedule.week_number}, Day of Week: {schedule.day_of_week}, Title: {schedule.content_title}, Content: {schedule.content}")
    
    return "Check your console for the debug output.", 200


@app.route("/create_class_planner/<string:page_id>", methods=["POST"])
def create_class_planner(page_id):
    class_data = Classes.query.filter_by(page_id=page_id).first()
    
    class_times = request.form["days_of_week"]
    clean_class_times = class_times.split("|")
    
    x = 0
    for item in clean_class_times:
        day = item.replace(" ", "").replace("yP", "y P")

        new_day = Schedule(class_name=class_data.class_name, day_of_week=day, week_number=1)
        db.session.add(new_day)
        
        db.session.commit()
        x += 1

    return redirect(url_for('classes', page_id=page_id))



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
        
    return redirect(url_for('classes', page_id=page_id))


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
    
    # If the note the user is trying to access don't exist.
    if not note:
        return "You haven't created this note, please do so by pressing + next to classes", 404


    return render_template("notes.html", note=note, page_id=page_id)    




@app.context_processor
def inject_data():
    notes = Notes.query.all()
    classes = Classes.query.all() 
    schedule = Schedule.query.all() 
    
    grouped_schedule = {}
    for schedule in schedule:
        if schedule.week_number not in grouped_schedule:
            grouped_schedule[schedule.week_number] = []
            
        grouped_schedule[schedule.week_number].append(schedule)
    
    data = {
        "notes": notes,
        "classes": classes,
        "schedule": schedule,
        "grouped_schedule": grouped_schedule,
        "username": "John Doe"
    }
    
    return data


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    
    app.run(debug=True)