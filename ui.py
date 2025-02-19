import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


class ImageToPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📸 Image to PDF Converter")
        self.root.geometry("700x600")
        self.root.configure(bg="#e0f7fa")

        self.images = []  # Initialize the images list

        self.label = tk.Label(
            root, text="🖼️ Select Images to Convert to PDF",
            font=("Arial", 16, "bold"), bg="#e0f7fa", fg="#00796b"
        )
        self.label.pack(pady=10)

        self.frame = tk.Frame(root, bg="#ffffff", height=250, bd=2, relief=tk.GROOVE)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(self.frame, bg="#ffffff")
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ffffff")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.button_frame = tk.Frame(root, bg="#e0f7fa")
        self.button_frame.pack(pady=15)

        self.select_button = tk.Button(
            self.button_frame, text="📂 Select Images", command=self.load_images,
            font=("Arial", 12, "bold"), bg="#00796b", fg="#ffffff", padx=10, pady=5
        )
        self.select_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(
            self.button_frame, text="💾 Save as PDF", command=self.save_pdf,
            font=("Arial", 12, "bold"), bg="#d32f2f", fg="#ffffff", padx=10, pady=5
        )
        self.save_button.pack(side=tk.LEFT, padx=10)

    def load_images(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if not file_paths:
            return

        for path in file_paths:
            image = Image.open(path)
            self.images.append((path, image))
            self.display_image(path)

    def display_image(self, path):
        img = Image.open(path)
        img.thumbnail((120, 120))
        img = ImageTk.PhotoImage(img)

        frame = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=1, relief=tk.RIDGE)
        frame.pack(fill=tk.X, padx=5, pady=2)

        move_up = tk.Button(
            frame, text="⬆", command=lambda p=path: self.move_image(p, -1), bg="#0288d1", fg="white"
        )
        move_up.pack(side=tk.LEFT, padx=5)

        move_down = tk.Button(
            frame, text="⬇", command=lambda p=path: self.move_image(p, 1), bg="#0288d1", fg="white"
        )
        move_down.pack(side=tk.LEFT, padx=5)

        label = tk.Label(frame, image=img, bg="#ffffff")
        label.image = img
        label.pack(side=tk.LEFT, padx=10)

        name_label = tk.Label(frame, text=os.path.basename(path), bg="#ffffff", font=("Arial", 10))
        name_label.pack(side=tk.LEFT, padx=5)

    def move_image(self, path, direction):
        index = next((i for i, img in enumerate(self.images) if img[0] == path), None)
        if index is not None and 0 <= index + direction < len(self.images):
            self.images[index], self.images[index + direction] = self.images[index + direction], self.images[index]
            self.refresh_display()

    def refresh_display(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for path, _ in self.images:
            self.display_image(path)

    def save_pdf(self):
        if not self.images:
            messagebox.showerror("Error", "No images selected!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF file", "*.pdf")]
        )
        if not file_path:
            return

        image_list = [img.convert("RGB") for _, img in self.images]
        image_list[0].save(file_path, save_all=True, append_images=image_list[1:])

        messagebox.showinfo("Success", "PDF saved successfully!")

