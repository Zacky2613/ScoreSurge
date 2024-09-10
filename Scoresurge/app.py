from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_migrate import Migrate
from datetime import datetime


# Flask config.
app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database.db"

# Database config.
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Api
api = Api(app)

class Study_Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_spent_total = db.Column(db.Integer)
    time_spent_class = db.Column(db.Integer)
    
    time_spent_date = db.Column(db.Integer)
    class_name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)


class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False, unique=True)
    grade_semester_1 = db.Column(db.String(5), nullable=False)
    grade_semester_2 = db.Column(db.String(5), nullable=False)


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
    page_id = db.Column(db.String(40), nullable=False, unique=True)
    teacher = db.Column(db.String(30))
    class_room = db.Column(db.String(20))
    
    # grades = db.Column(db.String(20))
    # class_room = db.Column(db.String(20))
    
    def __repr__(self) -> str:
        return f"Schedule: {self.content}"


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    week_number = db.Column(db.Integer)
    day_of_week = db.Column(db.String(20))
    period = db.Column(db.String(20))
    class_name = db.Column(db.Text)
    
    content_title = db.Column(db.String(60))
    period_type = db.Column(db.String(40))
    content = db.Column(db.Text)

    
    def __repr__(self) -> str:
        return f"Schedule: {self.content}"



# Defining multiple routes for the same function.
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/classes/<string:page_id>")
def classes(page_id):
    class_name = page_id.replace("_", " ").title()
    class_data = Classes.query.filter_by(class_name=class_name).first()
    schedule_data = Schedule.query.filter_by(class_name=class_data.class_name).all()
    grades_data = Grades.query.filter_by(class_name=class_data.class_name)
    
    grouped_schedule = {}
    for schedule in schedule_data:
        week_class_key = schedule.week_number
        
        # Check if the key exists, if not create an empty list
        if week_class_key not in grouped_schedule:
            grouped_schedule[week_class_key] = []
            
        # Append the schedule to the appropriate list
        grouped_schedule[week_class_key].append(schedule)
    
    return render_template(
        "classes.html", 
        class_data=class_data,
        schedule=schedule_data,
        grouped_schedule=grouped_schedule,
        grades_data=grades_data,
        page_id=page_id
    )

@app.route("/grades")
def grades():
    grades_data = Grades.query.all()
    
    return render_template(
        "grades.html",
        grades=grades_data
    )

@app.route("/study_tracker")
def study_tracker():
    study_tracker_data = Study_Tracker.query.all()
    total_time = db.session.query(db.func.sum(Study_Tracker.time_spent_total)).scalar()
    
    return render_template(
        "study_tracker.html",
        study_tracker=study_tracker_data,
        total_time=total_time
    )

@app.template_filter('format_time')
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    returnable_time = []
    if (hours > 0):
        returnable_time.append(f"{int(hours)}h")
    if (minutes > 0):
        returnable_time.append(f"{int(minutes)}m")
    if (seconds > 0 or not returnable_time):
        returnable_time.append(f"{int(seconds)}s")
        
    return " ".join(returnable_time)

# Note updating
@app.route("/notes/<string:page_id>", methods=["POST", "GET"])
def notes(page_id):
    note = Notes.query.filter_by(page_id=page_id).first()
    class_data = Classes.query.filter_by(page_id=page_id).first()
    
    if (request.method == "POST"):
        # Grabbing the text inside the user's notes.
        note_content = request.form["content"]

        if note:
            note.content = note_content

        else:
            note_name = page_id.replace("_", " ").title()
            note = Notes(note_name=note_name, page_id=page_id, content=note_content)
            db.session.add(note)
            

        db.session.commit()
        return redirect(url_for("notes", page_id=page_id))
    
    # If the note the user is trying to access don't exist.
    if not note:
        return "You haven't created this note, please do so by pressing + next to classes", 404

    return render_template("notes.html", note=note, class_data=class_data, page_id=page_id)    

@app.route("/timetable")
def timetable():
    now = datetime.now()
    # day_of_week_today = now.strftime("%A")
    day_of_week_today = "Monday"

    # Fetch today's schedules from the database
    today_schedule = Schedule.query.filter_by(day_of_week=day_of_week_today).all()


    timetable_data = {}
    for schedule in today_schedule:
        period = schedule.period
        if period not in timetable_data:
            timetable_data[period] = []
            
        timetable_data[period].append({
            "class_name": schedule.class_name,
            "content_title": schedule.content_title,
            "period_type": schedule.period_type,
            "content": schedule.content
        })
    
    return render_template(
        "timetable.html",
        timetable=timetable_data,
        day_of_week=day_of_week_today
    )

