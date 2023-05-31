from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import *
import requests
import geocoder

# Add Employee
def add():
	root.withdraw()
	
	def save():
		try:
			con = connect("ems.db")
			cursor = con.cursor()
			sql = "insert into emp values('%d','%s','%f')"
			id = int(id_ent.get())
			name = name_ent.get()
			x = name.replace(" ",'')
			salary = float(sal_ent.get())
			if (id>0) and (len(name) >= 2) and (salary>=8000) and (x.isalpha()): 
				cursor.execute(sql % (id,name,salary))
				con.commit()
				messagebox.showinfo("Success","Employee Added!")
			else:
				if id<=0:
					messagebox.showerror("Error","ID must be greater than 0.")
					id_ent.delete(0,END)
					id_ent.focus()
				if len(name)<2:
					messagebox.showerror("Error","Name has to be minimum 2 letters")
					name_ent.delete(0,END)
					name_ent.focus()
				if salary<8000:
					messagebox.showerror("Error","Salary has to be minimum 8000.")
					sal_ent.delete(0,END)
					sal_ent.focus()
				if x.isalpha() == False:
					messagebox.showerror("Error","Name cannot contain digits or symbols.")
					name_ent.delete(0,END)
					name_ent.focus() 

		except ValueError as ve:
			con.rollback()
			messagebox.showerror("Error","Incorrect Input type")
		finally:
			if con is not None:
				con.close()
			id_ent.delete(0,END)
			name_ent.delete(0,END)
			sal_ent.delete(0,END)
			id_ent.focus()
	
	def back():
		win_1.destroy()
		root.deiconify()

	win_1 = Tk()
	win_1.title("Add Employee")
	win_1.geometry("520x430+500+200")
	win_1.configure(bg="#ADD8E6")
	f = ("Activ Grotesk",15,"bold")
		
	id_lab = Label(win_1,text="Enter ID:",font=f,bg="#ADD8E6")
	id_lab.pack(pady=5)
	id_ent = Entry(win_1,font=f)
	id_ent.pack(pady=10)

	name_lab = Label(win_1,text="Enter Name:",font=f,bg="#ADD8E6")
	name_lab.pack(pady=5)
	name_ent = Entry(win_1,font=f)
	name_ent.pack(pady=10)

	sal_lab = Label(win_1,text="Enter Salary:",font=f,bg="#ADD8E6")
	sal_lab.pack(pady=5)	
	sal_ent = Entry(win_1,font=f)
	sal_ent.pack(pady=10)

	save_btn = Button(win_1,text="Save",font=f,width=10,command=save)
	save_btn.pack(pady=10)
	back_btn = Button(win_1,text="Back",font=f,width=10,command=back)
	back_btn.pack(pady=10)

	win_1.mainloop()

# View Employee
def view():
	root.withdraw()
	
	def back():
		win_2.destroy()
		root.deiconify()
	
	win_2 = Tk()
	win_2.title("View Employee")
	win_2.geometry("520x400+500+200")
	win_2.configure(bg="#FBE7A1")
	f = ("Activ Grotesk",15,"bold")
	
	view_sb = Scrollbar(win_2,bd=5)	
	view_sb.pack(side=RIGHT,pady=10,fill='y')

	#defining a treeview for viewing employees in tabular format.
	Emp_Table = ttk.Treeview(win_2,yscrollcommand = view_sb.set)

	#defining columns
	Emp_Table['columns'] = ('Emp_ID','Emp_Name','Salary')

	#formatting columns
	Emp_Table.column("#0",width=0,stretch=NO)
	Emp_Table.column("Emp_ID",anchor = W,width=50)
	Emp_Table.column("Emp_Name",anchor = CENTER,width=120)
	Emp_Table.column("Salary",anchor = W,width=80)

	#creating headings
	Emp_Table.heading("#0",text="",anchor=W)
	Emp_Table.heading("Emp_ID",text="Emp ID",anchor=W)
	Emp_Table.heading("Emp_Name",text="Emp Name",anchor=CENTER)	
	Emp_Table.heading("Salary",text="Salary",anchor=W)

	try:
		con = connect("EMS.db")
		sql = "select * from emp order by id asc;"
		cursor = con.cursor()

		cursor.execute(sql)
		d1 = cursor.fetchall()
		
		i=0
		for d in d1:
			view_id = d[0]
			view_name = d[1]
			view_sal = d[2]
			Emp_Table.insert(parent='',index='end',iid=i,text='',values=(view_id,view_name,view_sal))
			i = i+1
		view_sb.config(command=Emp_Table.yview)
		Emp_Table.pack(pady=20)
					
	except Exception as e:
		con.rollback()
		messagebox.showerror("Error",e)	

	back_btn = Button(win_2,text="Back",font=f,width=10,command=back)
	back_btn.pack(pady=10)

	win_2.mainloop()

