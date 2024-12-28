from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox
import subprocess
import os
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def check_file_exists(path: Path) -> bool:
    return path.exists()

def format_output_text(output_text, text):
    lines = text.split('\n')
    for line in lines:
        if any(keyword in line for keyword in ["не удовлетворяет", "traceback", "Error", "Ошибка"]):
            tag = "error"
        elif "удовлетворяет" in line:
            tag = "success"
        else:
            tag = "normal"
        output_text.insert("end", line + "\n", tag)

def run_main(main_pdf_path, docx_path, combined_paths, output_text):
    # Разделение путей на HTML и PDF файлы
    html_paths = [path for path in combined_paths if path.endswith('.html')]
    additional_pdf_paths = [path for path in combined_paths if path.endswith('.pdf')]

    python_executable = ".venv\\Scripts\\python.exe" if os.name == 'nt' else ".venv/bin/python"
    args = [
        python_executable, "main.py",
        main_pdf_path,
        docx_path,
        ",".join(html_paths),
        ",".join(additional_pdf_paths)
    ]
    result = subprocess.run(args, capture_output=True, text=True)
    
    output_text.config(state='normal')
    output_text.delete(1.0, "end")
    if result.returncode == 0:
        format_output_text(output_text, "Результат:\n" + result.stdout)
    else:
        format_output_text(output_text, "Произошла ошибка:\n" + result.stderr)
    output_text.config(state='disabled')

def select_file(entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, "end")
        entry.insert(0, file_path)

def select_files(entry):
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        entry.delete(0, "end")
        entry.insert(0, ",".join(file_paths))

window = Tk()
window.geometry("862x519")
window.configure(bg = "#3A7FF6")

canvas = Canvas(
    window,
    bg = "#3A7FF6",
    height = 519,
    width = 862,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    430.9999999999999,
    0.0,
    861.9999999999999,
    519.0,
    fill="#FCFCFC",
    outline="")

entry_image_1_path = relative_to_assets("entry_1.png")
if check_file_exists(entry_image_1_path):
    entry_image_1 = PhotoImage(file=entry_image_1_path)
    entry_bg_1 = canvas.create_image(
        654.4999999999999,
        167.5,
        image=entry_image_1
    )
else:
    print(f"File not found: {entry_image_1_path}")

entry_1 = Entry(
    bd=0,
    bg="#F1F5FF",
    fg="#000716",
    highlightthickness=0
)
entry_1.insert(0, "Выбирите путь для контракта")
entry_1.place(
    x=493.9999999999999,
    y=137.0,
    width=321.0,
    height=59.0
)

button_image_1_path = relative_to_assets("button_1.png")
if check_file_exists(button_image_1_path):
    button_image_1 = PhotoImage(file=button_image_1_path)
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: select_file(entry_1),
        relief="flat"
    )
    button_1.place(
        x=786.9999999999999,
        y=157.0,
        width=24.0,
        height=22.0
    )
else:
    print(f"File not found: {button_image_1_path}")

entry_image_2_path = relative_to_assets("entry_2.png")
if check_file_exists(entry_image_2_path):
    entry_image_2 = PhotoImage(file=entry_image_2_path)
    entry_bg_2 = canvas.create_image(
        650.4999999999999,
        329.5,
        image=entry_image_2
    )
else:
    print(f"File not found: {entry_image_2_path}")

entry_2 = Entry(
    bd=0,
    bg="#F1F5FF",
    fg="#000716",
    highlightthickness=0
)
entry_2.insert(0, "Выбирите путь для приемки (PDF или HTML)")
entry_2.place(
    x=489.9999999999999,
    y=299.0,
    width=321.0,
    height=59.0
)

button_image_3_path = relative_to_assets("button_3.png")
if check_file_exists(button_image_3_path):
    button_image_3 = PhotoImage(file=button_image_3_path)
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: select_files(entry_2),
        relief="flat"
    )
    button_3.place(
        x=782.9999999999999,
        y=319.0,
        width=24.0,
        height=22.0
    )
else:
    print(f"File not found: {button_image_3_path}")

entry_image_4_path = relative_to_assets("entry_4.png")
if check_file_exists(entry_image_4_path):
    entry_image_4 = PhotoImage(file=entry_image_4_path)
    entry_bg_4 = canvas.create_image(
        650.4999999999999,
        248.5,
        image=entry_image_4
    )
else:
    print(f"File not found: {entry_image_4_path}")

entry_4 = Entry(
    bd=0,
    bg="#F1F5FF",
    fg="#000716",
    highlightthickness=0
)
entry_4.insert(0, "Выбирите путь для ТЗ")
entry_4.place(
    x=489.9999999999999,
    y=218.0,
    width=321.0,
    height=59.0
)

button_image_4_path = relative_to_assets("button_4.png")
if check_file_exists(button_image_4_path):
    button_image_4 = PhotoImage(file=button_image_4_path)
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: select_file(entry_4),
        relief="flat"
    )
    button_4.place(
        x=782.9999999999999,
        y=238.0,
        width=24.0,
        height=22.0
    )
else:
    print(f"File not found: {button_image_4_path}")

button_image_2_path = relative_to_assets("button_2.png")
if check_file_exists(button_image_2_path):
    button_image_2 = PhotoImage(file=button_image_2_path)
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: run_main(
            entry_1.get(),
            entry_4.get(),
            entry_2.get().split(','),
            output_text
        ),
        relief="flat"
    )
    button_2.place(
        x=556.9999999999999,
        y=401.0,
        width=180.0,
        height=55.0
    )
else:
    print(f"File not found: {button_image_2_path}")

output_text = Text(
    bd=0,
    bg="#F1F5FF",
    fg="#000716",
    highlightthickness=0,
    state='disabled'
)
output_text.place(
    x=30,
    y=100,
    width=350,
    height=350
)

# Добавление тегов для форматирования текста
output_text.tag_configure("header", font=("Helvetica", 16, "bold"), foreground="#333333")
output_text.tag_configure("success", font=("Helvetica", 12), foreground="green")
output_text.tag_configure("error", font=("Helvetica", 12), foreground="red")
output_text.tag_configure("normal", font=("Helvetica", 12), foreground="#000000")

canvas.create_text(
    20.999999999999886,
    28.000000000000007,
    anchor="nw",
    text="Парсер нормативных документов",
    fill="#FCFCFC",
    font=("Roboto Bold", 24 * -1)
)

canvas.create_text(
    481.9999999999999,
    74.0,
    anchor="nw",
    text="Выбирите файлы",
    fill="#505485",
    font=("Roboto Bold", 24 * -1)
)

canvas.create_rectangle(
    20.999999999999886,
    63.00000000000001,
    80.99999999999989,
    68.0,
    fill="#FCFCFC",
    outline="")

canvas.create_text(
    28.999999999999886,
    78.0,
    anchor="nw",
    text="Вывод программы:",
    fill="#FCFCFC",
    font=("Roboto Regular", 16 * -1)
)

window.resizable(False, False)
window.mainloop()
