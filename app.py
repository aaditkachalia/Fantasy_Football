from flask import Flask, render_template,flash,redirect,url_for,session,logging,request,jsonify
from flask_mysqldb import MySQL 
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
import json
import pandas as pd


app=Flask(__name__)


#Config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_User']='root'
app.config['MYSQL_PASSWORD']='icaniwill'
app.config['MYSQL_DB']='myflaskapp'
app.config['MYSQL_CURSORCLASS']='DictCursor'


#Init mysql
mysql=MySQL(app)
#mysql.init_app(app)
#conn=mysql.connect()


def array(list3):
	string=""
	for x in list:
		string+=x
	return string

@app.route('/home')

def index():
	return render_template('start.html')
#global email
@app.route('/',methods=['GET','POST'])
def login():
	if request.method == 'POST':
	    email=request.form['email']
	    session['em']=email
	    password1=request.form['pass']
	    cur=mysql.connection.cursor()
	    results=cur.execute("Select * from login where email like %s and password like %s",[email,password1])
	    if(results>0):
	    	app.logger.info('Password Matched')
	    	cur.close()
	    	return render_template('start.html')
	    else:
	    	app.logger.info('Password not matched')
	    	return render_template('login_aa.html')
	    	cur.close()
	else:
		return render_template('login_aa.html')
	 

				
@app.route('/buildteam',methods=['GET','POST'])
def buildteam():
	try:

		cur=mysql.connection.cursor()
		result=cur.execute("select level_game from login where email like 'aaditkachalia@gmail.com'")
		level=cur.fetchone()
		mail=session.get('em')
		#rating=request.form.get("rating")
		#attackers=request.form.getlist('a[]')
		if request.method == "POST" :
			# values = request.form["values"]
			print("I suck")
			attackers=(request.get_json()["arr1"])
			print(attackers)
			new_attackers=[x+1 for x in attackers]
			print("Dude")
			print(new_attackers)
			attack_tuple=str(tuple(new_attackers))
			defense=(request.get_json()["arr2"])
			new_defense=[x+1 for x in defense]
			defense_tuple=str(tuple(new_defense))
			midfielder=(request.get_json()["arr3"])
			new_midfielder=[x+1 for x in midfielder]
			midfielder_tuple=str(tuple(new_midfielder))
			goalkeeper=(request.get_json()["arr4"])
			new_goalkeeper=[x+1 for x in goalkeeper]
			goalkeeper_tuple=str(tuple(new_goalkeeper))
			print(goalkeeper_tuple)
			print("ss")
			print(attackers)
			button_action=(request.get_json()["buttonaction"])
			print(button_action)
			len_t=len(attackers)+len(defense)+len(midfielder)+len(goalkeeper)
			print(len_t)
			if button_action==True:
				if len_t==15:
					#l=[]
					#for i in attackers:
					print("Wassup")
					attack1=cur.execute("select * from level%s_a where id in "+attack_tuple,[level['level_game']])
					final_attack=cur.fetchall()
					print("Bitch")
					defense1=cur.execute("select * from level%s_d where id in "+defense_tuple,[level['level_game']])
					final_defense=cur.fetchall()
					print("I like you")
					midfielder1=cur.execute("select * from level%s_m where id in "+midfielder_tuple,[level['level_game']])
					final_midfielder=cur.fetchall()
					print("More than anyone.")
					print(final_midfielder)
					goalkeeper1=cur.execute("select * from level%s_g where id in "+goalkeeper_tuple,[level['level_game']])
					final_goalkeeper=cur.fetchall()
					print("Huh?")
					final_team=final_goalkeeper+final_defense+final_midfielder+final_attack
					print(final_team)
					session['final']=final_team
					#print("I am the best.")
					#print(final_attack)
						 #call a function for populating database
					#insert_into(l,i,mail)
					"""for i in defense:
						l.append(mid.iloc[i].values)
						 #call a function for populating databask
						insert_into(l,i,mail)
					for i in midfielder:
						l.append(level1_a.iloc[i].values)
						 #call a function for populating database
						insert_into(l,i,mail)
					for i in goalkeeper:
						l.append(level1_a.iloc[i].values)
						 #call a function for populating database
						insert_into(l,i)
					validate=cut_amt(mail)
					if(validate==True):
						return render_template('yourteam.html')
					else:
						raise Exception"""
				else:
					raise Exception


			print(len_t)
			print(attackers)
			print(midfielder)
			print(defense)
			print(goalkeeper)
	        
		#email=session.get('email',2)	
		
		

		print("HI")
		print(level['level_game'])
		print("Bye")
		#print(rating)
		#app.logger.info(level.level_game)
	#	level1=int(level[level_game])
		actual_level=level['level_game']
		result1=cur.execute("select * from level%s_a",[level['level_game']])
		attack=cur.fetchall()
		#print(attack)
		result2=cur.execute("select * from level%s_m",[level['level_game']])
		mid=cur.fetchall()
		result1=cur.execute("select * from level%s_d",[level['level_game']])
		defense=cur.fetchall()
		result1=cur.execute("select * from level%s_g",[level['level_game']])
		goal=cur.fetchall()
		len_a=len(attack)
		len_d=len(defense)
		len_m=len(mid)
		len_g=len(goal)
		print(len_a)
		if result>0:
			return render_template('buildteam.html',len_d=len_d,len_m=len_m,len_g=len_g,len_a=len_a,actual_level=actual_level,attack=attack,defense=defense,mid=mid,goal=goal)
			cur.close()
		else:
			msg="There is some error in fetching"
			return render_template('buildteam.html',msg=msg)
		"""def buildteam():
			listname=request.args.get(list_name)
			list5=get_list(list_name)
			print("this is list5")
			print(list5)
			#array(list3)
			return jsonify("list")
			#print(list)
	"""
		cur.close()
	except Exception as e:
		print(e)
	
		msg="There is some error."
		return render_template('buildteam.html',msg=msg)
	#email=login()

