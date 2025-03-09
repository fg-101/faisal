import tkinter as tk
from tkinter import messagebox, ttk
import json
import random
import os

# قائمة لتخزين الحسابات
email = []

# اسم ملف التخزين
DATA_FILE = "users.json"

# ✅ تحميل البيانات عند تشغيل التطبيق
def load_data():
    global email
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                email = json.load(file)  # تحميل البيانات من الملف
            except json.JSONDecodeError:
                email = []  # إذا كان الملف فارغًا أو معطوبًا

# ✅ حفظ البيانات في الملف عند إضافة مستخدم جديد
def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(email, file, indent=4)

def a():
    def adduser():
        respon = entry.get().strip()
        respon2 = entry2.get().strip()
        respon3 = entry3.get().strip()
        
        if not respon or not respon2 or not respon3:
            messagebox.showwarning("EMPTY!", "You have to write!")
            return
        
        # إضافة البيانات كمجموعة واحدة
        email.append({"Email": respon, "Password": respon2, "Application": respon3})
        save_data()  # حفظ البيانات مباشرة بعد الإضافة
        messagebox.showinfo("NEW TASK!", "You added a new user!")

    def back2():
        root2.destroy()
        root.deiconify()
    
    root.withdraw()
    root2 = tk.Toplevel(root)
    root2.title("إنشاء حساب جديد")
    root2.geometry("400x300")

    frame = tk.Frame(root2)
    frame.pack(pady=10)

    label2 = tk.Label(frame, text="EMAIL:", font=("Arial", 14))
    label2.pack(side=tk.LEFT, padx=5)

    entry = tk.Entry(frame, font=("Arial", 14))
    entry.pack(side=tk.LEFT, fill="x", expand=True)

    frame2 = tk.Frame(root2)
    frame2.pack(pady=10)

    label3 = tk.Label(frame2, text="Password:", font=("Arial", 14))
    label3.pack(side=tk.LEFT, padx=5)

    entry2 = tk.Entry(frame2, font=("Arial", 14))  # إخفاء كلمة المرور
    entry2.pack(side=tk.LEFT, fill="x", expand=True)
    
    frame3 = tk.Frame(root2)
    frame3.pack(pady=10)

    label4 = tk.Label(frame3, text="Application", font=("Arial", 14))
    label4.pack(side=tk.LEFT, padx=5)

    entry3 = tk.Entry(frame3, font=("Arial", 14)) 
    entry3.pack(side=tk.LEFT, fill="x", expand=True)
    
    button_add = tk.Button(root2, text="New User", font=("Arial", 12), command=adduser)
    button_add.pack(pady=15)
    
    button_back = tk.Button(root2, text="الذهاب الى الصفحة الرئيسية", font=("Arial", 12), command=back2)
    button_back.pack(pady=30)

    root2.mainloop()

