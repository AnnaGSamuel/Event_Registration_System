from flask import Flask,render_template,request,session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret123*'

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "event"

)

cursor = db.cursor()

@app.route("/")
def show_form():
    return render_template("log_form.html")

'''@app.route("/login", methods=["GET"])
def original_form():
    error_message = None  # Initialize error_message to None by default

    return render_template("travel.html", error_msg=error_message)'''


@app.route("/login", methods = ["POST", "GET"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    start_date = request.form["date"]

    try:
         cursor.execute("SELECT COUNT(*) FROM form WHERE event_date = %s",(start_date,))
         is_date_booked = cursor.fetchone()[0]

         if(is_date_booked):
             session["error_message"] = "Already booked. Please choose another date"
             return render_template("log_form.html", error_msg=session.get("error_message"))
             '''error_message = "Already booked.Please choose another date."
             return render_template("travel.html",error_msg = error_message)'''
         else:
              sql = "INSERT INTO form (name,email,event_date) VALUES (%s,%s,%s)"
              values = (name,email,start_date)
              cursor.execute(sql,values)
              db.commit()
              
              last_inserted_id = cursor.lastrowid
              print(last_inserted_id)
              cursor.execute("SELECT * FROM form WHERE lastrowid = %s", (last_inserted_id,))
              last_inserted_row = cursor.fetchone()

              return render_template("reg_success.html",details=last_inserted_row)
              
    except Exception as e:
        # Handle database-related errors here
        error_message = "An error occurred: " + str(e)
        return render_template("log_form.html", error_msg=error_message)

if(__name__ == "__main__"):
    app.run(debug=True)

