from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import *
import requests
import geocoder
import csv
from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt


class emptyFieldsError(Exception):
    "Raised when Entry Fields are empty."
    pass
class extraValidationError(Exception):
    "Raised when fields don't match minimum requirements"
    pass

def add():
    root.withdraw()
    def back():
        win_1.destroy()
        root.deiconify()

    def save():
        try:
            if id_ent.get() and name_ent.get() and sal_ent.get():
                print("All fields filled")
                if id_ent.get().replace("-","",1).isnumeric() and name_ent.get().replace(" ","").isalpha() and sal_ent.get().replace("-","",1).replace(".","",1).isnumeric():
                    print("All Entry Data types are correct")
                    id = int(id_ent.get())
                    name = name_ent.get()
                    sal = float(sal_ent.get())
                    if isinstance(id,int) and isinstance(name,str) and isinstance(sal,float):
                        print("ID is valid int")
                        print("Name is valid str")
                        print("Salary is valid float")
                        if (id>0) and len(name)>=2 and (sal>0) and (sal>=8000):
                            print("ID is +ve and is not 0")
                            print("Length of name is greater than or equal to 2")
                            print("Salary is +ve and greater than 8000")

                            con = connect("ems.db")
                            cursor = con.cursor()
                            sq = "select exists (select * from emp where id='%d' )"
                            c = cursor.execute(sq % id)
                            data_id = c.fetchall()
                            data_id = data_id[0][0]
                            if data_id == 0:
                                sql = "insert into emp values('%d','%s','%f')"
                                cursor.execute(sql % (id,name,sal))
                                con.commit()
                                messagebox.showinfo("Success","🎊 Employee Successfully Added 🎊")
                            elif data_id == 1:
                                messagebox.showerror("Error","ID already exists!\nPlease enter unique id.")
                        else:
                            raise extraValidationError
                    else:
                        raise Exception
                else:
                    raise ValueError
            else:
                print("Some Field is Empty give error")
                raise emptyFieldsError
        except emptyFieldsError as e1:
            if len(id_ent.get())==0:
                messagebox.showerror("Error","ID cannot be empty.")
            if len(name_ent.get())==0:
                messagebox.showerror("Error","Name cannot be empty.")
            if len(sal_ent.get())==0:
                messagebox.showerror("Error","Salary cannot be empty.")
            #print("Issue: ",repr(e))
        except ValueError as e2:
            if not id_ent.get().replace("-","",1).replace(".","",1).isnumeric():
                messagebox.showerror("Error","ID cannot have alphabets or special characters.")
            if not id_ent.get().replace("-","",1).isnumeric():
                messagebox.showerror("Error","ID must be integer.")
            if not name_ent.get().isalpha():
                messagebox.showerror("Error", "Name cannot have numbers or special characters.")
            if not sal_ent.get().replace("-","",1).replace(".","",1).isnumeric():
                messagebox.showerror("Error", "Salary cannot have alphabets or special characters.")
        except extraValidationError as e3:
            if id<=0:
                messagebox.showerror("Error","ID cannot be negative or equal to 0!")
            if len(name)<2:
                messagebox.showerror("Error","Name has to be minimum 2 letters! ")
            if sal<0:
                messagebox.showerror("Error","Salary cannot be negative, it has to minimum 8000! ")
            elif 0<=sal<8000:
                messagebox.showerror("Error","Salary has to be minimum 8000.")
        except Exception as e:
            print("Issue",repr(e))
        finally:
            if con is not None:
                con.close()
            id_ent.delete(0, END)
            name_ent.delete(0, END)
            sal_ent.delete(0, END)
            id_ent.focus()

    win_1 = Tk()
    win_1.title("Add Employee")
    win_1.geometry("520x430+500+200")
    win_1.configure(bg="#ADD8E6")
    f = ("Activ Grotesk", 15, "bold")

    id_lab = Label(win_1, text="Enter ID:", font=f, bg="#ADD8E6")
    id_lab.pack(pady=5)
    id_ent = Entry(win_1, font=f)
    id_ent.pack(pady=10)

    name_lab = Label(win_1, text="Enter Name:", font=f, bg="#ADD8E6")
    name_lab.pack(pady=5)
    name_ent = Entry(win_1, font=f)
    name_ent.pack(pady=10)

    sal_lab = Label(win_1, text="Enter Salary:", font=f, bg="#ADD8E6")
    sal_lab.pack(pady=5)
    sal_ent = Entry(win_1, font=f)
    sal_ent.pack(pady=10)

    save_btn = Button(win_1, text="Save", font=f, width=10, command=save)
    save_btn.pack(pady=10)
    back_btn = Button(win_1, text="Back", font=f, width=10, command=back)
    back_btn.pack(pady=10)

    def on_closing():
        messagebox.showinfo("Close", "E.M.S is terminated.")
        win_1.destroy()
        root.destroy()

    win_1.protocol('WM_DELETE_WINDOW', on_closing)
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
    f = ("Activ Grotesk", 15, "bold")

    view_sb = Scrollbar(win_2, bd=5)
    view_sb.pack(side=RIGHT, pady=10, fill='y')

    # defining a treeview for viewing employees in tabular format.
    Emp_Table = ttk.Treeview(win_2, yscrollcommand=view_sb.set)

    # defining columns
    Emp_Table['columns'] = ('Emp_ID', 'Emp_Name', 'Salary')

    # formatting columns
    Emp_Table.column("#0", width=0, stretch=NO)
    Emp_Table.column("Emp_ID", anchor=W, width=50)
    Emp_Table.column("Emp_Name", anchor=CENTER, width=120)
    Emp_Table.column("Salary", anchor=W, width=80)

    # creating headings
    Emp_Table.heading("#0", text="", anchor=W)
    Emp_Table.heading("Emp_ID", text="Emp ID", anchor=W)
    Emp_Table.heading("Emp_Name", text="Emp Name", anchor=CENTER)
    Emp_Table.heading("Salary", text="Salary", anchor=W)

    try:
        con = connect("EMS.db")
        sql = "select * from emp order by id asc;"
        cursor = con.cursor()

        cursor.execute(sql)
        d1 = cursor.fetchall()

        i = 0
        for d in d1:
            view_id = d[0]
            view_name = d[1]
            view_sal = d[2]
            Emp_Table.insert(parent='', index='end', iid=i, text='', values=(view_id, view_name, view_sal))
            i = i + 1
        view_sb.config(command=Emp_Table.yview)
        Emp_Table.pack(pady=20)

    except Exception as e:
        con.rollback()
        messagebox.showerror("Error", e)

    back_btn = Button(win_2, text="Back", font=f, width=10, command=back)
    back_btn.pack(pady=10)

    def on_closing():
        messagebox.showinfo("Close", "E.M.S is terminated.")
        win_2.destroy()
        root.destroy()

    win_2.protocol('WM_DELETE_WINDOW', on_closing)
    win_2.mainloop()

