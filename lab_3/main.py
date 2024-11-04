import string

def prepare_text(text):
    """
    Prepare the plaintext for encryption by converting it to uppercase, removing non-alphabetic characters,
    and splitting it into pairs of letters.
    """
    text = ''.join(c for c in text.upper() if c in string.ascii_letters + 'ȘȚĂÎÂ')
    text = [text[i:i+2] for i in range(0, len(text), 2)]
    if len(text[-1]) == 1:
        text[-1] += 'X'
    return text

def create_cipher_matrix(key):
    """
    Construct the 6x5 cipher matrix from the given key.
    """
    key = ''.join(c for c in key.upper() if c in string.ascii_letters + 'ȘȚĂÎÂ')
    key = ''.join(dict.fromkeys(key))  # Remove duplicate letters
    alphabet = [c for c in string.ascii_uppercase + 'ȘȚĂÎÂ' if c != 'J']
    matrix = []
    for char in key + ''.join(alphabet):
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, len(matrix), 5)]

def encrypt_pair(pair, matrix):
    """
    Encrypt a pair of letters using the Playfair cipher algorithm.
    """
    row1, col1 = next((i, j) for i in range(6) for j in range(5) if matrix[i][j] == pair[0])
    row2, col2 = next((i, j) for i in range(6) for j in range(5) if matrix[i][j] == pair[1])

    if row1 == row2:
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return matrix[(row1 + 1) % 6][col1] + matrix[(row2 + 1) % 6][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]

def encrypt_message(plaintext, key):
    """
    Encrypt the plaintext using the Playfair cipher algorithm with the given key.
    """
    matrix = create_cipher_matrix(key)
    ciphertext = []
    for pair in prepare_text(plaintext):
        ciphertext.append(encrypt_pair(pair, matrix))
    return ''.join(ciphertext)

def decrypt_pair(pair, matrix):
    """
    Decrypt a pair of letters using the Playfair cipher algorithm.
    """
    row1, col1 = next((i, j) for i in range(6) for j in range(5) if matrix[i][j] == pair[0])
    row2, col2 = next((i, j) for i in range(6) for j in range(5) if matrix[i][j] == pair[1])

    if row1 == row2:
        return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:
        return matrix[(row1 - 1) % 6][col1] + matrix[(row2 - 1) % 6][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]

def decrypt_message(ciphertext, key):
    """
    Decrypt the ciphertext using the Playfair cipher algorithm with the given key.
    """
    matrix = create_cipher_matrix(key)
    plaintext = []
    for pair in [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]:
        plaintext.append(decrypt_pair(pair, matrix))
    return ''.join(plaintext).replace('X', '')

if __name__ == "__main__":
    print("Welcome to the Playfair Cipher!")

    while True:
        print("Choose an operation:")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")

        try:
            operation = int(input("Enter the number (1-3): "))
        except ValueError:
            print("Invalid input. Please try again.")
            continue

        if operation == 3:
            print("Exiting...")
            break
        elif operation in [1, 2]:
            key = input("Enter the key: ")
            if len(key) < 7:
                print("Key must be at least 7 characters long. Please try again.")
                continue

            if operation == 1:
                plaintext = input("Enter the plaintext: ")
                ciphertext = encrypt_message(plaintext, key)
                print("Ciphertext:", ciphertext)
            else:
                ciphertext = input("Enter the ciphertext: ")
                plaintext = decrypt_message(ciphertext, key)
                print("Plaintext:", plaintext)
        else:
            print("Invalid operation. Please try again.")