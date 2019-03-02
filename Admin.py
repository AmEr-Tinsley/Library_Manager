from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk
conn = sqlite3.connect("Bib.db")
c=conn.cursor()

def add(title_box,author_box,categ_box,window,description):
    title=title_box.get()
    author=author_box.get()
    categ = categ_box.get()
    content=description.get("1.0","end-1c")
    #print(content)
    if title=='' or author=='' or categ=='':
        messagebox.showerror("Error","Please fill all the entries ! ")
        return
    c.execute("""INSERT INTO book (titre,auteur,category,free,description) VALUES(?,?,?,?,?)""",(title,author,categ,1,str(content)))
    conn.commit()
    
    messagebox.showinfo("Success","Book added !")
    refresh(window)

def retrun_book(tree_borrow,window):
    curr = tree_borrow.focus()
    L=tree_borrow.item(curr)
    #print(L)
    c.execute("""delete From tenancy where ID_book=? and ID_student=?""",(L["values"][0],int(L["text"])))
    conn.commit()
    c.execute("""SELECT cnt from User where ID=?""",(int(L["text"]),))
    cnt=c.fetchone()
    cnt=int(cnt[0])
    c.execute("""UPDATE User set cnt=? where ID=?""",(cnt-1,int(L["text"])))
    conn.commit()
    c.execute("UPDATE book set free=? where ID=?",(1,L['values'][0]))
    conn.commit()
    refresh(window)

def refresh(window):
    window.destroy()
    admin()
def getitem(tree,btn_remove):
    curr = tree.focus()
    #print(curr)
    L=tree.item(curr)['values']
    if not L:
        return
    if L[2]=="YES":
        btn_remove.configure(state='normal')
    else:
        btn_remove.configure(state=DISABLED)
def del_item(tree,window):
    curr = tree.focus()
    L=tree.item(curr)
    #print(L)
    c.execute("""DELETE from book where auteur=? and titre=?""",(L['values'][0],L["text"]))
    conn.commit()
    #print("here")
    refresh(window)

def ban(tree_std,window):
    curr = tree_std.focus()
    L=tree_std.item(curr)
    #print(L)
    c.execute("""UPDATE USER SET banned=? where ID=?""",(1,int(L["text"])))
    conn.commit()
    refresh(window)

def admin():
    window = Tk()
    window.geometry("950x800")
    window.configure(bg="steelblue")
    window.resizable(False,False)
    window.title("Admin")
    bar = Frame(window,width=950,height=180,bg="steelblue")
    bar.place(x=0,y=0)

    title = Label(window,text="Book's title",font=('arial 12'),fg="black",bg="steelblue")
    title.place(x=0,y=50)
    author = Label(window,text="Book's author",font=('arial 12'),fg="black",bg="steelblue")
    author.place(x=0,y=90)
    category = Label(window,text="Book's category",font=('arial 12'),fg="black",bg="steelblue")
    category.place(x=0,y=130)
    description_label = Label(window,text="Book's description",font=('arial 12'),fg="black",bg="steelblue")
    description_label.place(x=280,y=10)
    description = Text(window,height=8,width=50,bg="white")
    description.place(x=280,y=40)
    description.insert(END, "No available description for this book...")

    title_box = Entry(window)
    title_box.place(x=130,y=50)
    author_box = Entry(window)
    author_box.place(x=130,y=90)
    categ_box = Entry(window)
    categ_box.place(x=130,y=130)
    
    btn_add = Button(window,width=17,text="Add",height=2,command=lambda:add(title_box,author_box,categ_box,window,description),bg="lightblue")
    btn_add.place(x=750,y=90)

    
    book_list =  Label(window,text="Books",font=('arial 10'),bg="steelblue",fg="black")
    book_list.place(x=10,y=200)
    btn_remove = Button(window,text="Remove book",state=DISABLED,width=20,bg="lightblue",command=lambda:del_item(tree,window))
    btn_remove.place(x=10,y=460)
    tree=ttk.Treeview(window,columns=("a","b","c"))
    tree.heading('#0', text='Book name')
    tree.heading('#1', text="Book's author")
    tree.heading('#2', text="Book's category")
    tree.heading('#3',text="Free")
    

    tree.column("#0", width=120)
    tree.column("#1", width=120)
    tree.column("#2", width=120)
    tree.column("#3", width=50)  
    tree.bind("<ButtonRelease-1>",lambda event: getitem(tree,btn_remove))
    tree.place(x=10,y=220)
    
        
    c.execute("""Select * from book""")
    for elem in c:
        if(elem[4]==1):
            wa="YES"
        else:
            wa="NO"
        tree.insert("", "end",text=elem[2],values=(elem[1],elem[3],wa))
   

    tree_std=ttk.Treeview(window,columns=("a","b","c"))
    tree_std.heading('#0', text='ID')
    tree_std.heading('#1', text="Name")
    tree_std.heading('#2', text="Last Name")
    tree_std.heading('#3',text="Books borrowed")

    tree_std.column("#0", width=120)
    tree_std.column("#1", width=120)
    tree_std.column("#2", width=120)
    tree_std.column("#3",width=100)
    tree_std.place(x=470,y=220)
    students_list =  Label(window,text="Students",font=('arial 10'),bg="steelblue",fg="black")
    students_list.place(x=470,y=200)
    c.execute("""Select * from User""")
    for elem in c:
        if elem[6]==1:
            continue
        tree_std.insert("", "end",text=elem[0],values=(elem[3],elem[4],elem[5]))
    btn_ban = Button(window,text="Ban user",width=20,bg="lightblue",command=lambda:ban(tree_std,window))
    btn_ban.place(x=470,y=460)


    tree_borrow=ttk.Treeview(window,columns=("a","b","c"))
    tree_borrow.heading('#0', text='ID_student')
    tree_borrow.heading('#1', text="ID_book")
    tree_borrow.heading('#2', text="Start_date")
    tree_borrow.heading('#3',text="End_date")

    tree_borrow.column("#0", width=120)
    tree_borrow.column("#1", width=120)
    tree_borrow.column("#2", width=120)
    tree_borrow.column("#3",width=100)

    tree_borrow.place(x=150,y=560)
    borrow_list =  Label(window,text="Borrow List",font=('arial 10'),bg="steelblue",fg="black")
    borrow_list.place(x=150,y=535)
    c.execute("""Select * from tenancy""")
    for elem in c:
        tree_borrow.insert("", "end",text=elem[1],values=(elem[0],elem[2],elem[3]))

    btn_return = Button(window,text="Book returned!",width=20,height=2,bg="lightblue",command=lambda:retrun_book(tree_borrow,window))
    btn_return.place(x=650,y=670)

    window.mainloop()


