from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import datetime
conn = sqlite3.connect("Bib.db")
c=conn.cursor()
def refresh(window,username,passwd):
    window.destroy()
    student(username,passwd)
def getitem(tree,btn_borrow,description):
    curr = tree.focus()
    L=tree.item(curr)
    #print(L)
    if not L['values']:
        return
    if L['values'][2]=="YES":
        btn_borrow.configure(state='normal')
    else:
        btn_borrow.configure(state=DISABLED)
    #print(L['values'][0]+" "+L["text"])
    a=L["text"]
    b=L['values'][0]
    c.execute("""SELECT description FROM book where titre=? and auteur=?""",(b,a))
    wa=c.fetchone()
    if wa:
        wa=wa[0] 
        description.configure(state="normal")
        description.delete('1.0',END)
        description.insert(INSERT,wa)
        description.configure(state=DISABLED)
def borrow(username,passwd,tree,window):
    c.execute("""SELECT ID,cnt FROM User where login=? and mdp=?""",(username,passwd))
    wa=c.fetchone()  
    ID_user = wa[0]
    cnt = wa[1]
    curr = tree.focus()
    L=tree.item(curr)
    c.execute("""SELECT ID FROM book where auteur=? and titre=?""",(L["text"],L['values'][0])) 
    wa=c.fetchone()
    ID_book=str(wa[0])
    if(cnt == 5):
        messagebox.showerror("Error","You have reached the maximum allowed borrowing books !")
    else:
        now = datetime.datetime.now().date()
        end = now + datetime.timedelta(days=10)
        now=str(now)
        end = str(end)
        now=now[:10]
        end=end[:10]
        #print(now+" "+end)

        c.execute("""INSERT INTO tenancy (ID_book,ID_student,date_start,date_end) values(?,?,?,?)""",(ID_book,ID_user,now,end))
        c.execute("""UPDATE User SET cnt=? where ID=?""",(cnt+1,ID_user))
        c.execute("""UPDATE book SET free=? where ID=?""",(0,ID_book))
        conn.commit()
        #print(now)
    refresh(window,username,passwd)


def student(username,passwd):
    window = Tk()
    window.geometry("950x750")
    window.resizable(False,False)
    window.configure(bg="steelblue")
    window.title("Student")
    tree=ttk.Treeview(window,columns=("a","b","c"))
    tree.heading('#0', text="Book's author")
    tree.heading('#1', text="Book name")
    tree.heading('#2', text="Book's category")
    tree.heading('#3',text="Free")

    tree.column("#0", width=120)
    tree.column("#1", width=120)
    tree.column("#2", width=120)
    tree.column("#3", width=50)
    tree.place(x=15,y=200)
    btn_borrow=Button(window,text="Borrow!",width=17,bg="lightblue",state=DISABLED,command=lambda:borrow(username,passwd,tree,window))
    btn_borrow.place(x=15,y=445)
    
    bar = Frame(window,width=950,height=140,bg="lightblue")
    bar.place(x=0,y=0)
    welcome = Label(window,text="Welcome "+username+"!",font=('arial 35'),bg="lightblue",fg="black")
    welcome.place(x=350,y=15)
    books = Label(window,text="Books available",font=('arial 12'),bg="steelblue",fg="black")
    books.place(x=15,y=175)
    desc_lab = Label(window,text="Description",font=('arial 12'),bg="steelblue",fg="black")
    desc_lab.place(x=520,y=175)
    description = Text(window,height=14,width=50,bg="white",state=DISABLED)
    description.place(x=520,y=200)
    tree.bind("<ButtonRelease-1>",lambda event: getitem(tree,btn_borrow,description))

    c.execute("""Select * from book""") 
    all_books = c.fetchall()

    for elem in all_books:
        if(elem[4]==1):
            wa="YES"
        else:
            wa="NO"
        tree.insert("", "end",text=elem[1],values=(elem[2],elem[3],wa))
    
    tree_borrow=ttk.Treeview(window,columns=("a","b","c"))
    tree_borrow.heading('#0', text='Book name')
    tree_borrow.heading('#1', text="Book author")
    tree_borrow.heading('#2', text="book category")
    tree_borrow.heading('#3',text="Date to return the book back")

    tree_borrow.column("#0", width=120)
    tree_borrow.column("#1", width=120)
    tree_borrow.column("#2", width=120)
    tree_borrow.column("#3",width=220)

    tree_borrow.place(x=150,y=520)
    borrow_list =  Label(window,text="My Borrowed books",font=('arial 10'),bg="steelblue",fg="black")
    borrow_list.place(x=150,y=490)
    c.execute("""SELECT ID FROM User where login=? and mdp=?""",(username,passwd))
    wa=c.fetchone()
    ID_user = wa[0]

    c.execute("""SELECT * from tenancy""")
    all_borrowed = c.fetchall()

    all_borrowed=list(all_borrowed)


    for elem in all_borrowed:
        if elem[1]==ID_user:
           c.execute("""SELECT titre,auteur,category FROM book where ID=?""",(elem[0],))
           wa=c.fetchone()
           tree_borrow.insert("", "end",text=wa[0],values=(wa[1],wa[2],elem[3]))
    window.mainloop()