@app.route("/track_time", methods=["POST"])
def track_time():
    
    # The data sent from the javascript in js/base.js
    time_spent_seconds = round(int(request.form.get("time_spent", 0)) / 1000, 2)
    # time_spent_seconds = 100000000
    date = request.form.get("time_date")
    class_name = request.form.get("class_name")

    # If this entry is for a class/note or not
    if class_name:
        study_tracker_data = Study_Tracker.query.filter_by(class_name=class_name, date=date).first()
    else:
        study_tracker_data = Study_Tracker.query.filter_by(class_name=None, date=date).first()
    
    # If the record already exists
    if study_tracker_data:
        study_tracker_data.time_spent_total += time_spent_seconds
        study_tracker_data.time_spent_class += time_spent_seconds
        study_tracker_data.time_spent_date += time_spent_seconds
        
        db.session.commit()
        message = "Time updated successfully"
        
    # Making new record
    else:
        time_track = Study_Tracker(
            class_name = class_name,
            time_spent_date = time_spent_seconds,
            time_spent_class = time_spent_seconds,
            time_spent_total = time_spent_seconds,
            date=date
        )
        
        db.session.add(time_track)
        db.session.commit()
        
        message = "Time Created successfully"
        
    
    return message, 200
    

@app.route("/edit_grades", methods=["POST"])
def edit_grades():
    grades = Grades.query.all()
    
    for grade in grades:
        selected_grade_semester_1 = request.form.get(f"new_grade_semester_1_{grade.id}")
        selected_grade_semester_2 = request.form.get(f"new_grade_semester_2_{grade.id}")
        
        # Updating the new grades
        if selected_grade_semester_1:
            grade.grade_semester_1 = selected_grade_semester_1
            
        if selected_grade_semester_1:
            grade.grade_semester_2 = selected_grade_semester_2
    
    db.session.commit()

    return redirect(url_for("grades"))


@app.route("/add_to_class_planner/<string:page_id>", methods=["POST"])
def add_to_class_planner(page_id):
    class_data = Classes.query.filter_by(page_id=page_id).first()
    
    week_number = request.form["week_number"]
    day_of_weeks = request.form.getlist("day_of_week[]")
    periods = request.form.getlist("period[]")
    period_headers = request.form.getlist("period-header[]")
    period_contents = request.form.getlist("content[]")
    
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
        period = periods[i]

        
        new_week_entry = Schedule(
            class_name=class_data.class_name, 
            week_number=week_number,
            day_of_week=day_of_week,
            period=period,
            content_title=header,
            content=content,
        )
        
        db.session.add(new_week_entry)
        db.session.commit()
        
    
    return redirect(url_for("classes", page_id=page_id))

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
        day, period = day.split(" ")
        
        print(day, period)

        new_planner = Schedule(
            class_name=class_data.class_name, 
            day_of_week=day,
            period=period,
            week_number=1
        )
        db.session.add(new_planner)
        db.session.commit()
        
        x += 1

    return redirect(url_for("classes", page_id=page_id))



@app.route("/create_note_and_class", methods=["POST"])
def create_class():
    note_and_class_title = request.form["class_name"]
    teacher_name = request.form["teacher"]
    class_room = request.form["class_room"]
    grade_semester_1 = request.form["grade_semester_1"]
    grade_semester_2 = request.form["grade_semester_2"]
    

    page_id = note_and_class_title.lower().replace(" ", "_")
    note_and_class_title_clean = page_id.replace("_", " ").title()
    
    existing_class = Notes.query.filter_by(page_id=page_id).first()

    # If the new class is unqiue
    if not existing_class:
        new_grades = Grades(
            class_name = note_and_class_title_clean,
            grade_semester_1 = grade_semester_1,
            grade_semester_2 = grade_semester_2
        )
        
        new_class = Classes(
            class_name = note_and_class_title_clean, 
            page_id = page_id,
            teacher = teacher_name,
            class_room = class_room
        )
        
        new_note = Notes(
            note_name=note_and_class_title_clean, 
            page_id=page_id, 
            content=""
        )
        
        new_schedule = Schedule(
            
        )
        
        db.session.add(new_class)
        db.session.add(new_grades)
        db.session.add(new_note)
        
        db.session.commit()
        
    return redirect(url_for("classes", page_id=page_id))



@app.context_processor
def inject_data():
    notes = Notes.query.all()
    classes = Classes.query.all() 
    schedule = Schedule.query.all() 

    data = {
        "notes": notes,
        "classes": classes,
        "schedule": schedule,
        "username": "John Doe"
    }
    
    return data


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    
    app.run(debug=True)