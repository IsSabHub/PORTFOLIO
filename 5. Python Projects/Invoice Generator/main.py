import tkinter
from tkinter import ttk
from docxtpl import DocxTemplate
import datetime
from tkinter import messagebox
from ttkthemes import ThemedStyle

def clear_item():
    qty_spinbox.delete(0, tkinter.END)
    qty_spinbox.insert(0, "1")
    desc_entry.delete(0, tkinter.END)
    price_spinbox.delete(0, tkinter.END)
    price_spinbox.insert(0, "0.0")

invoice_list = []
def add_item():
    qty = int(qty_spinbox.get())
    desc = desc_entry.get()
    price = float(price_spinbox.get())
    line_total = qty*price
    invoice_item = [qty, desc, price, line_total]
    tree.insert('',0, values=invoice_item)
    clear_item()
    
    invoice_list.append(invoice_item)

def generate_customer_number(first_name, last_name):
    now = datetime.datetime.now()
    customer_number = f"{first_name[:3].upper()}{last_name[:3].upper()}-{now.strftime('%Y%m%d%H%M%S')}"
    return customer_number

def new_invoice():
    first_name_entry.delete(0, tkinter.END)
    last_name_entry.delete(0, tkinter.END)
    phone_entry.delete(0, tkinter.END)
    clear_item()
    tree.delete(*tree.get_children())
    
    invoice_list.clear()
    
def generate_invoice():
    doc = DocxTemplate("invoice_template.docx")
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    customer_number = generate_customer_number(first_name, last_name)
    subtotal = sum(item[3] for item in invoice_list) 
    salestax = 0.21
    total = subtotal*(1-salestax)
    
    doc.render({"name":f"{first_name} {last_name}", 
            "phone":phone,
            "email":email,
            "customer_number":customer_number,
            "invoice_list": invoice_list,
            "subtotal":subtotal,
            "salestax":str(salestax*100)+"%",
            "total":total})
    
    doc_name = f"{customer_number}.docx"
    doc.save(doc_name)
    
    messagebox.showinfo("Invoice Complete", "Invoice Complete")
    
    new_invoice()

window = tkinter.Tk()
window.title("Invoice Generator Form")

style = ThemedStyle(window)
style.set_theme("equilux")

frame = ttk.Frame(window)
frame.pack(padx=20, pady=10)

first_name_label = ttk.Label(frame, text="First Name")
first_name_label.grid(row=0, column=0)
last_name_label = ttk.Label(frame, text="Last Name")
last_name_label.grid(row=0, column=1)

first_name_entry = ttk.Entry(frame)
last_name_entry = ttk.Entry(frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

phone_label = ttk.Label(frame, text="Phone")
phone_label.grid(row=0, column=2)
phone_entry = ttk.Entry(frame)
phone_entry.grid(row=1, column=2)

email_label = ttk.Label(frame, text="Email")
email_label.grid(row=0, column=3)
email_entry = ttk.Entry(frame)
email_entry.grid(row=1, column=3)

qty_label = ttk.Label(frame, text="Qty")
qty_label.grid(row=2, column=0)
qty_spinbox = ttk.Spinbox(frame, from_=1, to=100)
qty_spinbox.grid(row=3, column=0)

desc_label = ttk.Label(frame, text="Description")
desc_label.grid(row=2, column=1)
desc_entry = ttk.Entry(frame)
desc_entry.grid(row=3, column=1)

price_label = ttk.Label(frame, text="Price")
price_label.grid(row=2, column=2)
price_spinbox = ttk.Spinbox(frame, from_=0.0, to=1000.0, increment=0.01)
price_spinbox.grid(row=3, column=2)

add_button = ttk.Button(frame, text="Add Item", command=add_item)
add_button.grid(row=4, column=0)

clear_button = ttk.Button(frame, text="Clear Item", command=clear_item)
clear_button.grid(row=4, column=1)

tree = ttk.Treeview(frame, columns=("Quantity", "Description", "Price", "Line Total"))
tree.heading("#0", text="ID")
tree.heading("Quantity", text="Quantity")
tree.heading("Description", text="Description")
tree.heading("Price", text="Price")
tree.heading("Line Total", text="Line Total")
tree.column("#0", width=50)
tree.column("Quantity", width=100)
tree.column("Description", width=250)
tree.column("Price", width=100)
tree.column("Line Total", width=100)
tree.grid(row=5, column=0, columnspan=3, pady=10)

generate_invoice_button = ttk.Button(frame, text="Generate Invoice", command=generate_invoice)
generate_invoice_button.grid(row=6, column=0)

new_invoice_button = ttk.Button(frame, text="New Invoice", command=new_invoice)
new_invoice_button.grid(row=6, column=1)

quit_button = ttk.Button(frame, text="Quit", command=window.quit)
quit_button.grid(row=6, column=2)

window.mainloop()