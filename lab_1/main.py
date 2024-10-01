"""
Caesar Cipher Lab Tasks
Task 1.1
Implement the Caesar algorithm for the English alphabet in one of the programming languages. Use only the letter encodings as shown in Table 1 (encodings specified in the programming language, e.g. ASCII or Unicode, are not allowed to be used). Key values shall be between 1 and 25 inclusive and no other values are allowed. Text character values shall be between 'A' and 'Z', 'a' and 'z' and no other values are prefixed. If the user enters other values - the user will be prompted for the correct slide. Before encryption the text will be converted to upper case and spaces will be removed. The user will be able to choose the operation - encryption or decryption, enter the key, message or cryptogram and get the cryptogram or decrypted message respectively.
Task 1.2
Implement the Caesar algorithm with 2 keys, preserving the conditions expressed in Task 1.1. In addition, key 2 must contain only letters of the Latin alphabet, and have a length of not less than 7.
"""

def encrypt_default(text, shift):
    """Encrypt the text using the default Caesar cipher."""
    return ''.join(chr((ord(char) - ord('A') + shift) % 26 + ord('A')) for char in text.upper() if char.isalpha())


def decrypt_default(text, shift):    
    """Decrypt the text using the default Caesar cipher."""
    return encrypt_default(text, -shift)


def get_valid_keyword():
    """Get a valid keyword from the user (at least 7 letters)."""
    while True:
        keyword = input("Enter the keyword (at least 7 letters): ")
        if keyword.isalpha() and len(keyword) >= 7:
            return keyword
        else:
            print("Keyword must contain only letters and be at least 7 characters long.")


def get_valid_shift():
    """Get a valid shift value from the user (between 1 and 25)."""
    while True:
        try:
            shift = int(input("Enter the shift value (1-25): "))
            if 1 <= shift <= 25:
                return shift
            else:
                print("Shift must be between 1 and 25.")
        except ValueError:
            print("Please enter a valid integer.")


def get_valid_text():
    """Get valid text from the user (only letters and spaces allowed)."""
    while True:
        text = input("Enter the text (letters and spaces only): ")
        if all(char.isalpha() or char.isspace() for char in text):
            return (''.join(char for char in text if char.isalpha())).lower()
        else:
            print("Text must contain only letters and spaces.")


def generate_alphabet(keyword):
    """Generate a new alphabet based on the keyword."""
    keyword = ''.join(dict.fromkeys(keyword.upper()))  # Remove duplicates
    remaining_letters = [chr(i) for i in range(ord('A'), ord('Z')+1) if chr(i) not in keyword]
    return keyword + ''.join(remaining_letters)


def encrypt_with_key(text, keyword, shift):
    """Encrypt the text using the Caesar cipher with a keyword."""
    alphabet = generate_alphabet(keyword)
    print(f"The generated alphabet is: {alphabet}")
    return ''.join(alphabet[(alphabet.index(char) + shift) % 26] for char in text.upper() if char.isalpha())


def decrypt_with_key(text, keyword, shift):
    """Decrypt the text using the Caesar cipher with a keyword."""
    alphabet = generate_alphabet(keyword)
    return ''.join(alphabet[(alphabet.index(char) - shift) % 26] for char in text.upper() if char.isalpha())


def task_1():
    """Basic Caesat Cipher Implementation"""
    print("Caesar Cipher Implementation")
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose from the available options: ")

    text = get_valid_text()
    shift = get_valid_shift()

    if choice == '1':
        encrypted_text = encrypt_default(text, shift)
        print(f"Encrypted text: {encrypted_text}")
    elif choice == '2':
        decrypted_text = decrypt_default(text, shift)
        print(f"Decrypted text: {decrypted_text}")
    else:
        print("Invalid choice. Please choose from the available options")
    

def task_2():
    """Caesar Cipher with key Implementation"""
    print("Caesar Cipher with key implementation")
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose from the available options: ")

    keyword = get_valid_keyword()
    text = get_valid_text()
    shift = get_valid_shift()

    if choice == '1':
        encrypted_text = encrypt_with_key(text, keyword, shift)
        print(f"Encrypted text: {encrypted_text}")
    elif choice == '2':
        decrypted_text = decrypt_with_key(text, keyword, shift)
        print(f"Decrypted text: {decrypted_text}")
    else:
        print("Invalid choice. Please choose from the available options")


def main():
    while True:
        print("Caesar Cipher Implementation")
        print("1. Basic Caesar Cipher (Task 1)")
        print("2. Enhanced Caesar Cipher (Task 2)")
        print("3. Exit")

        choice = input("Choose from the available options: ")

        if choice == '1':
            task_1()
            print("--------------------------------")
        elif choice == '2':
            task_2()
            print("--------------------------------")
        elif choice == '3':
            print("Exiting the program")
            print("--------------------------------")
            break
        else:
            print("Invalid choice. Please choose from the available options")
            print("--------------------------------")

if __name__=='__main__':
    main()