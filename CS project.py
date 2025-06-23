#Importing the required modules
import tkinter as tk
from tkinter import ttk, messagebox
import csv

# File paths for CSV files
animal_file = "animals_rescued.csv"
expense_file = "expenses.csv"
donation_file = "donations.csv"
volunteer_file = "volunteers.csv"

# Utility functions to handle CSV operations (will be used for any reading / write operation)
def read_csv(file_path, headers):
    data = []
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    return data

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

#Adding headers inside the CSV file 
animals_rescued = read_csv(animal_file, ["ID", "Name", "Age", "Rescue Date", "Status"])
expenses = read_csv(expense_file, ["ID", "Category", "Amount"])
donations = read_csv(donation_file, ["ID", "Donor", "Amount"])
volunteers = read_csv(volunteer_file, ["ID", "Name", "Age", "Role", "Contact", "Availability"])

# Function to refresh table data
def refresh_table(tree, data):
    for row in tree.get_children():
        tree.delete(row)
    for row in data[1:]:
        tree.insert("", "end", values=row)

# Function to add new data
def add_data_form(data, file_path, columns, tree):
    form_window = tk.Toplevel(root)
    form_window.title("Add New Data")
    form_window.geometry("400x400")
    form_window.configure(bg='#333333')

    tk.Label(form_window, text="Add New Data", font=("Elephant", 20), bg='#333333', fg='white').pack(pady=10)

    inputs = []
    for column in columns:
        tk.Label(form_window, text=column, bg='#333333', fg='white').pack(pady=5)
        entry = tk.Entry(form_window, width=30)
        entry.pack()
        inputs.append(entry)

    def save_data():
        new_row = []
        for entry in inputs :
            new_row.append(entry.get())
        if "" in new_row: # i.e., if the field is left empty
            messagebox.showerror("Error", "All fields are required!")
            return
        new_row[0] = str(len(data))
        data.append(new_row)
        write_csv(file_path, data)
        refresh_table(tree, data)
        messagebox.showinfo("Success", "Data added successfully!")

    tk.Button(form_window, text="Save", width=25, height=2, command=save_data, bg='#FFFFFF', font=("Consolas", 12), fg='#333333').pack(pady=20)

# Function to delete data
def delete_data_form(data, file_path, tree):
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Data")
    delete_window.geometry("400x200")
    delete_window.configure(bg='#333333')

    tk.Label(delete_window, text="Delete Data", font=("Elephant", 20), bg='#333333', fg='white').pack(pady=10)
    tk.Label(delete_window, text="Enter the ID to delete:", bg='#333333', fg='white').pack(pady=5)

    id_entry = tk.Entry(delete_window, width=30)
    id_entry.pack(pady=5)

    def delete_data():
        id_to_delete = id_entry.get()
        if not id_to_delete:
            messagebox.showerror("Error", "ID is required!")
            return

        updated_data = [data[0]]  # Start with the header row
        deleted = False
        for row in data[1:]:
            if row[0] != id_to_delete:
                updated_data.append(row)
            else:
                deleted = True

        if not deleted:
            messagebox.showerror("Error", f"No record found with ID: {id_to_delete}")
        else:
            write_csv(file_path, updated_data)
            data[:] = updated_data
            refresh_table(tree, updated_data)
            messagebox.showinfo("Success", f"Record with ID {id_to_delete} deleted!")


    tk.Button(delete_window, text="Delete", width=25, height=2, command=delete_data, bg='#FFFFFF', font=("Consolas", 12), fg='#333333').pack(pady=20)


# Function to create the main menu
def main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="NGO Management System", font=("Elephant", 30), bg='#333333', fg='white').pack(pady=20)

    tk.Button(root, text="Info about Animals Rescued", width=30, height=3, font=("Consolas", 14), command=open_animal_info, bg='#fed700', fg='#333333').pack(pady=10)

    tk.Button(root, text="Expenses", width=30, height=3, font=("Consolas", 14), command=open_expenses, bg='#fed700', fg='#333333').pack(pady=10)

    tk.Button(root, text="Donation Amount Received", width=30, height=3, font=("Consolas", 14), command=open_donations, bg='#fed700', fg='#333333').pack(pady=10)

    tk.Button(root, text="Volunteer Details", width=30, height=3, font=("Consolas", 14), command=open_volunteer_details, bg='#fed700', fg='#333333').pack(pady=10)

# Function to open a new window for data display
def create_new_window(title, data, columns, file_path):
    new_window = tk.Toplevel(root)
    new_window.title(title)
    new_window.geometry("600x400")
    new_window.configure(bg='#333333')

    tk.Label(new_window, text=title, font=("Elephant", 20), bg='#333333', fg='white').pack(pady=10)

    tree = ttk.Treeview(new_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)

    refresh_table(tree, data)
    tree.pack(pady=20)

    tk.Button(new_window, text="Add", width=25, height=2, command=lambda: add_data_form(data, file_path, columns, tree), bg='#FFFFFF', font=("Consolas", 12), fg='#333333').pack(pady=5)

    tk.Button(new_window, text="Delete", width=25, height=2, command=lambda: delete_data_form(data, file_path, tree), bg='#FFFFFF', font=("Consolas", 12), fg='#333333').pack(pady=5)
    tk.Button(new_window, text="Close", width=25, height=2, command=new_window.destroy, bg='#FFFFFF', font=("Consolas", 12), fg='#333333').pack(pady=10)

def open_animal_info():
    create_new_window("Animals Rescued", animals_rescued, ["ID", "Name", "Age", "Rescue Date", "Status"], animal_file)

def open_expenses():
    create_new_window("Expenses", expenses, ["ID", "Category", "Amount"], expense_file)

def open_donations():
    create_new_window("Donations", donations, ["ID", "Donor", "Amount"], donation_file)

def open_volunteer_details():
    create_new_window("Volunteer Details", volunteers, ["ID", "Name", "Age", "Role", "Contact", "Availability"], volunteer_file)

# Main application setup
root = tk.Tk()
root.title("NGO Management System")
root.geometry("1080x720")
root.configure(bg='#333333')

main_menu()
root.mainloop()