# Update Employee
def update():
	root.withdraw()
	
	def back():
		win_3.destroy()
		root.deiconify()
	
	win_3 = Tk()
	win_3.title("Update Employee")
	win_3.geometry("520x430+500+200")
	win_3.configure(bg="#F98B88")
	f = ("Activ Grotesk",15,"bold")
		
	id_lab = Label(win_3,text="Enter ID:",font=f)
	id_lab.pack(pady=10)
	id_ent = Entry(win_3,font=f)
	id_ent.pack(pady=10)

	name_lab = Label(win_3,text="Enter Name:",font=f)
	name_lab.pack(pady=10)
	name_ent = Entry(win_3,font=f)
	name_ent.pack(pady=10)

	sal_lab = Label(win_3,text="Enter Salary:",font=f)
	sal_lab.pack(pady=10)	
	sal_ent = Entry(win_3,font=f)
	sal_ent.pack(pady=10)

	save_btn = Button(win_3,text="Save",font=f,width=10)
	save_btn.pack(pady=10)
	back_btn = Button(win_3,text="Back",font=f,width=10,command=back)
	back_btn.pack(pady=10)

	win_3.mainloop()

# Delete Employee
def delete():
	root.withdraw()
	

	def back():
		win_4.destroy()
		root.deiconify()
	
	win_4 = Tk()
	win_4.title("Delete Employee")
	win_4.geometry("520x400+500+200")
	win_4.configure(bg="#89ABFA")
	f = ("Activ Grotesk",15,"bold")
		
	id_lab = Label(win_4,text="Enter ID:",font=f)
	id_lab.pack(pady=10)
	id_ent = Entry(win_4,font=f)
	id_ent.pack(pady=10)

	save_btn = Button(win_4,text="Save",font=f,width=10)
	save_btn.pack(pady=10)
	back_btn = Button(win_4,text="Back",font=f,width=10,command=back)
	back_btn.pack(pady=10)

	win_4.mainloop()
	


# Location function using API
def location():
	try:
		wa = "https://ipinfo.io/"
		res = requests.get(wa)
		data = res.json()
		ct = data['city']
		return ct
	except Exception as e:
		print("Issue",e)

# Temperature function using API 
def temperature():
	g = geocoder.ip('me')
	Lat = str(g.latlng[0])
	Long = str(g.latlng[1])

	wa = "https://api.openweathermap.org/data/2.5/weather?lat="+Lat+"&lon="+Long+"&appid=d94c2df0e2c0da985f23bf31d152648b&units=metric"
	res = requests.get(wa)

	data = res.json()
	return (data['main']['temp'])
	

root = Tk()
root.title("E.M.S")
root.geometry("520x400+500+200")
root.configure(bg='#DBF9DB')

f = ("Activ Grotesk",15,"bold")


add_btn = Button(root,text = 'Add',font=f,width=10,command=add)
add_btn.pack(pady=10)

view_btn = Button(root,text = 'View',font=f,width=10,command=view)
view_btn.pack(pady=10)

update_btn = Button(root,text = 'Update',font=f,width=10,command=update)
update_btn.pack(pady=10)

del_btn = Button(root,text = 'Delete',font=f,width=10,command=delete)
del_btn.pack(pady=10)

charts_btn = Button(root,text = 'Charts',font=f,width=10)
charts_btn.pack(pady=10)


# Loc and Temp frame
frame1 = Frame(root,height=75,width=500,bg='#DBF9DB',bd=10,highlightbackground="black",highlightthickness=1,highlightcolor='black')
frame1.pack(padx=10,pady=15)
frame1.place(anchor=S,relx=0.5,rely=0.95)

loc_label = Label(frame1,text = "Location:",font=f,bg='#DBF9DB',fg="black")
loc_label.pack(padx=10,pady=10)
loc_label.place(anchor=CENTER,relx=0.2,rely=0.5)

loc_ans = Label(frame1,text = location(),font=f,bg='#DBF9DB',fg="black")
loc_ans.pack(padx=10,pady=10)
loc_ans.place(anchor=CENTER,relx=0.4,rely=0.5)

temp_label = Label(frame1,text = "Temp:",font=f,bg='#DBF9DB',fg="black")
temp_label.pack(padx=10,pady=10)
temp_label.place(anchor=CENTER,relx=0.6,rely=0.5)

temp_ans = Label(frame1,text = temperature(),font=f,bg='#DBF9DB',fg="black")
temp_ans.pack(padx=10,pady=10)
temp_ans.place(anchor=CENTER,relx=0.8,rely=0.5)

root.mainloop()