from tkinter import *

root = Tk()
root.title("E.M.S")
root.geometry("520x400+500+200")
root.configure(bg='#DBF9DB')

f = ("Activ Grotesk",15,"bold")

add_btn = Button(root,text = 'Add',font=f,width=10)
add_btn.pack(pady=10)
view_btn = Button(root,text = 'View',font=f,width=10)
view_btn.pack(pady=10)
update_btn = Button(root,text = 'Update',font=f,width=10)
update_btn.pack(pady=10)
del_btn = Button(root,text = 'Delete',font=f,width=10)
del_btn.pack(pady=10)
charts_btn = Button(root,text = 'Charts',font=f,width=10)
charts_btn.pack(pady=10)

frame1 = Frame(root,height=75,width=500,bg='#DBF9DB',bd=10,highlightbackground="black",highlightthickness=1,highlightcolor='black')
frame1.pack(padx=10,pady=15)
frame1.place(anchor=S,relx=0.5,rely=0.95)

loc_label = Label(frame1,text = "Location:",font=f,bg='#DBF9DB',fg="black")
loc_label.pack(padx=10,pady=10)
loc_label.place(anchor=CENTER,relx=0.2,rely=0.5)

loc_ans = Label(frame1,text = "",font=f,bg='white',fg="black")
loc_ans.pack(padx=10,pady=10)
loc_ans.place(anchor=CENTER,relx=0.4,rely=0.5)

temp_label = Label(frame1,text = "Temp:",font=f,bg='#DBF9DB',fg="black")
temp_label.pack(padx=10,pady=10)
temp_label.place(anchor=CENTER,relx=0.6,rely=0.5)

temp_ans = Label(frame1,text = "",font=f,bg='white',fg="black")
temp_ans.pack(padx=10,pady=10)
temp_ans.place(anchor=CENTER,relx=0.8,rely=0.5)

root.mainloop()