
---
# Code 128 Barcode Generator

This Python program generates a **Code 128** barcode for a given string of text. Code 128 is a high-density linear barcode symbology that can encode the entire ASCII character set.

## Features

- Encodes any ASCII text into a **Code 128** barcode.
- Generates a visual barcode image (PNG format).
- Includes checksum calculation and barcode encoding based on Code 128 standards.

## How It Works

### Steps:
1. **Input Text**: The user inputs a string of text that they want to encode into a barcode.
2. **Barcode Encoding**: The program encodes the text into a binary barcode pattern based on the Code 128 standard.
3. **Checksum Calculation**: A checksum is calculated to ensure the barcode's integrity.
4. **Barcode Image Generation**: The binary barcode pattern is drawn as a PNG image.

### Barcode Components:
- **Start Code**: The starting point of the barcode (Code B in this case).
- **Data Characters**: Each character in the input text is encoded into a binary pattern.
- **Checksum**: A calculated value that helps verify the accuracy of the barcode.
- **Stop Code**: The end of the barcode pattern.

## Installation

This program requires the **Pillow** library for image manipulation. You can install it using `pip`:

```bash
pip install pillow
```

## Usage

1. **Run the Program**: Execute the Python script to run the barcode generation.
   
   ```bash
   python barcode_generator.py
   ```

2. **Enter Text**: When prompted, enter the text that you wish to encode as a barcode.

3. **Output**: The barcode will be generated and saved as a PNG image in the same directory.

   Example:

   ```plaintext
   Enter text to encode as a barcode: HelloWorld
   Barcode saved as barcode.png
   ```

## Example Output

For the input **"HelloWorld"**, the barcode image will be saved as **barcode.png**. You can scan this barcode with a barcode scanner or print it for use.

## Code Structure

- **CHAR_SET**: A dictionary that maps each character to its corresponding barcode pattern.
- **calculate_checksum(data)**: Calculates the checksum based on Code 128 encoding rules.
- **encode_to_barcode(data)**: Encodes the input data into a binary barcode pattern.
- **draw_barcode(barcode_pattern, file_name="barcode.png")**: Draws the barcode image from the encoded pattern and saves it as a PNG file.

## Customization

- **Bar Width and Height**: You can customize the appearance of the barcode by adjusting the `bar_width` and `bar_height` parameters in the `draw_barcode` function.

## Error Handling

- The program checks if any character in the input string is not supported by Code 128 and raises an error.
  
  Example:

  ```plaintext
  Error: Character 'x' not supported in Code 128
  ```

## License

This project is open-source and available under the [MIT License](LICENSE).

---