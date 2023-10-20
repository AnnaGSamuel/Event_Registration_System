from flask import Flask,render_template,request,redirect,url_for
import mysql.connector

app = Flask(__name__)

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


@app.route("/login", methods = ["POST"])
def submit():
    if(request.method == "POST"):
        institution_name = request.form["institution_name"]
        full_name = request.form["fullname"]
        email = request.form["emailaddress"]
        phone = request.form["phone_number"]
        event_name= request.form["title_name"]
        count = request.form["Number"]
        start_date= request.form["start_date"]
        end_date= request.form["end_date"]
        photo= request.form["photo"]
        food= request.form["food"]
        terms= request.form["terms"]
        
        try:
            cursor.execute("SELECT COUNT(*) FROM form WHERE start_date = %s",(start_date,))
            is_date_booked = cursor.fetchone()[0]

            if(is_date_booked):
                error_message = "Already booked.Please choose another date."
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

@app.route("/event_list")
def event_list():
    return render_template("index.html")

if(__name__ == "__main__"):
    app.run(debug=True)

