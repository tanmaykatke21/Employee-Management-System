from tkinter import *
import requests
import geocoder

# Add Employee
def add():
	root.withdraw()
	
	def back():
		win_1.destroy()
		root.deiconify()

	win_1 = Tk()
	win_1.title("Add Employee")
	win_1.geometry("520x400+500+200")
	win_1.configure(bg="#ADD8E6")
	f = ("Activ Grotesk",15,"bold")
		
	id_lab = Label(win_1,text="Enter ID:",font=f)
	id_lab.pack(pady=10)
	id_ent = Entry(win_1,font=f)
	id_ent.pack(pady=10)

	name_lab = Label(win_1,text="Enter Name:",font=f)
	name_lab.pack(pady=10)
	name_ent = Entry(win_1,font=f)
	name_ent.pack(pady=10)

	sal_lab = Label(win_1,text="Enter Salary:",font=f)
	sal_lab.pack(pady=10)	
	sal_ent = Entry(win_1,font=f)
	sal_ent.pack(pady=10)

	save_btn = Button(win_1,text="Save",font=f,width=10)
	save_btn.pack(pady=10)
	back_btn = Button(win_1,text="Back",font=f,width=10,command=back)
	back_btn.pack(pady=10)

	win_1.mainloop()

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
	view_sb.pack(pady=10)
	
	back_btn = Button(win_2,text="Back",font=f,width=10,command=back)
	back_btn.pack(pady=10)

	win_2.mainloop()

def update():
	root.withdraw()
	
	def back():
		win_3.destroy()
		root.deiconify()
	
	win_3 = Tk()
	win_3.title("Update Employee")
	win_3.geometry("520x400+500+200")
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