from tkinter import Tk, Label, Entry, Button, colorchooser, messagebox, filedialog, StringVar
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import qrcode
from pyzbar.pyzbar import decode

# Code 128 character set and values
CHAR_SET = {
    ' ': (0, "11011001100"), '!': (1, "11001101100"), '"': (2, "11001100110"), '#': (3, "10010011000"),
    '$': (4, "10010001100"), '%': (5, "10001001100"), '&': (6, "10011001000"), "'": (7, "10011000100"),
    '(': (8, "10001100100"), ')': (9, "11001001000"), '*': (10, "11001000100"), '+': (11, "11000100100"),
    ',': (12, "10110011100"), '-': (13, "10011011100"), '.': (14, "10011001110"), '/': (15, "10111001100"),
    '0': (16, "10011101100"), '1': (17, "10011100110"), '2': (18, "11001110010"), '3': (19, "11001011100"),
    '4': (20, "11001001110"), '5': (21, "11011100100"), '6': (22, "11001110100"), '7': (23, "11101101110"),
    '8': (24, "11101001100"), '9': (25, "11100101100"), ':': (26, "11100100110"), ';': (27, "11101100100"),
    '<': (28, "11100110100"), '=': (29, "11100110010"), '>': (30, "11011011000"), '?': (31, "11011000110"),
    '@': (32, "11000110110"), 'A': (33, "10100011000"), 'B': (34, "10001011000"), 'C': (35, "10001000110"),
    'D': (36, "10110001000"), 'E': (37, "10001101000"), 'F': (38, "10001100010"), 'G': (39, "11010001000"),
    'H': (40, "11000101000"), 'I': (41, "11000100010"), 'J': (42, "10110111000"), 'K': (43, "10110001110"),
    'L': (44, "10001101110"), 'M': (45, "10111011000"), 'N': (46, "10111000110"), 'O': (47, "10001110110"),
    'P': (48, "11101110110"), 'Q': (49, "11010001110"), 'R': (50, "11000101110"), 'S': (51, "11011101000"),
    'T': (52, "11011100010"), 'U': (53, "11011101110"), 'V': (54, "11101011000"), 'W': (55, "11101000110"),
    'X': (56, "11100010110"), 'Y': (57, "11101101000"), 'Z': (58, "11101100010"), '[': (59, "11100011010"),
    '\\': (60, "11101111010"), ']': (61, "11001000010"), '^': (62, "11110001010"), '_': (63, "10100110000"),
    '`': (64, "10100001100"), 'a': (65, "10010110000"), 'b': (66, "10010000110"), 'c': (67, "10000101100"),
    'd': (68, "10000100110"), 'e': (69, "10110010000"), 'f': (70, "10110000100"), 'g': (71, "10011010000"),
    'h': (72, "10011000010"), 'i': (73, "10000110100"), 'j': (74, "10000110010"), 'k': (75, "11000010010"),
    'l': (76, "11001010000"), 'm': (77, "11110111010"), 'n': (78, "11000010100"), 'o': (79, "10001111010"),
    'p': (80, "10100111100"), 'q': (81, "10010111100"), 'r': (82, "10010011110"), 's': (83, "10111100100"),
    't': (84, "10011110100"), 'u': (85, "10011110010"), 'v': (86, "11110100100"), 'w': (87, "11110010100"),
    'x': (88, "11110010010"), 'y': (89, "11011011110"), 'z': (90, "11011110110"), '{': (91, "11110110110"),
    '|': (92, "10101111000"), '}': (93, "10100011110"), '~': (94, "10001011110"), '\x7f': (95, "10111101000"),
}

START_CODE_B = "11010010000"  # Start code for Code 128
STOP_CODE = "1100011101011"  # Stop code for Code 128

def calculate_checksum(data):
    """
    Calculates the checksum for Code 128.
    """
    checksum = 104
    for i, char in enumerate(data):
        checksum += CHAR_SET[char][0] * (i + 1)
    return checksum % 103

def encode_to_barcode(data):
    """
    Encodes input data into a barcode pattern using Code 128.
    """
    barcode_pattern = START_CODE_B
    for char in data:
        if char not in CHAR_SET:
            raise ValueError(f"Character '{char}' not supported in Code 128")
        barcode_pattern += CHAR_SET[char][1]
    
    # Calculate checksum
    checksum_value = calculate_checksum(data)
    for key, value in CHAR_SET.items():
        if value[0] == checksum_value:
            barcode_pattern += value[1]
            break

    barcode_pattern += STOP_CODE
    return barcode_pattern

def draw_barcode(barcode_pattern, file_name="barcode.png", bar_width=3, bar_height=100):
    """
    Draws a barcode from the binary pattern and saves it as an image.
    """
    width = len(barcode_pattern) * bar_width
    img = Image.new("RGB", (width, bar_height), "white")
    draw = ImageDraw.Draw(img)

    x = 0
    for bit in barcode_pattern:
        if bit == '1':  # Draw black bar
            draw.rectangle([x, 0, x + bar_width - 1, bar_height], fill="black")
        x += bar_width

    img.save(file_name)
    print(f"Barcode saved as {file_name}")

