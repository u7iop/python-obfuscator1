import re
import random
import keyword
import marshal
from tkinter import Tk, filedialog, Button, messagebox, Entry, Label
import tkinter as tk

# Print program introduction and disclaimer
print("This program is designed to transform your Python code into a more complex and difficult-to-understand version while maintaining its functionality.")
print("Obfuscation can be useful for protecting intellectual property or for educational purposes to understand code security.")
print("Please note that while this tool can be used for legitimate purposes, it can also be misused for malicious intents.")
print("I do not endorse or support the use of this tool for unethical or illegal activities.")
print("It is the responsibility of the user to ensure that they adhere to legal and ethical standards when using this software.")
print("Proceed with caution and use responsibly.")

print("This Project was made for RowdyHacks 2024 by Team Coderunner")

# Print program logo
print("\033[95m" + """
░█████╗░░█████╗░██████╗░███████╗██████╗░██╗░░░██╗███╗░░██╗███╗░░██╗███████╗██████╗░
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██║░░░██║████╗░██║████╗░██║██╔════╝██╔══██╗
██║░░╚═╝██║░░██║██║░░██║█████╗░░██████╔╝██║░░░██║██╔██╗██║██╔██╗██║█████╗░░██████╔╝
██║░░██╗██║░░██║██║░░██║██╔══╝░░██╔══██╗██║░░░██║██║╚████║██║╚████║██╔══╝░░██╔══██╗
╚█████╔╝╚█████╔╝██████╔╝███████╗██║░░██║╚██████╔╝██║░╚███║██║░╚███║███████╗██║░░██║
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝░╚═════╝░╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
""" + "\033[0m")

def obfuscate_python_code(code):
    """
    Obfuscate the given Python code.
    """
    # this function is used to obfuscate the python code.
    string_literals = re.findall(r'(\'[^\']*\'|\"[^\"]*\")', code)
    string_literal_mapping = {}
    for literal in string_literals:
        obfuscated_literal = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(len(literal)))
        string_literal_mapping[obfuscated_literal] = literal
        code = code.replace(literal, obfuscated_literal)

    # This attempts to preserve any variables.
    variable_assignments = re.findall(r'(?<!def\s)(?<!class\s)(?<!lambda\s)(\w+)\s*=', code)
    variable_mapping = {}
    for variable in variable_assignments:
        obfuscated_variable = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(3, 8)))
        variable_mapping[obfuscated_variable] = variable
        code = re.sub(r'\b{}\b'.format(re.escape(variable)), obfuscated_variable, code)

    # This preserves any numbers so that the code can potentially work.
    numbers = re.findall(r'\b\d+\b', code)
    number_mapping = {}
    for number in numbers:
        obfuscated_number = ''.join(random.choice('0123456789') for _ in range(len(number)))
        number_mapping[obfuscated_number] = number
        code = code.replace(number, obfuscated_number)

    # This will find all the words in the code
    words = re.findall(r'\b\w+\b', code)

    # Remove Python keywords from the list of words
    words = [word for word in words if not keyword.iskeyword(word)]

    # Creates a mapping of words to obfuscated words
    obfuscated_mapping = {}
    for word in words:
        obfuscated_mapping[word] = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(3, 8)))

    # Replace original words with obfuscated ones
    obfuscated_code = code
    for word, obfuscated_word in obfuscated_mapping.items():
        obfuscated_code = obfuscated_code.replace(word, obfuscated_word)

    # Restore string literals
    for obfuscated_literal, literal in string_literal_mapping.items():
        obfuscated_code = obfuscated_code.replace(obfuscated_literal, literal)

    # Restore variable assignments
    for obfuscated_variable, variable in variable_mapping.items():
        obfuscated_code = obfuscated_code.replace(obfuscated_variable, variable)

    # Restore numbers
    for obfuscated_number, number in number_mapping.items():
        obfuscated_code = obfuscated_code.replace(obfuscated_number, number)

    return obfuscated_code


def select_file():
    """
    Select a Python file.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    file_path_entry.delete(0, 'end')
    file_path_entry.insert('end', file_path)

def obfuscate_code():
    """
    Obfuscate the selected Python code and save it to a file.
    """
    file_path = file_path_entry.get()

    if not file_path:
        messagebox.showerror("Error", "Please select a Python file.")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        python_code = file.read()

    obfuscated_python_code = obfuscate_python_code(python_code)

    obfuscated_code_bytes = marshal.dumps(obfuscated_python_code)
    obfuscated_code = f"import marshal\nexec(marshal.loads({obfuscated_code_bytes}))"

    destination_file_path = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[("Python Files", "*.py")]
    )

    if not destination_file_path:
        return

    with open(destination_file_path, 'w', encoding='utf-8') as file:
        file.write(obfuscated_code)

    messagebox.showinfo("Success", "Code obfuscated and saved successfully.")

def change_button_color(button, index=0):
    #idk this just looks cool lmao
    """
    Change the color of the given button to a random color and apply a smooth rainbow effect to the lettering. 
    """
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    random_color = colors[index % len(colors)]
    button.configure(fg=random_color)
    button.configure(font=("Arial", 15, "bold italic underline"))  
    button.after(1000, lambda: change_button_color(button, index + 1))

# Creates the main GUI
root = tk.Tk()
root.title("Coderunner Obfuscator")  # The Title of the GUI

# Create a label for the program name
label = tk.Label(root, text="Welcome to CodeRunner Obfuscator!", font=("Arial", 15))
label.pack(pady=10)

# Create a label and entry for file path
file_path_label = Label(root, text="Python File:")
file_path_label.pack()
file_path_entry = Entry(root)
file_path_entry.pack()

# Create a button to select file
select_file_button = Button(root, text="Select File", command=select_file, activebackground="green", bd=1, relief="solid")
select_file_button.pack()

# Create a button to obfuscate code
obfuscate_button = Button(root, text="Obfuscate Code", command=obfuscate_code, activebackground="blue", bd=1, relief="solid")
obfuscate_button.pack()

# Change color of the buttons =)
change_button_color(select_file_button)
change_button_color(obfuscate_button)

# Run the main loops
root.mainloop()
if __name__ == "__main__":
    root.mainloop()