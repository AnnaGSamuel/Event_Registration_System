from flask import Flask,render_template,request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root@123",
    database = "event"

)

cursor = db.cursor()

@app.route("/")
def show_form():
    return render_template("travel.html")

@app.route("/login", methods = ["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    start_date = request.form["date"]

    try:
         cursor.execute("SELECT COUNT(*) FROM form WHERE event_date = %s",(start_date,))
         is_date_booked = cursor.fetchone()[0]

         if(is_date_booked):
             error_message = "Already booked.Please choose another date."
             return render_template("travel.html",error_msg = error_message)
         else:
              sql = "INSERT INTO form (name,email,event_date) VALUES (%s,%s,%s)"
              values = (name,email,start_date)
              cursor.execute(sql,values)
              db.commit()
              
              

              return render_template("reg_success.html",name=name,email=email,st=start_date)
              
    except Exception as e:
        # Handle database-related errors here
        error_message = "An error occurred: " + str(e)
        return render_template("travel.html", error_msg=error_message)

if(__name__ == "__main__"):
    app.run(debug=True)