# ✅ تحسين عرض البيانات عند الحفظ
def save_screen():
    root.withdraw()
    
    def openagain():
        root21.destroy()
        root.deiconify()

    root21 = tk.Toplevel(root)
    root21.title("Saved Accounts")
    
    columns = ("Email", "Password", "Application")
    tree = ttk.Treeview(root21, columns=columns, show="headings")

    # تسمية الأعمدة
    tree.heading("Email", text="Email")
    tree.heading("Password", text="Password")
    tree.heading("Application", text="Application")

    # ضبط حجم الأعمدة
    tree.column("Email", width=150, anchor="center")
    tree.column("Password", width=150, anchor="center")
    tree.column("Application", width=150, anchor="center")

    # إضافة البيانات من الملف مع تخزين ID فريد لكل عنصر
    for idx, user in enumerate(email):
        item_id = tree.insert("", "end", values=(user["Email"], user["Password"], user["Application"]))
        tree.item(item_id, tags=str(idx))  # ربط الـ ID بالمؤشر في الـ email

    tree.pack(pady=20)

    # دالة حذف المستخدم
    # دالة حذف المستخدم
    def refresh_tree():
    # حذف جميع العناصر من الـ Treeview وإعادة تعبئته من القائمة email
        for item in tree.get_children():
            tree.delete(item)
        for idx, user in enumerate(email):
            item_id = tree.insert("", "end", values=(user["Email"], user["Password"], user["Application"]))
            tree.item(item_id, tags=(str(idx),))

    def delete_user():
        selected_item = tree.selection()
        if selected_item:
            selected_item = selected_item[0]
        # الحصول على الفهرس من الـ tag قبل الحذف
            tag = tree.item(selected_item, "tags")
            if tag:
                index = int(tag[0])
                del email[index]  # حذف البيانات من القائمة
                save_data()       # حفظ التغييرات في الملف
                refresh_tree()    # إعادة تعبئة الـ Treeview لتحديث الفهارس
                messagebox.showinfo("Deleted", "User deleted successfully!")


    # دالة تعديل المستخدم
    def edit_user():
        selected_item = tree.selection()  # الحصول على العنصر المحدد
        if selected_item:
            selected_item = selected_item[0]
            # جلب البيانات الحالية
            user = tree.item(selected_item, "values")
            email_value, password_value, app_value = user
            # عرض البيانات في نافذة لتعديلها
            edit_window = tk.Toplevel(root21)
            edit_window.title("Edit User")
            
            # حقل تعديل البريد الإلكتروني
            label_email = tk.Label(edit_window, text="Email:")
            label_email.pack()
            entry_email = tk.Entry(edit_window)
            entry_email.insert(0, email_value)  # إدخال القيمة الحالية
            entry_email.pack()

            # حقل تعديل كلمة المرور
            label_password = tk.Label(edit_window, text="Password:")
            label_password.pack()
            entry_password = tk.Entry(edit_window)
            entry_password.insert(0, password_value)  # إدخال القيمة الحالية
            entry_password.pack()

            # حقل تعديل التطبيق
            label_app = tk.Label(edit_window, text="Application:")
            label_app.pack()
            entry_app = tk.Entry(edit_window)
            entry_app.insert(0, app_value)  # إدخال القيمة الحالية
            entry_app.pack()

            # زر لتحديث البيانات
            def save_edited_user():
                new_email = entry_email.get().strip()
                new_password = entry_password.get().strip()
                new_app = entry_app.get().strip()

                if not new_email or not new_password or not new_app:
                    messagebox.showwarning("Warning", "All fields are required!")
                    return

                # تحديث البيانات في القائمة
                index = int(tree.item(selected_item, "tags")[0])  # الحصول على الفهرس
                email[index] = {"Email": new_email, "Password": new_password, "Application": new_app}

                # تحديث العنصر في Treeview
                tree.item(selected_item, values=(new_email, new_password, new_app))

                save_data()  # حفظ التغييرات
                edit_window.destroy()  # إغلاق نافذة التعديل
                messagebox.showinfo("Updated", "User updated successfully!")

            # زر حفظ التعديلات
            save_button = tk.Button(edit_window, text="Save", command=save_edited_user)
            save_button.pack(pady=10)

    frame3 = tk.Frame(root21)
    frame3.pack(pady=20)

    # زر لحذف الحساب
    button_del = tk.Button(frame3, text="Delete", font=("Arial", 12), command=delete_user)
    button_del.pack(side=tk.LEFT, padx=5)

    # زر لتعديل الحساب
    button_edit = tk.Button(frame3, text="Edit", font=("Arial", 12), command=edit_user)
    button_edit.pack(side=tk.LEFT, padx=5)

    button_back = tk.Button(root21, text="Return", font=("Arial", 12), command=openagain)
    button_back.pack(pady=30)

    root21.mainloop()

def passwordstrong():
    root.withdraw()
    def a55():
        # توليد أجزاء كلمة المرور
        a1 = random.choices("123456789", k=5)
        a2 = random.choices("!@#%*()-_=+/?:;", k=5)
        a3 = random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", k=6)
        
        # دمج الأجزاء وخلطهم
        af = a1 + a2 + a3
        random.shuffle(af)
        
        return "".join(af)
    
    def show_message():
        # إنشاء كلمة مرور جديدة
        password = a55()
        
        # تحديث حقل الإدخال بكلمة المرور
        entry.delete(0, tk.END)  # مسح النص الحالي
        entry.insert(0, password)  # إدخال كلمة المرور الجديدة
    def back ():
        root.deiconify()
        root44.destroy()
    root44 = tk.Tk()
    root44.title("إنشاء كلمة مرور")
    root44.geometry("400x300")
    
    label = tk.Label(root44, text="إنشاء كلمات مرور قوية", font=("Arial", 16))
    label.pack(pady=10)
    
    # حقل الإدخال لعرض كلمة المرور
    entry = tk.Entry(root44, font=("Arial", 14))
    entry.pack(pady=10)
    
    # زر لتوليد كلمة مرور جديدة
    button = tk.Button(root44, text="إنشاء كلمة مرور جديدة", font=("Arial", 12), command=show_message)
    button.pack(pady=10)
    
    button55 = tk.Button(root44, text="الذهاب الى الصفحة الرئيسية", font=("Arial", 12), command=back)
    button55.pack(pady=30)
    
    root44.mainloop()
def exit ():
    root.destroy()

load_data()


root = tk.Tk()
root.title("الصفحة الرئيسية")
root.geometry("400x300")

label = tk.Label(root, text="تخزين كلمات الحسابات (كلمات السر والايميل)", font=("Arial", 16))
label.pack(pady=10)

button_new = tk.Button(root, text="جديد", font=("Arial", 12), command=a)
button_new.pack(pady=10)

button2 =tk.Button(root, text="كلمات سر قوية" , font=("Arial", 12), command=passwordstrong)
button2.pack(pady=15)

button_save = tk.Button(root, text="عرض الحسابات المحفوظة", font=("Arial", 12), command=save_screen)
button_save.pack(pady=15)

button_exit1=tk.Button(root, text="الخروج من التطبيق", font=("Arial", 12), command=exit)
button_exit1.pack(pady=15)
root.mainloop()
