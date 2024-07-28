import pyotp
import qrcode
import time
import os
import sys
import matplotlib.pyplot as plt


def generate_totp_qr_code(secret, issuer, account_name, filename):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=account_name, issuer_name=issuer)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    show_qr(img)
    write_secret_key_to_file(secret)
    
    
def show_qr(qr_img):
    plt.imshow(qr_img, cmap='gray')
    plt.axis('off')
    plt.show()    


def write_secret_key_to_file(secret):
    filename = 'secret_key.txt'
    with open(filename, 'w') as file:
        file.write(secret)


def get_secret_key_from_file():
    filename = 'secret_key.txt'
    if not os.path.exists(filename):
        print("Must produce QR code before trying to get otp")
        return None
    elif os.path.getsize(filename) == 0:
        print("Must produce QR code before trying to get otp")
        return None
    
    with open(filename, 'r') as file:
        secret = file.read()
    return secret


def generate_otp(secret):
    totp = pyotp.TOTP(secret)
    otp = totp.now()
    return otp


def main():
    command = sys.argv[1] if len(sys.argv) == 2 else print("Invalid command; nothing to run.")
    if command == "--generate-qr":
        secret = pyotp.random_base32()
        issuer = "Google email"
        account_name = "braydenedwards1205@gmail.com"
        filename = "grcode.jpg"
        generate_totp_qr_code(secret=secret, issuer=issuer, account_name=account_name, filename=filename)
        print("QR code file created")
        print(f"Secret Key: {secret}")
    elif command == "--get-otp":
        secret = get_secret_key_from_file()
        print(f"secret key used: {secret}")
        while True:
            otp = generate_otp(secret)
            print(f"OTP: {otp}")
            time.sleep(30)
        
if __name__ == "__main__":
    main()