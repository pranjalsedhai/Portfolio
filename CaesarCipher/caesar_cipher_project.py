"""
This program encrypts and decrypts the file or console message
based on the user requirement using Caesar Cipher.
"""

# Displays a welcome message to the user
def welcome():
    """Prints the welcome message."""
    print("Welcome to the Caesar Cipher")
    print("This program encrypts and decrypts text with the Caesar Cipher.")

# Handles user input for choosing mode and message (console mode only)
def enter_message():
    """
    Prompts the user for mode and message.
    Returns mode (e/d) and the message as uppercase text.
    """
    while True:
        mode = input("Would you like to encrypt (e) or decrypt (d): ").lower()
        if mode in ('e', 'd'):
            break
        print("Invalid Mode")

    text = input("What message would you like to encrypt or decrypt: ").upper()
    return mode, text

# Encrypts a message using Caesar Cipher
def encrypt(message, shift):
    """
    Encrypts the message using Caesar Cipher.
    Takes two parameters: message and shift.

    Returns:
    str: The encrypted message with each letter shifted by the given amount.
    """
    encrypted_text = ""
    for char in message:
        if char.isalpha():  # Only shift alphabetical characters
            encrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            encrypted_text += char  # Keep non-alphabet characters unchanged
    return encrypted_text

# Decrypts a message using Caesar Cipher
def decrypt(message, shift):
    """
    Decrypts the message using Caesar Cipher by calling encrypt
    with a negative shift.

    Parameters:
    message (str): The encrypted message.
    shift (int): The shift number used during encryption.

    Returns:
    str: The decrypted message.
    """
    return encrypt(message, -shift)


# Reads a file and encrypts or decrypts its content line by line
def process_file(filename, mode):
    """
    Processes a file for encryption or decryption.
    Takes two parameters: filename and mode (e/d).
    Returns a list of encrypted/decrypted lines. 
    """
    with open(filename, "r") as input_file:
        result = []
        for line in input_file:
            line = line.strip().upper()  # Remove whitespace and convert to uppercase
            if mode == 'e':
                result.append(encrypt(line, shift))  
            elif mode == 'd':
                result.append(decrypt(line, shift))
    return result

# Checks whether the provided file exists and is not empty
def is_file(filename):
    """
    Checks if a file exists and is not empty.

    Parameters:
    filename: The name or path of the file to check.

    Returns:
    bool: True if the file exists and is not empty, False otherwise.
    """
    try:
        with open(filename, 'r') as file:
            if file.read(1):  # Try reading one character to check if file is empty
                return True 
            else:
                return False
    except FileNotFoundError:
        return False

# Writes the processed result (encrypted/decrypted) to a file
def write_messages(result):
    """
    Writes the processed messages to results.txt.
    
    Parameters:
    result (list of str): A list of processed messages to be written.

    Returns:
    None
    """
    with open("results.txt", "w") as output_file:
        for line in result:
            output_file.write(f"{line}\n")

# Prompts user to select message source: console or file
def message_or_file():
    """
    Prompts the user for encryption/decryption mode and input type.
    
    Returns mode, message or (Nothing if reading from file), filename
    or (Nothing if input is from console).
    """
    while True:
        mode = input("Would you like to encrypt (e) or decrypt (d): ").lower()
        if mode in ('e', 'd'):
            break
        print("Invalid Mode")

    while True:
        method = input("Would you like to read from a file (f) or the console (c)? ").lower()
        if method == 'f':
            while True:
                filename = input("Enter a filename: ")
                if is_file(filename):
                    return mode, None, filename
                else:
                    print("Invalid Filename or file is empty. Please try again.")
        elif method == 'c':
            text = input("Enter your message: ").upper()
            return mode, text, None
        else:
            print("Invalid choice. Please enter 'f' or 'c'.")

# Main driver function for the Caesar Cipher program
def main():
    """
    Main function to run the Caesar Cipher program.
    """
    global shift  # Needed to use the shift variable across functions
    welcome()  # Display welcome message

    while True:
        # Ask user for mode and source of message (file or console)
        mode, text, filename = message_or_file()

        # Get shift amount from user
        while True:
            try:
                shift = int(input("What is the shift number (0-25): "))
                if 0 <= shift <= 25:
                    break
                else:
                    print("Invalid Shift. Enter a number between 0 and 25.")
            except ValueError:
                print("Invalid Character. Enter a number between 0 and 25.")

        # Process file if filename provided
        if filename:
            result = process_file(filename, mode)
            write_messages(result)
            print("Output written to results.txt")
        else:
            # Process single console message
            if mode == 'e':
                print(encrypt(text, shift))
            elif mode == 'd':
                print(decrypt(text, shift))

        # Ask if the user wants to continue
        while True:
            continue_program = input("Would you like to encrypt or decrypt another message? (y/n): ").lower()
            if continue_program == 'y':
                break
            elif continue_program == 'n':
                print("Thanks for using the program, goodbye!")
                return
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")


# Entry point for the script
if __name__ == "__main__":
    main()
