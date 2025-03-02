import cv2
import numpy as np

def encode_message(image_path, output_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Error: Image not found! Check the path.")
        return

    # Get user input for message and passcode
    message = input("Enter the message to hide: ")
    passcode = input("Enter a passcode for encryption: ")

    # Append passcode + message + stopping marker
    full_message = passcode + ":" + message + "#####"

    # Convert message to binary
    binary_msg = ''.join(format(ord(char), '08b') for char in full_message)

    # Store message length in 32 bits
    binary_len = format(len(binary_msg), '032b')  
    binary_data = binary_len + binary_msg  

    # Flatten image
    flat_img = img.flatten()

    # Check if message fits
    if len(binary_data) > len(flat_img):
        print(f"❌ Error: Message too large! Max capacity: {len(flat_img) // 8} characters.")
        return

    # Embed the binary data in LSB
    for i in range(len(binary_data)):
        flat_img[i] = (flat_img[i] & 0xFE) | int(binary_data[i])

    # Save modified image
    img_encoded = flat_img.reshape(img.shape)
    cv2.imwrite(output_path, img_encoded)
    print(f"✅ Message encrypted and saved as {output_path}")

# Call function
encode_message("Stenooed.jpg", "encryptedImage.png")  # Use PNG format