def update():
    root.withdraw()

    def find():
        try:
            if id_ent.get():
                if id_ent.get().replace("-", "", 1).isnumeric():
                    id = int(id_ent.get())
                    if isinstance(id, int):
                        if (id > 0):
                            con = connect("ems.db")
                            cursor = con.cursor()
                            sq = "select exists (select * from emp where id='%d')"
                            c = cursor.execute(sq % (id))
                            data_id = c.fetchall()
                            data_id = data_id[0][0]
                            if data_id == 1:
                                sql = "select * from emp where id='%d'"
                                cursor.execute(sql % (id))
                                id_ent.configure(state='readonly')
                                name_ent.configure(state=NORMAL)
                                sal_ent.configure(state=NORMAL)
                                name_ent.focus()
                                data = cursor.fetchall()
                                for d in data:
                                    name_ent.insert(0,d[1])
                                    sal_ent.insert(0,str(d[2]))
                            elif data_id==0:
                                messagebox.showerror("Error","ID does not exist!")
                                id_ent.delete(0, END)
                                id_ent.focus()
                        else:
                            raise extraValidationError
                    else:
                        raise Exception
                else:
                    raise ValueError
            else:
                raise emptyFieldsError
        except emptyFieldsError as e1:
            if len(id_ent.get()) == 0:
                messagebox.showerror("Error","ID cannot be Empty!")
        except ValueError as e2:
            if not id_ent.get().replace("-","",1).replace(".","").isnumeric():
                messagebox.showerror("Error","ID cannot be alphabets or integers")
            if not id_ent.get().replace("-","",1).isnumeric():
                messagebox.showerror("Error","ID must be integer.")
        except Exception as e3:
            messagebox.showerror("Error",e3)
        except extraValidationError as e4:
            if id<=0:
                messagebox.showerror("Error","ID cannot be negative or equal to 0.")
        finally:
            pass
    def save():
        try:
            if id_ent.get():
                if name_ent.get() and sal_ent.get():
                    if name_ent.get().replace(" ","").isalpha() and sal_ent.get().replace("-","",1).replace(".","",1).isnumeric():
                        id = int(id_ent.get())
                        name = name_ent.get()
                        sal = float(sal_ent.get())
                        if isinstance(name, str) and isinstance(sal, float):
                            if len(name) >= 2 and (sal > 0) and (sal >= 8000):
                                con = connect("ems.db")
                                cursor = con.cursor()
                                sql = "UPDATE emp SET name='%s',salary='%f' WHERE id='%d'"
                                cursor.execute(sql % (name,sal,id))
                                con.commit()
                                messagebox.showinfo("Success","Employee Updated Successfully")
                            else:
                                raise extraValidationError
                        else:
                            raise Exception
                    else:
                        raise ValueError
                else:
                    raise emptyFieldsError
            else:
                raise emptyFieldsError
        except emptyFieldsError as e1:
            if len(id_ent.get()) == 0:
                messagebox.showerror("Error","Find Employee by ID first!")
            elif len(id_ent.get()) != 0:
                if len(name_ent.get()) == 0:
                    messagebox.showerror("Error","Name is empty!")
                if len(sal_ent.get()) == 0:
                    messagebox.showerror("Error", "Salary is empty!")
        except ValueError as e2:
            if not name_ent.get().isalpha():
                messagebox.showerror("Error", "Name cannot have numbers or special characters.")
            if not sal_ent.get().replace("-","",1).replace(".","",1).isnumeric():
                messagebox.showerror("Error", "Salary cannot have alphabets or special characters.")
        except extraValidationError as e4:
            if len(name_ent.get())<2:
                messagebox.showerror("Error","Name should be minimum 2 letters")
            if sal<0:
                messagebox.showerror("Error","Salary cannot be negative, it has to minimum 8000! ")
            elif 0<=sal<8000:
                messagebox.showerror("Error","Salary has to be minimum 8000.")
        except Exception as e3:
            messagebox.showerror("Error",repr(e3))


    def clear():
        id_ent.configure(state=NORMAL)
        id_ent.delete(0, END)
        name_ent.delete(0, END)
        sal_ent.delete(0, END)
        name_ent.configure(state='readonly')
        sal_ent.configure(state='readonly')
        id_ent.focus()
    def back():
        win_3.destroy()
        root.deiconify()

    win_3 = Tk()
    win_3.title("Update Employee")
    win_3.geometry("520x430+500+200")
    win_3.configure(bg="#F98B88")
    f = ("Activ Grotesk", 15, "bold")

    id_lab = Label(win_3, text="Enter ID:", font=f, bg="#F98B88")
    id_lab.pack(pady=10)
    id_ent = Entry(win_3, font=f)
    id_ent.pack(pady=10)

    find_btn = Button(win_3, text="Find", font=f, command=find)
    find_btn.pack(pady=10)
    find_btn.place(relx=0.8, rely=0.12)

    name_lab = Label(win_3, text="Enter Name:", font=f, bg="#F98B88")
    name_lab.pack(pady=10)
    name_ent = Entry(win_3, font=f,state='readonly')
    name_ent.pack(pady=10)

    sal_lab = Label(win_3, text="Enter Salary:", font=f, bg="#F98B88")
    sal_lab.pack(pady=10)
    sal_ent = Entry(win_3, font=f,state='readonly')
    sal_ent.pack(pady=10)

    save_btn = Button(win_3, text="Save", font=f, width=10, command=save)
    save_btn.pack(pady=10)
    save_btn.place(relx=0.2, rely=0.71)
    clr_btn = Button(win_3, text="Clear", font=f, width=10, command=clear)
    clr_btn.pack(pady=10)
    clr_btn.place(relx=0.55, rely=0.71)
    back_btn = Button(win_3, text="Back", font=f, width=10, command=back)
    back_btn.pack(pady=10)
    back_btn.place(relx=0.375, rely=0.85)

    def on_closing():
        messagebox.showinfo("Close", "E.M.S is terminated.")
        win_3.destroy()
        root.destroy()

    win_3.protocol('WM_DELETE_WINDOW', on_closing)
    win_3.mainloop()

