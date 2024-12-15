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
        self.geometry("600x500")

        self.heading_label = ctk.CTkLabel(self, text="Convert File to Markdown", font=("Arial", 20))
        self.heading_label.pack(pady=10)

        self.supported_formats_label = ctk.CTkLabel(
            self,
            text=("Supported Formats:\n"
                  "PDF (.pdf)\n"
                  "PowerPoint (.pptx)\n"
                  "Word (.docx)\n"
                  "Excel (.xlsx)\n"
                  "Images (EXIF metadata, OCR)\n"
                  "Audio (EXIF metadata, speech transcription)\n"
                  "HTML (Wikipedia, etc.)\n"
                  "Other text formats (csv, json, xml, etc.)"),
            wraplength=500,
            font=("Arial", 12),
            justify="left"
        )
        self.supported_formats_label.pack(pady=10)

        self.select_file_button = ctk.CTkButton(self, text="Select File", command=self.select_file)
        self.select_file_button.pack(pady=10)

        self.file_path_label = ctk.CTkLabel(self, text="No file selected", wraplength=500, font=("Arial", 12))
        self.file_path_label.pack(pady=10)

        self.convert_button = ctk.CTkButton(self, text="Convert to Markdown", command=self.convert_to_markdown, state="disabled")
        self.convert_button.pack(pady=10)

        self.batch_convert_button = ctk.CTkButton(self, text="Batch Convert Files", command=self.batch_convert_files)
        self.batch_convert_button.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("All Supported Files", "*.pdf *.pptx *.docx *.xlsx *.jpg *.jpeg *.png *.wav *.mp3 *.html *.csv *.json *.xml"),
                ("PDF Files", "*.pdf"),
                ("PowerPoint Files", "*.pptx"),
                ("Word Files", "*.docx"),
                ("Excel Files", "*.xlsx"),
                ("Image Files", "*.jpg *.jpeg *.png"),
                ("Audio Files", "*.wav *.mp3"),
                ("HTML Files", "*.html"),
                ("Text Files", "*.csv *.json *.xml"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            self.file_path_label.configure(text=file_path)
            self.file_path = file_path
            self.convert_button.configure(state="normal")
        else:
            self.file_path_label.configure(text="No file selected")
            self.convert_button.configure(state="disabled")

    def convert_to_markdown(self):
        try:
            markitdown = MarkItDown()

            result = markitdown.convert(self.file_path)
            markdown_content = result.text_content

            markdown_file_path = os.path.splitext(self.file_path)[0] + ".md"
            with open(markdown_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)

            messagebox.showinfo("Success", f"Markdown file saved at:\n{markdown_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def batch_convert_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[
                ("All Supported Files", "*.pdf *.pptx *.docx *.xlsx *.jpg *.jpeg *.png *.wav *.mp3 *.html *.csv *.json *.xml"),
                ("All Files", "*.*"),
            ],
        )
        if not file_paths:
            messagebox.showwarning("No Files Selected", "No files were selected for batch conversion.")
            return

        success_count = 0
        failure_count = 0

        for file_path in file_paths:
            try:
                markitdown = MarkItDown()
                result = markitdown.convert(file_path)
                markdown_content = result.text_content

                markdown_file_path = os.path.splitext(file_path)[0] + ".md"
                with open(markdown_file_path, "w", encoding="utf-8") as md_file:
                    md_file.write(markdown_content)

                success_count += 1
            except Exception as e:
                print(f"Error converting {file_path}: {e}")
                failure_count += 1

        summary = (f"Batch Conversion Complete:\n\n"
                   f"Successfully converted: {success_count} file(s)\n"
                   f"Failed conversions: {failure_count} file(s)")
        messagebox.showinfo("Batch Conversion", summary)

if __name__ == "__main__":
    app = MarkdownConverterApp()
    app.mainloop()