# QR Code Functions
def generate_qr():
    # Get user input
    data = text_input.get()
    if not data.strip():
        status_label.config(text="Error: Please enter some text or a URL.", fg="red")
        return
    
    # Get selected QR code color
    qr_color = qr_color_button["bg"]
    
    # Create a QR code object
    qr = qrcode.QRCode(
        version=2,  # Controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=20,  # Size of each box in pixels
        border=4,  # Border size (minimum is 4)
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create the image with selected QR code color
    img = qr.make_image(fill_color=qr_color, back_color="white")
    
    # Save the QR code as a .png file
    try:
        output_file = "qrcode.png"
        img.save(output_file)
        status_label.config(text=f"QR code successfully saved as {output_file}", fg="green")
    except Exception as e:
        status_label.config(text=f"Error: Failed to save QR code. {str(e)}", fg="red")
        return
    
    # Display the QR code in the UI
    img_tk = ImageTk.PhotoImage(img.resize((200, 200)))
    qr_image_label.config(image=img_tk)
    qr_image_label.image = img_tk

def choose_color():
    # Open color picker
    color = colorchooser.askcolor(title="Choose QR Code Color")
    if color[1]:  # If a color was selected
        qr_color_button.config(bg=color[1])

def create_instruction_qr():
    # Create a QR for instruction
    instructions = (
        "EnterText-ChooseColor-GenerateQR"
    )
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    qr.add_data(instructions)
    qr.make(fit=True)
    
    # Generate the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    return ImageTk.PhotoImage(img.resize((200, 200)))

# QR Scanning Function
def scan_qr():
    # Ask user to upload an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if not file_path:
        return

    # Open the image and decode QR codes
    img = Image.open(file_path)
    decoded_objects = decode(img)
    
    if decoded_objects:
        for obj in decoded_objects:
            # Extract QR code data
            qr_data = obj.data.decode("utf-8")
            scan_result.set(f"QR Code Data: {qr_data}")
    else:
        messagebox.showerror("Scan Error", "No QR code detected in the image.")

# Tkinter UI Setup
app = Tk()
app.title("Barcode and QR Code Generator")
app.geometry("400x550")
app.resizable(False, False)

# Create a notebook (tabs)
notebook = ttk.Notebook(app)

# Create the generator tab (QR Code)
generator_tab = ttk.Frame(notebook)
notebook.add(generator_tab, text="Generate QR")

# Create the barcode maker tab
barcode_tab = ttk.Frame(notebook)
notebook.add(barcode_tab, text="Barcode Maker")

# Create the scanner tab
scanner_tab = ttk.Frame(notebook)
notebook.add(scanner_tab, text="Scanner")

notebook.pack(expand=True, fill="both")

# Barcode Maker Tab UI
Label(barcode_tab, text="Enter Text to Create Barcode:").pack(pady=10)
barcode_input = Entry(barcode_tab, width=40)
barcode_input.pack(pady=5)

generate_barcode_button = Button(barcode_tab, text="Generate Barcode", command=lambda: generate_barcode(barcode_input.get()))
generate_barcode_button.pack(pady=20)

barcode_image_label = Label(barcode_tab)
barcode_image_label.pack(pady=20)

# Function to generate the barcode and display it
def generate_barcode(data):
    if not data.strip():
        messagebox.showerror("Input Error", "Please enter some text to generate the barcode.")
        return
    try:
        barcode_pattern = encode_to_barcode(data)
        print(barcode_pattern)  # Optional: Debugging line
        draw_barcode(barcode_pattern, file_name="barcode.png")
        barcode_img = Image.open("barcode.png")
        barcode_img_tk = ImageTk.PhotoImage(barcode_img.resize((400, 100)))
        barcode_image_label.config(image=barcode_img_tk)
        barcode_image_label.image = barcode_img_tk
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# QR Code Generator Tab (UI as before)
Label(generator_tab, text="Enter Text or URL:").pack(pady=10)
text_input = Entry(generator_tab, width=40)
text_input.pack(pady=5)

Label(generator_tab, text="Choose QR Code Color:").pack(pady=10)
qr_color_button = Button(generator_tab, text="Select Color", bg="lightblue", command=choose_color)
qr_color_button.pack(pady=5)

generate_button = Button(generator_tab, text="Generate QR Code", command=generate_qr)
generate_button.pack(pady=20)

qr_image_label = Label(generator_tab)
qr_image_label.pack(pady=20)

instruction_qr = create_instruction_qr()
qr_image_label.config(image=instruction_qr)
qr_image_label.image = instruction_qr

status_label = Label(generator_tab, text="")
status_label.pack(pady=10)

# QR Scanner Tab UI
Label(scanner_tab, text="Upload an Image to Scan QR Code:").pack(pady=20)
scan_button = Button(scanner_tab, text="Upload Image", command=scan_qr)
scan_button.pack(pady=10)

scan_result = StringVar()
scan_result_label = Label(scanner_tab, textvariable=scan_result, wraplength=350, justify="center")
scan_result_label.pack(pady=20)

# Start the application loop
app.mainloop()
