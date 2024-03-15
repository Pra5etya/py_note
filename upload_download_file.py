import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Button, ttk
import sqlite3
import os

class UploadProgressWindow:
    def __init__(self, master, total_files):
        self.master = master
        self.master.title("Upload Progress")

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(master, variable=self.progress_var, maximum=100, mode='determinate')
        self.progress_bar.pack(fill='x', padx=10, pady=10)

        self.total_files_label = tk.Label(master, text=f"Total files: {total_files}")
        self.total_files_label.pack()

        # Menambahkan waktu tidur (sleep) selama 3 detik setelah progress bar selesai
        self.master.after(3000, self.close_window)

    def close_window(self):
        self.master.destroy()

    def update_progress(self, current_progress):
        self.progress_var.set(current_progress)
        self.master.update_idletasks()

class DownloadProgressWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Download Progress")

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(master, variable=self.progress_var, maximum=100, mode='determinate')
        self.progress_bar.pack(fill='x', padx=10, pady=10)

    def update_progress(self, current_progress):
        self.progress_var.set(current_progress)
        self.master.update_idletasks()

class ImageDatabaseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Database App")

        self.db_connection = sqlite3.connect('image_database.db')
        self.cursor = self.db_connection.cursor()
        self.create_table()

        self.upload_button = tk.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.file_list_label = tk.Label(master, text="Uploaded Files:")
        self.file_list_label.pack()

        self.file_listbox = Listbox(master, width=50)
        self.file_listbox.pack()

        self.download_button = Button(master, text="Download Selected File", command=self.download_selected_file)
        self.download_button.pack(pady=5)

        self.update_button = Button(master, text="Update Selected File", command=self.update_selected_file)
        self.update_button.pack(pady=5)

        self.delete_button = Button(master, text="Delete Selected File", command=self.delete_selected_file)
        self.delete_button.pack(pady=5)

        self.populate_file_listbox()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS images
                            (id INTEGER PRIMARY KEY,
                            filename TEXT,
                            image BLOB)''')
        self.db_connection.commit()

    def upload_image(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            total_files = len(file_paths)
            self.progress_window = tk.Toplevel(self.master)
            self.progress_window.withdraw()
            self.progress_window.protocol("WM_DELETE_WINDOW", self.cancel_upload)
            self.progress_window.deiconify()
            progress_ui = UploadProgressWindow(self.progress_window, total_files)
            self.progress_window.update()

            files_uploaded = 0
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                with open(file_path, 'rb') as f:
                    image_data = f.read()
                    self.cursor.execute("INSERT INTO images(filename, image) VALUES (?, ?)", (filename, image_data))
                    self.db_connection.commit()
                files_uploaded += 1
                progress = (files_uploaded / total_files) * 100
                progress_ui.update_progress(progress)
            messagebox.showinfo("Success", "All images uploaded successfully.")
            self.progress_window.destroy()
            self.populate_file_listbox()

    def cancel_upload(self):
        confirm = messagebox.askyesno("Cancel Upload", "Are you sure you want to cancel the upload?")
        if confirm:
            self.progress_window.destroy()

    def populate_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT filename FROM images")
        files = self.cursor.fetchall()
        if files:
            for file in files:
                self.file_listbox.insert(tk.END, file[0])

    def download_selected_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            self.download_image(selected_file)
        else:
            messagebox.showinfo("Error", "Please select a file to download.")

    def download_image(self, filename):
        self.cursor.execute("SELECT image FROM images WHERE filename=?", (filename,))
        row = self.cursor.fetchone()
        if row:
            image_data = row[0]
            file_path = filedialog.asksaveasfilename(defaultextension="", filetypes=[("All files", "*.*")], initialfile=filename)
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                messagebox.showinfo("Success", f"Image downloaded successfully as '{os.path.basename(file_path)}'.")
                self.show_download_progress()
        else:
            messagebox.showinfo("Error", "File not found in the database.")

    def show_download_progress(self):
        self.download_progress_window = tk.Toplevel(self.master)
        self.download_progress_window.withdraw()
        self.download_progress_window.deiconify()
        progress_ui = DownloadProgressWindow(self.download_progress_window)
        self.download_progress_window.update()
        progress = 0
        while progress <= 100:
            progress_ui.update_progress(progress)
            progress += 1
            self.download_progress_window.after(30)
        self.download_progress_window.after(3000, self.download_progress_window.destroy)

    def update_selected_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            file_path = filedialog.askopenfilename()
            if file_path:
                new_filename = os.path.basename(file_path)
                with open(file_path, 'rb') as f:
                    updated_image_data = f.read()
                    self.cursor.execute("UPDATE images SET filename=?, image=? WHERE filename=?", (new_filename, updated_image_data, selected_file))
                    self.db_connection.commit()
                messagebox.showinfo("Success", "Image updated successfully.")
                self.populate_file_listbox()
        else:
            messagebox.showinfo("Error", "Please select a file to update.")

    def delete_selected_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {selected_file}?")
            if confirm:
                self.cursor.execute("DELETE FROM images WHERE filename=?", (selected_file,))
                self.db_connection.commit()
                messagebox.showinfo("Success", "File deleted successfully.")
                self.populate_file_listbox()
        else:
            messagebox.showinfo("Error", "Please select a file to delete.")

def main():
    root = tk.Tk()
    app = ImageDatabaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
