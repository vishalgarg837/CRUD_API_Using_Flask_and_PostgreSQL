from flask import Flask, render_template, request
from flask import jsonify
import psycopg2
import sys

 
app = Flask(__name__)
myConn = None

try:
    myConn = psycopg2.connect(database = "python_crud_test", user = "postgres")   
    cur = myConn.cursor()
except psycopg2.DatabaseError, e:
    print "I am unable to connect to the database."
    if myConn:
        myConn.rollback()
    print "Error: %s" %e
    sys.exit(1)
'''finally:
    if myConn:
        myConn.close()   '''
         
@app.route('/create')
def create():
    cur.execute("DROP TABLE IF EXISTS Student")
    cur.execute("CREATE SEQUENCE id_sequence start 1 increment 1; CREATE TABLE IF NOT EXISTS Student(Id integer PRIMARY KEY default nextval('id_sequence'), Stu_Name VARCHAR(50), Mob_Number VARCHAR(10), Reg_Date date, Email_Id VARCHAR(50))")
    myConn.commit()
    return jsonify( { "message" : "Table Created Successfully!" }), 200    

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/check_add_validation', methods = ['POST'])
def add_get():
    if request.method == 'POST':
        stuName = request.form['Stu_Name']
        mobNumber = request.form['Mob_Number']
        regDate = request.form['date']
        emailId = request.form['Email_Id']          
        query = "INSERT INTO Student(id, Stu_Name, Mob_Number, Reg_Date, Email_Id) VALUES(nextval('id_sequence'), %s, %s, %s, %s)"
        data = (stuName, mobNumber, regDate, emailId)
        cur.execute(query, data)
        myConn.commit()
        return jsonify({ "message" : "Data Added Successfully!"})
    else:
        return jsonify({ "message" : "Data not added!"})        

@app.route('/fetch')
def fetch():
    cur.execute("SELECT * FROM Student")
    rows = cur.fetchall()
    return render_template('fetch.html', result = rows)

@app.route('/updateData')
def update():
    cur.execute("SELECT * from Student ORDER BY id")
    rows = cur.fetchall()
    return render_template('updateData.html', result = rows)

@app.route('/update_db_code', methods = ['GET', 'POST'])
def update_data():
    if request.method == 'POST':
        ID = request.form.get('selectId')
        #ID = request.form['Id']
        stuName = request.form['Stu_Name']
        mobNumber = request.form['Mob_Number']
        regDate = request.form['t3']
        emailId = request.form['Email_Id']
        query = "UPDATE student SET stu_name = %s, mob_number = %s, reg_date = %s, email_id = %s WHERE student.id=%s"
        data = (stuName, mobNumber, regDate, emailId, ID)
        cur.execute(query, data)
        myConn.commit()
        return jsonify({ "message" : "Data updated!"})
    elif request.method == 'GET':
        return jsonify({ "message" : "Data not updated due to unavailable data!"})    
    else:
        return jsonify({ "message" : "Data not updated!"})    

@app.route('/delete')
def delete():
    cur.execute("SELECT * from Student ORDER BY id")
    rows = cur.fetchall()
    return render_template('delete.html', result = rows)


@app.route('/delete_db_code', methods = ['GET', 'POST'])
def delete_data():
    if request.method == 'POST':
        ID = request.form.get('selectId')
        '''ID = request.form['Id']
        stuName = request.form['t1']
        mobNumber = request.form['t2']
        regDate = request.form['t3']
        emailId = request.form['t4']'''
        query = "DELETE FROM student WHERE student.id=%s"
        #updateIDQuery = "ALTER TABLE student AUTO_INCREMENT = 1"
        #alterQuery = "ALTER SEQUENCE student_id_seq RESTART WITH 1"
        #alterQuery = "SET  @num := 0; UPDATE Student SET id = @num := (@num+1); ALTER TABLE Student AUTO_INCREMENT = 1;"
        data = (ID)
        cur.execute(query, data)
        #cur.execute(updateIDQuery)
        #cur.execute(alterQuery)
        myConn.commit()
        return jsonify({ "message" : "Data deleted successfully!"})
    elif request.method == 'GET':
        return jsonify({ "message" : "Data not deleted due to unavailable data!"})    
    else:
        return jsonify({ "message" : "Data not deleted!"})   

if __name__=='__main__':
    app.run(debug=True, host = "0.0.0.0", port = 5000)