def delete():
    root.withdraw()

    def remove():
        try:
            if id_ent.get():
                if id_ent.get().replace("-","",1).isnumeric():
                    id = int(id_ent.get())
                    if isinstance(id, int):
                        if (id > 0):
                            con = connect("ems.db")
                            cursor = con.cursor()
                            id = int(id_ent.get())
                            sq = "select exists (select * from emp where id='%d' )"
                            c = cursor.execute(sq % id)
                            data_id = c.fetchall()
                            data_id = data_id[0][0]
                            if data_id == 1:
                                sql = "DELETE from emp WHERE id='%d'"
                                cursor.execute(sql % id)
                                con.commit()
                                messagebox.showinfo("Success", "Record Deleted!")
                            elif data_id == 0:
                                messagebox.showerror("Error", "ID does not exist!")
                        else:
                            raise extraValidationError
                    else:
                        raise Exception
                else:
                    raise ValueError
            else:
                if len(id_ent.get())==0:
                    raise emptyFieldsError
        except emptyFieldsError as e1:
            messagebox.showerror("Error","ID is empty!")
        except ValueError as e2:
            if not id_ent.get().replace("-","",1).replace(".","",1).isnumeric():
                messagebox.showerror("Error","ID cannot have alphabets or special characters.")
            if not id_ent.get().replace("-","",1).isnumeric():
                messagebox.showerror("Error","ID must be integer.")
        except Exception as e3:
            print("Issue",e3)
        except extraValidationError as e4:
            if id<=0:
                messagebox.showerror("Error","Id cannot be negative or 0")
        finally:
            if con is not None:
                con.close()
            id_ent.delete(0, END)

    def back():
        win_4.destroy()
        root.deiconify()

    win_4 = Tk()
    win_4.title("Delete Employee")
    win_4.geometry("520x400+500+200")
    win_4.configure(bg="#89ABFA")
    f = ("Activ Grotesk", 15, "bold")

    id_lab = Label(win_4, text="Enter ID:", font=f, bg="#89ABFA")
    id_lab.pack(pady=10)
    id_ent = Entry(win_4, font=f)
    id_ent.pack(pady=10)

    del_btn = Button(win_4, text="Delete", font=f, width=10, command=remove)
    del_btn.pack(pady=10)
    back_btn = Button(win_4, text="Back", font=f, width=10, command=back)
    back_btn.pack(pady=10)

    def on_closing():
        messagebox.showinfo("Close", "E.M.S is terminated.")
        win_4.destroy()
        root.destroy()

    win_4.protocol('WM_DELETE_WINDOW', on_closing)
    win_4.mainloop()

