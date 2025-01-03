import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from config import FONT_TITLE, FONT_LABEL, FONT_ENTRY, BUTTON_PADDING, FRAME_PADDING
from xml_parser import parse_xml

def iniciar_aplicacion():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("XML to CSV Converter")
    ventana.geometry("1000x800")

    input_path = ctk.StringVar()
    output_path = ctk.StringVar()

    def select_input_folder():
        folder = filedialog.askdirectory(title="Select XML files folder")
        input_path.set(folder)

    def select_output_folder():
        folder = filedialog.askdirectory(title="Select output folder")
        output_path.set(folder)

    def process_files():
        input_folder = input_path.get()
        output_folder = output_path.get()

        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please select both input and output folders")
            return

        results_textbox.delete("1.0", "end")
        try:
            for xml_file in os.listdir(input_folder):
                if not xml_file.endswith('.xml'):
                    continue

                file_path = os.path.join(input_folder, xml_file)
                data = parse_xml(file_path)

                if not data["general"]:
                    continue

                num_pedimento = data["general"][0]["Pedimento"]
                if not num_pedimento:
                    continue

                general_csv = os.path.join(output_folder, f"{num_pedimento}_general.csv")
                with open(general_csv, "w", newline="", encoding="utf-8") as f:
                    fieldnames = data["general"][0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data["general"])

                product_csv = os.path.join(output_folder, f"{num_pedimento}_productos.csv")
                with open(product_csv, "w", newline="", encoding="utf-8") as f:
                    fieldnames = data["productos"][0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data["productos"])

                results_textbox.insert("end", f"Processed: {xml_file}\n")
                results_textbox.insert("end", f"  General CSV: {general_csv}\n")
                results_textbox.insert("end", f"  Product CSV: {product_csv}\n\n")

            messagebox.showinfo("Success", "All files processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_all():
        input_path.set("")
        output_path.set("")
        results_textbox.delete("1.0", "end")

    sidebar = ctk.CTkFrame(ventana, corner_radius=15, width=300)
    sidebar.pack(side="left", fill="y", **FRAME_PADDING)

    main_content = ctk.CTkFrame(ventana, corner_radius=15)
    main_content.pack(side="right", expand=True, fill="both", **FRAME_PADDING)

    ctk.CTkLabel(sidebar, text="Folders", font=FONT_TITLE).pack(**BUTTON_PADDING)
    ctk.CTkLabel(sidebar, text="Input Folder:", font=FONT_LABEL).pack(**BUTTON_PADDING)
    ctk.CTkEntry(sidebar, textvariable=input_path, font=FONT_ENTRY, width=250, state="readonly").pack(**BUTTON_PADDING)
    ctk.CTkButton(sidebar, text="Browse", command=select_input_folder).pack(**BUTTON_PADDING)

    ctk.CTkLabel(sidebar, text="Output Folder:", font=FONT_LABEL).pack(**BUTTON_PADDING)
    ctk.CTkEntry(sidebar, textvariable=output_path, font=FONT_ENTRY, width=250, state="readonly").pack(**BUTTON_PADDING)
    ctk.CTkButton(sidebar, text="Browse", command=select_output_folder).pack(**BUTTON_PADDING)

    ctk.CTkButton(sidebar, text="Process Files", font=FONT_LABEL, command=process_files).pack(pady=20)
    ctk.CTkButton(sidebar, text="Clear All", font=FONT_LABEL, command=clear_all).pack(pady=10)

    ctk.CTkLabel(main_content, text="Processing Results", font=FONT_TITLE).pack(**BUTTON_PADDING)
    results_textbox = ctk.CTkTextbox(main_content, font=FONT_ENTRY, width=500, height=500)
    results_textbox.pack(expand=True, fill="both", **BUTTON_PADDING)

    ventana.mainloop()
