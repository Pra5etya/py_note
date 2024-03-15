import requests
import tkinter as tk

def send_data_to_web(data):
    url = 'http://127.0.0.1:5000/send_data'
    payload = {'data': data}
    response = requests.post(url, data=payload)
    print(response.text)

def get_data_from_web():
    url = 'http://127.0.0.1:5000/get_data'
    response = requests.get(url)
    data = response.json()
    # Menampilkan data yang diterima dari server Flask di konsol desktop
    print("Data yang diterima dari web:", data['data'])
    return data['data']

def send_data():
    data = entry.get()
    send_data_to_web(data)

def get_data():
    data = get_data_from_web()
    label.config(text="Data dari Web: " + data)

# GUI
root = tk.Tk()
root.title("Aplikasi Desktop")
root.geometry("300x150")

label = tk.Label(root, text="")
label.pack()

entry = tk.Entry(root, width=30)
entry.pack()

send_button = tk.Button(root, text="Kirim Data ke Web", command=send_data)
send_button.pack()

get_button = tk.Button(root, text="Dapatkan Data dari Web", command=get_data)
get_button.pack()

root.mainloop()