def chart():
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        sql = "select * from emp order by salary desc LIMIT 5"
        c = cursor.execute(sql)
        data = c.fetchall()
        path = Path('top_5_emp.csv')
        if path.is_file() == True:
            os.remove(path)
            csvFile = open('top_5_emp.csv', 'w')
            writer = csv.writer(csvFile)
            writer.writerow(['ID', 'Name', 'Salary'])
            for data_list in data:
                writer.writerow(data_list)
            csvFile.close()
            datac = pd.read_csv("top_5_emp.csv")
            Name = datac["Name"]
            Salary = datac["Salary"]
            plt.figure().set_figwidth(8)
            plt.bar(Name, Salary, width=0.20, color="green")
            plt.title("Top 5 Employees")
            plt.xlabel("Employee Name")
            plt.ylabel("Salary")
            plt.show()
        else:
            csvFile = open('top_5_emp.csv', 'w')
            writer = csv.writer(csvFile)
            writer.writerow(['ID', 'Name', 'Salary'])
            for data_list in data:
                writer.writerow(data_list)
            csvFile.close()
            datac = pd.read_csv("top_5_emp.csv")
            Name = datac["Name"]
            Salary = datac["Salary"]
            plt.figure().set_figwidth(8)
            plt.bar(Name, Salary, width=0.20, color="green")
            plt.xlabel("Employee Name")
            plt.ylabel("Salary")
            plt.show()
    except Exception as e:
        messagebox.showerror("Error", e)
    finally:
        if con is not None:
            con.close()

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

# Home Page GUI
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

charts_btn = Button(root,text = 'Charts',font=f,width=10,command=chart)
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