from cProfile import label
from cgitb import text
from msilib.schema import RadioButton
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from urllib.parse import DefragResult
import mysql.connector
from mysqlx import Column

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa order by nim")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
    
    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    
    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label3 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input3 = OptionMenu(dframe, input_jurusan, *options)
    input3.grid(row=2, column=1, padx=20, pady=10, sticky='w')


    #input 4
    label4 = Label(dframe, text="Jenis Kelamin").grid(row=3, column=0, sticky="w")
    jkframe = LabelFrame(dframe, text="", borderwidth=0)
    jkframe.grid(row=3, column=1, padx=20, pady=10, sticky="w")
    JK_option = [
        ("Perempuan", "Perempuan"),
        ("Laki-laki" , "Laki-laki"),
    ]
    
    jk = StringVar()
    jk.set("Perempuan")
    
    for text, value in JK_option:
        Radiobutton(jkframe, text=text, variable=jk, value=value).pack(anchor='w')
    
    
    #input 5
    label5= Label(dframe, text="Hobi").grid(row=4, column=0, sticky='w')
    hobi_option = ["Netfilxan", "Karoke", "Ceramah", "Tiktokan", "Stalking"]
    hobi_combobox = ttk.Combobox(dframe, value=hobi_option)
    hobi_combobox.grid(row=4, column=1, sticky='w')
    hobi_combobox.current(0)
    
    
    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jurusan, jk, hobi_combobox), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, jenis_kelamin, hobi):
    global mydb
    global dbcursor
    
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    jenis_kelamin = jenis_kelamin.get()
    hobi = hobi.get()
    
    #data check
    if nama == "" or nim == "" or jurusan == "" or jurusan == "" :
        alert(parent, "Data ga boleh kosong tau")
        return

    #making query
    query = "INSERT into mahasiswa (nim, nama ,jurusan, jenis_kelamin, hobi) value ('"+nim+"','"+nama+"', '"+jurusan+"','"+jenis_kelamin+"', '"+hobi+"')"
    #execute
    dbcursor.execute(query)
    mydb.commit()    
    #close database
    # mydb.close()
    
    # Input data disini
    btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_ok.pack(padx=10, pady=10)

def alert(parent, message) :
    # parent.withdraw()
    top = Toplevel()
    top.title("Warning")
    dframe = LabelFrame(top)
    dframe.pack()
    
    label_message = Label(dframe, text=message).grid(row=0, column=0)
    button_ok = Button(dframe, text="Baiklah", command=lambda: [top.destroy(), parent.deiconify()]).grid(row=1, column=0)
    
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title4 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title4 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label4 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label4 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():
    top = Toplevel()
    # Delete data disini
    query = "DELETE from mahasiswa"
    #execute
    dbcursor.execute(query)
    mydb.commit()
    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)
    # alert(root, "Hapus Berhasil")


def showImage():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Fasilitas Kampus")
    frame = LabelFrame(top, borderwidth=0, padx=10, pady=10)
    frame.pack()
    
    my_img1 = ImageTk.PhotoImage(Image.open('images/polish_cow.jpg'))
    my_img2 = ImageTk.PhotoImage(Image.open('images/chinese_tom.jpg'))
    my_img3 = ImageTk.PhotoImage(Image.open('images/pink_guy.jpg'))
    my_img4 = ImageTk.PhotoImage(Image.open('images/uh_oh.jpg'))
    my_img5 = ImageTk.PhotoImage(Image.open('images/jerma_sus.jpg'))

    image_list = [my_img1, my_img2, my_img3, my_img4, my_img5]
    number = 0
    
    my_label = Label(frame, image=my_img1)
    my_label.grid(row=0, column=0)
    
    
    buttonFrame = LabelFrame(frame, borderwidth=0)
    buttonFrame.grid(row =2, column=0, pady=15)
    
    button_back = Button(buttonFrame, text="<<", command=lambda: back(number-1, my_label, image_list, frame, buttonFrame, button_forward, button_back), state=DISABLED)
    
    button_exit = Button(buttonFrame, text="Exit Program", command=frame.quit)
    button_forward = Button(buttonFrame, text=">>", command=lambda: forward(number+1, my_label, image_list, buttonFrame, button_forward, button_back))

    button_back.grid(row=1, column=0)
    button_exit.grid(row=1, column=1)
    button_forward.grid(row=1, column=2)
    
    

    def back(image_number, my_label, image_list, buttonFrame, button_forward, button_back):

        my_label.grid_forget()
        my_label = Label(image=image_list[image_number])
        button_forward = Button(buttonFrame, text=">>", command=lambda: forward(image_number + 1, my_label, image_list, buttonFrame, button_forward, button_back))
        button_back = Button(buttonFrame, text="<<", command=lambda: back(image_number - 1, my_label, image_list, buttonFrame, button_forward, button_back))

        if image_number == 1:
            button_back = Button(buttonFrame, text="<<", state=DISABLED)

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)
        button_forward.grid(row=1, column=2)

    def forward(image_number, my_label, image_list, buttonFrame, button_forward, button_back):

        my_label.grid_forget()
        button_back.grid_forget()
        button_forward.grid_forget()
        
        my_label = Label(image=image_list[image_number])
        button_forward = Button(buttonFrame, text=">>", command=lambda: forward(image_number + 1, my_label, image_list, buttonFrame, button_forward, button_back))
        button_back = Button(buttonFrame, text="<<", command=lambda: back(image_number - 1, my_label, image_list, buttonFrame, button_forward, button_back))

        if image_number == 5:
            button_forward = Button(buttonFrame, text=">>", state=DISABLED)

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)
        button_forward.grid(row=1, column=2)
# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)


# Image shower
# b_img = Button(buttonGroup, text=" Semua Fasilitas Kampus", command=showImage(), width=30)
# b_img.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()