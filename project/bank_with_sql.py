from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import*
from datetime import datetime
import pymysql
# Create or connect to the database
con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS useraccount (
        name VARCHAR(255),
        password VARCHAR(255),
        email VARCHAR(255),
        mob VARCHAR(15),
        acn INT PRIMARY KEY AUTO_INCREMENT,
        Bal DOUBLE,
        type VARCHAR(50),
        status VARCHAR(50)
    )
''')

# Create the txnhistory table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS txnhistory (
        acn INT,
        date TIMESTAMP,
        amount DOUBLE,
        type VARCHAR(50),
        updated_balance DOUBLE,
        FOREIGN KEY (acn) REFERENCES useraccount(acn)
    )
''')

con.commit()
con.close()

win=Tk()
win.state('zoomed')
win.title("Banking automation system")
win.config(bg="powder blue")
win.resizable(width=False, height=False)
Lbl_title=Label(win,text="Bank Automation",font=("",30,"bold","underline"),bg="powder blue")
Lbl_title.pack()
photo=PhotoImage(file="hdfc.png")
lbl_img=Label(win,image=photo)
lbl_img.place(x=0,y=0)

def home_screen():
    frm=Frame(win)
    frm.config(bg='pink')
    frm.place(x=0,y=60,relwidth=1,relheight=1)
    lbl_username=Label(frm,text="Username",font=("",20),bg="pink")
    entry_username=Entry(frm,font=("",20),bd=5)
    lbl_username.place(relx=.3,rely=.1)
    entry_username.place(relx=.42,rely=.1)
    entry_username.focus()
    lbl_passw=Label(frm,text="Password",font=("",20),bg="pink")
    entry_passw=Entry(frm,font=("",20),bd=5,show="*")
    lbl_passw.place(relx=.3,rely=.2)
    entry_passw.place(relx=.42,rely=.2)

    lbl_type=Label(frm,text="User Type",font=("",20),bg="pink")
    lbl_type.place(relx=.3,rely=.3)
    combo_type=ttk.Combobox(frm,values=["---Select user----","Customer","Admin"],font=("",20))
    combo_type.current(0)
    combo_type.place(relx=.42,rely=.3)

    login_btn=Button(frm,command=lambda:welcome_screen(entry_username,entry_passw,combo_type),text="login",font=("",'20'),bg='powder blue',bd=10)
    login_btn.place(relx=.41,rely=.45)

    reset_btn=Button(frm,command=lambda:reset_home(entry_username,entry_passw,combo_type),text="reset",font=("",'20'),bg='powder blue',bd=10)
    reset_btn.place(relx=.5,rely=.45)

    open_btn=Button(frm,command=open_screen,text="open account",font=("",'20'),bg='powder blue',bd=10)
    open_btn.place(relx=.3,rely=.55)
    
    fp_btn=Button(frm,command=fp_screen,text="forgot password",font=("",'20'),bg='powder blue',bd=10)
    fp_btn.place(relx=.5,rely=.55)

def logout():
    option= messagebox.askyesno(title='logout',message="Do you really want to logout?")
    if(option==True):
        home_screen()
    else:
        pass

