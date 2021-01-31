from flask import Flask,render_template,request,json,redirect,url_for
import sqlite3
app = Flask(__name__)

@app.route("/login",methods = ['POST', 'GET'])
def login():
    msg=""
    if request.method=='POST':
        username=request.form['username']
        with sqlite3.connect("database.db") as conn:
            try:                    
                cur=conn.cursor()
                cur.execute("INSERT INTO user (username)  values ('{0}')".format(username))
                conn.commit()                               
            except:
                conn.rollback()
                # msg="Username is existed!"    
                # return render_template('login.html',msg=msg)             
            # finally:
            #     conn.close()  
        return redirect(url_for('labelPlate',username=username))   
    return render_template('login.html',msg=msg)

@app.route("/",methods = ['POST', 'GET'])
@app.route("/home",methods = ['POST', 'GET'])
def home():
    msg=""
    # if request.method=='POST':
    #     username=request.form['username']
    #     with sqlite3.connect("database.db") as conn:
    #         try:                    
    #             cur=conn.cursor()
    #             cur.execute("INSERT INTO user (username) values (?)",(username))
    #             conn.commit()  
    #             return render_template('labelPlate.html',username=username)                 
    #         except:
    #             conn.rollback()
    #             msg="Username is existed!"    
    #             return render_template('login.html',msg=msg)             
    #         # finally:
    #         #     conn.close()  
    # return render_template('login.html',msg=msg)
    return render_template('login.html',msg=msg)


@app.route("/upload",methods = ['POST', 'GET'])
def upload():
    if request.method=='POST':
        filename=request.form['filename']
        lst=filename.split("**")
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        error=""
        for item in lst:
            if item=="":
                continue
            try:
                cur.execute("INSERT INTO dataset_img (filename) values ('{0}')".format(item))
            except:
                error=error+item+"**"
                continue
        conn.commit()
        msg="Upload to database success!"
        return json.dumps({'msg':msg,'error':error})
    return render_template('upload.html')


@app.route('/labelPlate/<username>')
def labelPlate(username):
    conn=sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    #get random 5 images
    cur.execute("select * from dataset_img where status=0 order by random() limit 5")
    rows=cur.fetchall()
    #get number of images user labeled
    cur.execute("select * from dataset_img where username='{0}'".format(username))
    count=len(cur.fetchall())
    #get remains
    cur.execute("select * from dataset_img where status=0")
    remains=len(cur.fetchall())
    return render_template('labelPlate.html',username=username,rows=rows,count=count,remains=remains)

@app.route('/sendPlt',methods = ['POST', 'GET'])
def sendPlt():
    if request.method=='POST':
        lb=request.form['listID_Label'].split("**")
        user=request.form['user']        
        data=dict()
        for item in lb:
            if item=="":
                continue
            tmp=item.split(":")
            data.update({tmp[0]:tmp[1]})
        error=""
        with sqlite3.connect("database.db") as conn:
            cur=conn.cursor()
            for key in data.keys():
                try:                               
                    cur.execute("Update dataset_img set label='{0}',status=1,username='{1}' where id={2} and status=0 ".format(data[key],user,key))                             
                except:
                    error=error+"Wrong in id="+key+"\r\n"
                    continue
            conn.commit()          
        return json.dumps({'error':error})             
    return "Failed"

@app.route('/delete_table_img',methods=['POST'])
def delete_table_img():
    if request.method=='POST':
        conn=sqlite3.connect("database.db")
        error=" "
        try:
            cur=conn.cursor()
            cur.execute("delete from dataset_img")
            conn.commit()
        except:
            error="Không thể xóa dataset"
        return json.dumps({'error':error})
    return "OK"
@app.route('/viewImg/<username>')
def viewImg(username):
    conn=sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("select * from dataset_img where username='{0}'".format(username))
    #cur.execute("select * from Plate where username='Binh'")
    rows=cur.fetchall()
    return render_template("viewImg.html",rows=rows)

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