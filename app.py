from flask import Flask,render_template,request,json
import sqlite3
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('login.html')

@app.route("/upload")
def upload():
    return render_template('upload.html')


@app.route('/labelPlate',methods = ['POST', 'GET'])
def labelPlate():
    return render_template('labelPlate.html')

@app.route('/sendPlt',methods = ['POST', 'GET'])
def sendPlt():
    if request.method=='POST':
        lb=request.form['label']
        user=request.form['user']
        img_name=request.form['img_name']
        with sqlite3.connect("database.db") as conn:
            try:
                flag=checkExistInDB_Plate(user,img_name)
                if flag==True:
                    msg="You had label this plate"
                    return json.dumps({'msg':msg})
                cur=conn.cursor()
                cur.execute("INSERT INTO Plate (username,image_name,labelPlate) values (?,?,?)",(user,img_name,lb))
                conn.commit()
                msg="Add successful"
            except:
                conn.rollback()
                msg="can't be add"  
            finally:
                return json.dumps({'msg':msg})
                conn.close()              
    return "Failed"

@app.route('/viewPlt')
def viewPlt():
    conn=sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("select * from Plate")
    #cur.execute("select * from Plate where username='Binh'")
    rows=cur.fetchall()
    return render_template("viewPlt.html",rows=rows)

def checkExistInDB_Plate(user,img_name):
    conn=sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("select * from Plate where username='{0}' and image_name='{1}'".format(user,img_name))
    rows=cur.fetchall()
    if not rows:
        return False
    return True
if __name__ == '__main__':
    app.run(debug=True)