def welcome_screen(entry_username,entry_passw,combo_type):
    user=entry_username.get()
    psw=entry_passw.get()
    tp=combo_type.get()
    if(tp == "---Select user----"):
        messagebox.showwarning("warning","please entry account type")
        return
    elif(tp=="Customer"):
        con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
        cur=con.cursor()
        cur.execute("SELECT name, Bal, type FROM useraccount WHERE acn = %s AND password = %s", (user, psw))
        tup=cur.fetchone()
        con.close()
        if(tup==None):
            messagebox.showwarning("warning","Invalid username/Password")
        else:
            frm=Frame(win)
            frm.config(bg='pink')
            frm.place(x=0,y=60,relwidth=1,relheight=1)

            logout_btn=Button(frm,command=logout,text="logout",font=("",'20'),bg='powder blue',bd=10)
            logout_btn.place(x=1160,y=.01)
            lbl_cu=Label(frm,text=f"Welcome ,{tup[0]}",font=("",'15'),bg='pink',fg="black",bd=10)
            lbl_cu.place(x=0,y=0)

            left_frm=Frame(frm)
            left_frm.configure(bg='pink')
            left_frm.place(x=0,y=100,relwidth=.2,relheight=.8)

            check_btn=Button(left_frm,width=12,command=lambda:checkbal_frame(),text="check balance",font=("",'20'),bg='powder blue',bd=10)
            check_btn.place(x=1,y=0)

            deposit_btn=Button(left_frm,width=12,command=lambda:deposit_frame(),text="Deposit",font=("",'20'),bg='powder blue',bd=10)
            deposit_btn.place(x=1,y=100)
    
            widraw_btn=Button(left_frm,width=12,command=lambda:withdraw_frame(),text="withdraw",font=("",'20'),bg='powder blue',bd=10)
            widraw_btn.place(x=1,y=200)

            transfer_btn=Button(left_frm,width=12,command=lambda:transfer_frame(),text="transfer",font=("",'20'),bg='powder blue',bd=10)
            transfer_btn.place(x=1,y=300)

            txnhist_btn=Button(left_frm,width=12,command=lambda:txnhistory_frame(),text="txn history",font=("",'20'),bg='powder blue',bd=10)
            txnhist_btn.place(x=1,y=400)
    else:
        if(user=="admin" and psw=="admin"):
            frm=Frame(win)
            frm.config(bg='pink')
            frm.place(x=0,y=60,relwidth=1,relheight=1)
            lbl_wel=Label(frm,text="Welcome admin:",font=("",'15'),bg='pink',bd=10,fg="black")
            lbl_wel.place(x=2,y=2)
            logout_btn=Button(frm,command=logout,text="logout",font=("",'20'),bg='powder blue',bd=10)
            logout_btn.place(x=1160,y=.01)

            view_btn=Button(frm,width=12,command=lambda:viewcustomer_frame(),text="view customer",font=("",'20'),bg='powder blue',bd=10)
            view_btn.place(x=530,y=270)
        else:
            messagebox.showerror("Invalid","Invalid username/password for admin")
            return
    def viewcustomer_frame():
        f=Frame(frm)
        f.configure(bg="pink")
        f.place(x=0,y=10,relwidth=.9,relheight=.6)
        con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
        cur=con.cursor()
        cur.execute("select name,acn,type,Bal,mob,email from useraccount")
        lbl_name=Label(f,text="Name",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_acn=Label(f,text="Acn",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_type=Label(f,text="Type",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_avbal=Label(f,text="Avl. Bal",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_mob=Label(f,text="Mob.",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_email=Label(f,text="Email",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_name.place(x=70,y=10)
        lbl_acn.place(x=250,y=10)
        lbl_type.place(x=340,y=10)
        lbl_avbal.place(x=450,y=10)
        lbl_mob.place(x=600,y=10)
        lbl_email.place(x=800,y=10)
        i=50
        for row in cur:
            Label(f,text=f"{row[0]}",font=('',12),bg='pink',fg='black').place(x=70,y=i)
            Label(f,text=f"{row[1]}",font=('',12),bg='pink',fg='black').place(x=270,y=i)
            Label(f,text=f"{row[2]}",font=('',12),bg='pink',fg='black').place(x=350,y=i)
            Label(f,text=f"{row[3]}",font=('',12),bg='pink',fg='black').place(x=470,y=i)
            Label(f,text=f"{row[4]}",font=('',12),bg='pink',fg='black').place(x=600,y=i)
            Label(f,text=f"{row[5]}",font=('',12),bg='pink',fg='black').place(x=800,y=i)
            i=i+40
        
    def checkbal_frame():
        f=Frame(frm)
        f.configure(bg="pink")
        f.place(x=250,y=50,relwidth=.6,relheight=.6)
        con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
        cur=con.cursor()
        cur.execute("select Bal from useraccount where acn=%s",(user))
        bal=cur.fetchone()[0]
        con.close()
        lbl_name=Label(f,text=f"Name:\t{tup[0]}",font=("",'20'),bg='pink',bd=10,fg="green")
        lbl_bal=Label(f,text=f"Balance:\t{bal}",font=("",'20'),bg='pink',bd=10,fg="green")
        lbl_type=Label(f,text=f"Type:\t{tup[2]}",font=("",'20'),bg='pink',bd=10,fg="green")
        lbl_name.place(x=100,y=100)
        lbl_bal.place(x=100,y=200)
        lbl_type.place(x=100,y=300)
    def deposit_frame():
        f=Frame(frm)
        f.configure(bg="pink")
        f.place(x=250,y=50,relwidth=.6,relheight=.6)
        lbl_amt=Label(f,text="Amount:",font=("",'20'),bg='pink',bd=10,fg="green")
        entry_amt=Entry(f,font=("",'20'),bd=10)
        submit_btn=Button(f,command=lambda:deposit_amt(entry_amt),text="submit",font=("",'20'),bg='powder blue',bd=10,fg="green")
        reset_btn=Button(f,command=lambda:reset_deposit(entry_amt),text="reset",font=("",'20'),bg='powder blue',bd=10,fg="green")
        lbl_amt.place(x=100,y=100)
        entry_amt.place(x=300,y=100)
        submit_btn.place(x=200,y=200)
        reset_btn.place(x=500,y=200)
    def withdraw_frame():
        f=Frame(frm)
        f.configure(bg="pink")
        f.place(x=250,y=50,relwidth=.6,relheight=.6)
        lbl_amt=Label(f,text="Amount:",font=("",'20'),bg='pink',bd=10,fg="green")
        entry_amt=Entry(f,font=("",'20'),bd=10)
        withdraw_btn=Button(f,command=lambda:widraw_amt(entry_amt),text="withdraw",font=("",'20'),bg='powder blue',bd=10,fg="green")
        reset_btn=Button(f,command=lambda:reset_withdraw(entry_amt),text="reset",font=("",'20'),bg='powder blue',bd=10,fg="green")
        lbl_amt.place(x=100,y=100)
        entry_amt.place(x=300,y=100)
        withdraw_btn.place(x=200,y=200)
        reset_btn.place(x=500,y=200)
    def transfer_frame():
        f=Frame(frm)
        f.configure(bg="pink")
        f.place(x=250,y=50,relwidth=.6,relheight=.6)
        lbl_amt=Label(f,text="Amount:",font=("",'20'),bg='pink',bd=10,fg="green")
        entry_amt=Entry(f,font=("",'20'),bd=10)
        lbl_to=Label(f,text="To Acn",font=("",'20'),bg='pink',bd=10,fg="green")
        entry_to=Entry(f,font=("",'20'),bd=10)
        withdraw_btn=Button(f,command=lambda:transfer_amt(entry_amt,entry_to),text="Transfer",font=("",'20'),bg='powder blue',bd=10,fg="green")
        reset_btn=Button(f,command=lambda:reset_transfer(entry_amt,entry_to),text="reset",font=("",'20'),bg='powder blue',bd=10,fg="green")
        lbl_amt.place(x=100,y=100)
        entry_amt.place(x=300,y=100)
        entry_amt.focus()
        lbl_to.place(x=100,y=200)
        entry_to.place(x=300,y=200)
        withdraw_btn.place(x=200,y=300)
        reset_btn.place(x=500,y=300)
    def txnhistory_frame():
        f=Frame(frm)
        f.configure(bg="pink")
        f.place(x=250,y=50,relwidth=.6,relheight=.6)
        con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
        cur=con.cursor()
        cur.execute("SELECT * FROM txnhistory WHERE acn = %s", (user,))
        lbl_date=Label(f,text="Date",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_amount=Label(f,text="Amount",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_type=Label(f,text="Type",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_updatedbal=Label(f,text="Update Bal",font=("",'15'),bg='pink',bd=10,fg="green")
        lbl_date.place(x=100,y=10)
        lbl_amount.place(x=250,y=10)
        lbl_type.place(x=400,y=10)
        lbl_updatedbal.place(x=550,y=10)
        i=50
        for row in cur.fetchall():
            date_str = row[1].strftime('%Y-%m-%d')  # Format the datetime object to a string
            Label(f, text=f"{date_str}", font=('', 12), bg='pink', fg='black').place(x=100, y=i)
            Label(f, text=f"{row[2]}", font=('', 12), bg='pink', fg='black').place(x=270, y=i)
            Label(f, text=f"{row[3]}", font=('', 12), bg='pink', fg='black').place(x=420, y=i)
            Label(f, text=f"{row[4]}", font=('', 12), bg='pink', fg='black').place(x=570, y=i)
            i = i + 40
        
    def reset_deposit(entry_amt):
        entry_amt.delete(0,END)
    def reset_withdraw(entry_amt):
        entry_amt.delete(0,END)
    def reset_transfer(entry_amt,entry_to):
        entry_amt.delete(0,END)
        entry_to.delete(0,END)
        entry_amt.focus()
    def deposit_amt(entry_amt):
        amt=int(entry_amt.get())
        dt=datetime.now()
        con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
        cur=con.cursor()
        cur.execute("SELECT Bal FROM useraccount WHERE acn = %s", (user,))
        tup=cur.fetchone()[0]
        cur.execute("UPDATE useraccount SET Bal = Bal + %s WHERE acn = %s", (amt, user))
        cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)",(user,dt,amt,'Cr.',tup+amt))
        con.commit()
        messagebox.showinfo("update",f"{amt} is depsoited")
        con.close()
    def widraw_amt(entry_amt):
        amt=int(entry_amt.get())
        dt=datetime.now()
        con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
        cur=con.cursor()
        cur.execute("select Bal from useraccount where acn=%s",(user,))
        tup=cur.fetchone()[0]
        if(amt<=tup):
            cur.execute("update useraccount set Bal=Bal-%s where acn =%s",(amt,user))
            cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)",(user,dt,amt,'Dr.',tup-amt))
            con.commit()
            messagebox.showinfo("update",f"{amt} is withdrawl")
        else:
            messagebox.showinfo("update","you do not have enough amount to withdrawl")
        con.close()
    def transfer_amt(entry_amt,entry_to):
        amt=int(entry_amt.get())
        To=entry_to.get()
        dt=datetime.now()
        con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
        cur=con.cursor()
        cur.execute("select Bal from useraccount where acn=%s",(user))
        tup=cur.fetchone()[0]
        cur.execute("update useraccount set Bal=Bal-%s where acn =%s",(amt,user))
        cur.execute("update useraccount set Bal=Bal+%s where acn =%s",(amt,To))
        cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)",(user,dt,amt,'Dr.',tup-amt))
        cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)",(To,dt,amt,'Cr.',tup+amt))
        con.commit()
        messagebox.showinfo("update",f"{amt} is transfered")
        
    if(user!="admin" and psw!="admin"):
        checkbal_frame()
    
def fp_screen():
    frm=Frame(win)
    frm.config(bg='pink')
    frm.place(x=0,y=60,relwidth=1,relheight=1)

    back_btn=Button(frm,command=home_screen,text="Back",font=("",'20'),bg='powder blue',bd=10)
    back_btn.place(x=0,y=.01)
    lbl_acn=Label(frm,text="Account no:",font=("",'20'),bg='pink',bd=10,fg="green")
    entry_acn=Entry(frm,font=("",'20'),bd=10)
    lbl_mob=Label(frm,text="Mobile:",font=("",'20'),bg='pink',bd=10,fg="green")
    entry_mob=Entry(frm,font=("",'20'),bd=10)
    recover_btn=Button(frm,command=lambda:recover_pass(entry_acn,entry_mob),text="Recover",font=("",'20'),bg='powder blue',bd=10,fg="green")
    reset_btn=Button(frm,command=lambda:reset_fp(entry_acn,entry_mob),text="Reset",font=("",'20'),bg='powder blue',bd=10,fg="green")
    lbl_acn.place(x=200,y=100)
    entry_acn.place(x=370,y=100)
    entry_acn.focus()
    lbl_mob.place(x=200,y=200)
    entry_mob.place(x=370,y=200)
    recover_btn.place(x=300,y=300)
    reset_btn.place(x=500,y=300)

def open_screen():
   

    frm=Frame(win)
    frm.config(bg='pink')
    frm.place(x=0,y=60,relwidth=1,relheight=1)

    back_btn=Button(frm,command=home_screen,text="Back",font=("",'20'),bg='powder blue',bd=10)
    back_btn.place(x=0,y=.01)
    lbl_acn=Label(frm,text="Account no:",font=("",'20'),bg='pink',bd=10,fg="green")
    entry_acn=Entry(frm,font=("",'20'),bd=10,state='disable')
    lbl_mob=Label(frm,text="Mobile:",font=("",'20'),bg='pink',bd=10,fg="green")
    entry_mob=Entry(frm,font=("",'20'),bd=10)
    lbl_email=Label(frm,text="Email:",font=("",'20'),bg='pink',bd=10,fg="green")
    entry_email=Entry(frm,font=("",'20'),bd=10)
    lbl_name=Label(frm,text="Name:",font=("",'20'),bg='pink',bd=10,fg="green")
    entry_name=Entry(frm,font=("",'20'),bd=10)
    lbl_pass=Label(frm,text="password:",font=("",'20'),bg='pink',bd=10,fg="green")
    entry_pass=Entry(frm,font=("",'20'),bd=10,show="*")
    lbl_type=Label(frm,text="Type",font=("",20),bg="pink")
    combo_type=ttk.Combobox(frm,values=["Saving","Current"],font=("",20))
    combo_type.current(0)    
    open_btn=Button(frm,command=lambda:openacn_db(entry_mob,entry_email,entry_name,entry_pass,combo_type),text="open",font=("",'20'),bg='powder blue',bd=10,fg="green")
    reset_btn=Button(frm,command=lambda:reset_open(entry_acn,entry_mob,entry_email,entry_name,entry_pass,combo_type),text="Reset",font=("",'20'),bg='powder blue',bd=10,fg="green")
    lbl_mob.place(x=200,y=100)
    entry_mob.place(x=370,y=100)
    lbl_email.place(x=200,y=180)
    entry_email.place(x=370,y=180)
    lbl_name.place(x=200,y=260)
    entry_name.place(x=370,y=260)
    lbl_pass.place(x=200,y=340)
    entry_pass.place(x=370,y=340)
    lbl_type.place(x=200,y=420)
    combo_type.place(x=370,y=420)
    open_btn.place(x=350,y=500)
    reset_btn.place(x=500,y=500)

def reset_home(entry_username,entry_passw,combo_type):
    entry_username.delete(0,END)
    entry_passw.delete(0,END)
    combo_type.current(0)
    entry_username.focus()

def reset_fp(entry_acn,entry_mob):
    entry_acn.delete(0,END)
    entry_mob.delete(0,END)
    entry_acn.focus()

def reset_open(entry_acn,entry_mob,entry_email,entry_name,entry_pass,combo_type):
    entry_acn.delete(0,END)
    entry_mob.delete(0,END)
    entry_email.delete(0,END)
    entry_name.delete(0,END)
    entry_pass.delete(0,END)
    combo_type.current(0)
    entry_acn.focus()

def openacn_db(entry_mob,entry_email,entry_name,entry_pass,combo_type):
    con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
    cur=con.cursor()
    cur.execute("select max(acn) from useraccount")
    tup=cur.fetchone()
    if tup[0] is None:
        acn = 1
    else:
        acn = tup[0] + 1
    con.close()
    mob=entry_mob.get()
    email=entry_email.get()
    name=entry_name.get()
    pwd=entry_pass.get()
    tp=combo_type.get()
    status='active'
    bal=1000
    print(pwd)
    con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
    cur=con.cursor()
    cur.execute("INSERT INTO useraccount VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (name, pwd, email, mob, acn, bal, tp, status))
    con.commit()
    con.close()
    messagebox.showinfo("Account opening",f"Your Account is opened with Acn:{acn}")
def recover_pass(entry_acn,entry_mob):
    acn=entry_acn.get()
    mob=entry_mob.get()
    con = pymysql.connect(host='localhost', user='root', password='Harshit@1234', database='bank')
    cur=con.cursor()
    cur.execute("select password from useraccount where acn=(%s) and mob=(%s)",(acn,mob))
    tup=cur.fetchone()
    if(tup==None):
        messagebox.showwarning("password","Invalid Acn/Mob")
        return
    else:
        psw=tup[0]
        messagebox.showinfo("password",f"password is {psw}")
    home_screen()
home_screen()
win.mainloop()
