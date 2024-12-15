import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from markitdown import MarkItDown

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MarkdownConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File to Markdown Converter")
        self.geometry("500x300")

        self.heading_label = ctk.CTkLabel(self, text="Convert File to Markdown", font=("Arial", 20))
        self.heading_label.pack(pady=20)

        self.select_file_button = ctk.CTkButton(self, text="Select File", command=self.select_file)
        self.select_file_button.pack(pady=10)

        self.file_path_label = ctk.CTkLabel(self, text="No file selected", wraplength=400, font=("Arial", 12))
        self.file_path_label.pack(pady=10)

        self.convert_button = ctk.CTkButton(self, text="Convert to Markdown", command=self.convert_to_markdown, state="disabled")
        self.convert_button.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.file_path_label.configure(text=file_path)
            self.file_path = file_path
            self.convert_button.configure(state="normal")
        else:
            self.file_path_label.configure(text="No file selected")
            self.convert_button.configure(state="disabled")

    def convert_to_markdown(self):
        try:
            with open(self.file_path, "r") as file:
                content = file.read()

            markitdown = MarkItDown()
            result = markitdown.convert(content)

            markdown_file_path = os.path.splitext(self.file_path)[0] + ".md"
            with open(markdown_file_path, "w") as md_file:
                md_file.write(result)

            messagebox.showinfo("Success", f"Markdown file saved at:\n{markdown_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    app = MarkdownConverterApp()
    app.mainloop()
