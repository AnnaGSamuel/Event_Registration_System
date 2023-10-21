from flask import Flask,render_template,request
import mysql.connector
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "event"
)

admin_password = "123*"

cursor = db.cursor()

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def delete_expired_events():
    current_date = datetime.today()
    cursor.execute("DELETE FROM form WHERE end_date < %s", (current_date,))
    db.commit()

def schedule_event_deletion():
    scheduler.add_job(delete_expired_events, 'interval', hours=6)  # Runs the task daily
    

@app.route("/")
def show_events():
    cursor.execute("SELECT * FROM form ORDER BY start_date")  
    all_events = cursor.fetchall()
    return render_template("event.html",events = all_events)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        entered_password = request.form["password"]
        if entered_password == admin_password:
            return render_template("log_form.html")
        else:
            error_message = "Wrong password. Please try again."
            return render_template("login.html", error_msg=error_message)
    return render_template("login.html")


@app.route("/submit_form", methods = ["POST", "GET"])
def submit_form():
    if(request.method == "POST"):
        institution_name = request.form["institution_name"]
        full_name = request.form["fullname"]
        email = request.form["emailaddress"]
        phone = request.form["phone_number"]
        event_name= request.form["title_name"]
        count = request.form["Number"]
        start_date_str= request.form["start_date"]
        end_date_str= request.form["end_date"]
        photo= request.form["photo"]
        food= request.form["food"]
        terms= request.form["terms"]
    
        # Parse the datetime string from the form
        start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
        
        try:
            query = "SELECT * FROM form WHERE (start_date <= %s AND end_date >= %s) OR (start_date <= %s AND end_date >= %s)"
            cursor.execute(query, (start_date, start_date, end_date, end_date))
            is_date_booked = cursor.fetchone()

            if(is_date_booked):
                error_message = "Sorry, the selected time slot is already booked. Please choose another date."
                return render_template("log_form.html",error_msg = error_message)
            else:
                sql = "INSERT INTO form (inst_name,full_name,email,phone, event_name,count,start_date,end_date,photo,food,terms) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (institution_name,full_name,email,phone,event_name,count,start_date,end_date,photo,food,terms)
                cursor.execute(sql,values)
                db.commit()
    
                return render_template("reg_success.html",inst_name=institution_name,name=full_name,email=email,phone=phone,ename=event_name,count=count,start=start_date,end=end_date,photo_choice=photo,food_choice=food,terms=terms)
              
        except Exception as e:
            # Handle database-related errors here
            error_message = "An error occurred: " + str(e)
            return render_template("log_form.html", error_msg=error_message)

if(__name__ == "__main__"):
    schedule_event_deletion()
    app.run(debug=True)
