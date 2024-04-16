
import os
import base64
from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import filedialog, messagebox

def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def download_image(img_data, folder):
    img_data = img_data.split(',')[1]  # جدا کردن بخش اطلاعاتی از داده‌های تصویر
    img_binary = base64.b64decode(img_data)  # رمزگشایی داده‌های باینری تصویر
    with open(os.path.join(folder, f'image_{len(os.listdir(folder)) + 1}.png'), 'wb') as file:
        file.write(img_binary)

def process_website(url):
    
    response = requests.get(url)


    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')

 
        website_template = soup.prettify()
        save_to_file('website_template.html', website_template)

    
        css_code = '\n'.join([style.get_text() for style in soup.find_all('style')])
        save_to_file('css_code.css', css_code)

  
        js_code = '\n'.join([script.get_text() for script in soup.find_all('script') if script.get('src') is None])
        save_to_file('js_code.js', js_code)

        image_folder = 'images'
        os.makedirs(image_folder, exist_ok=True)

   
        for img in soup.find_all('img'):
            img_data = img.get('src')
            if img_data and img_data.startswith('data:image'):
                download_image(img_data, image_folder)

        messagebox.showinfo("قالب   سایت", "قالب سایت با موفقیت دراورده شد وسیو شد .")
    else:
        messagebox.showerror("Error", f"Error: {response.status_code}")

def main():

    root = tk.Tk()
    root.title("قالب سایت")

    url_label = tk.Label(root, text="Enter the URL of the website:", font=("Helvetica", 14))
    url_label.pack()

    url_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
    url_entry.pack(pady=10)

    process_button = tk.Button(root, text="Process", command=lambda: process_website(url_entry.get()), font=("Helvetica", 12), bg="#4CAF50", fg="white")
    process_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