def insert_into(l,i,mail):
	cur=mysql.connection.cursor()
	cursor.execute("""INSERT INTO userteam VALUES(%s,%d,%s,%s,%s,%d,%s,%d,%d,%d,%d,%s,%s,%d,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)""",
                   (mail,l[0][0],l[0][1],l[0][2],l[0][3],l[0][4],l[0][5],l[0][6],l[0][7],l[0][8],l[0][9],l[0][10],l[0][11],l[0][12],l[0][13],l[0][14],l[0][15],l[0][16],l[0][17],l[0][18],l[0][19],l[0][20],l[0][21],l[0][22],l[0][23],l[0][24],l[0][25],l[0][26],l[0][27],l[0][28],l[0][29],l[0][30],l[0][31],l[0][32],l[0][33],l[0][34],l[0][35],l[0][36],l[0][37],l[0][38],l[0][39],l[0][40],l[0][41],l[0][42],l[0][43],l[0][44],l[0][45],l[0][46],l[0][47],l[0][48],l[0][49],l[0][50],l[0][51],l[0][52],l[0][53],l[0][54],l[0][55]))
	mysql.connection.commit()
def cut_amt(mail):
    r1=cursor.execute("Select SUM(Price) from userteam where email=%s",[mail])
    summ=cur.fetchone()
    r2=cursor.execute("Select bank from user")
    b=cur.fetchone()
    b=b-sum
    if(b<0):
    	return False
    elif(b>=0):
    	return True
    else:
    	return False
    #if negative throw error
    cursor.execute("""update user
                   set bank=%d""",b)
@app.route('/yourteam',methods=['GET','POST'])
def myteam():
	email=session.get('em')
	final_team=session.get('final')
	print(email)
	print(final_team)
	return render_template('yourteam.html',email=email,final_team=final_team)

@app.route('/newuser',methods=['GET','POST'])
def signup():
	if request.method == 'POST':
	    email=request.form['emails']
	    print(email)
	    #conn=MySQL.connect('myflaskapp')
	    #session['em']=email
	    password1=request.form['passw']
	    password2=request.form['repassw']
	    print(password1)
	   # conn = .connect()
	    #cur = conn.cursor()
	    try:
	    	cur=mysql.connection.cursor()

	    	preresult=cur.execute("select MAX(userid) from login")
	    	lastuser=cur.fetchone();
	    	print(lastuser['MAX(userid)'])
	    	print(type(lastuser['MAX(userid)']))
	    	userid=int(lastuser['MAX(userid)'])+1
	    	print(userid)
	    	print(type(userid))
	    	results=cur.execute("Insert into login values(%s,%s,%s,1,40000)",(userid,email,password1))
	    	mysql.connection.commit()
	    	if(results>0):
	    		app.logger.info('User Signed In Sucesfully')
	    		cur.close()
	    		return render_template('start.html')
	    	else:
	    		app.logger.info('Password not matched')
	    		cur.close()
	    except Exception as e:
	    	print(e)
	else:
		return render_template('newuser.html')
		

	
    	


if __name__== '__main__':
	app.secret_key='secret123'
	app.run(debug=True)
