import cv2
import numpy as np

def decode_message(image_path):
    # Load encrypted image
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Error: Image not found! Check the path.")
        return

    flat_img = img.flatten()

    # Read 32-bit message length
    binary_len = ''.join(str(flat_img[i] & 1) for i in range(32))
    try:
        msg_length = int(binary_len, 2)
    except ValueError:
        print("❌ Error: Corrupt message length!")
        return

    # Validate length
    if msg_length > len(flat_img) - 32 or msg_length <= 0:
        print("❌ Error: Invalid message length detected. Possible corruption.")
        return

    # Extract hidden message bits
    binary_msg = ''.join(str(flat_img[i] & 1) for i in range(32, 32 + msg_length))

    # Convert binary to text
    decoded_chars = [chr(int(binary_msg[i:i+8], 2)) for i in range(0, len(binary_msg), 8)]
    decoded_msg = ''.join(decoded_chars)

    # Stop at termination marker
    if "#####" in decoded_msg:
        decoded_msg = decoded_msg.split("#####")[0]

    # Extract passcode and message
    if ":" not in decoded_msg:
        print("❌ Error: No valid passcode found in message!")
        return

    stored_passcode, secret_message = decoded_msg.split(":", 1)

    # Ask user for passcode
    entered_passcode = input("Enter passcode for decryption: ")

    if entered_passcode == stored_passcode:
        print(f"✅ Decrypted message: {secret_message}")
    else:
        print("❌ Incorrect passcode! Decryption failed.")

# Call function
decode_message("encryptedImage.png")  # Use PNG format
