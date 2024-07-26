import qrcode
import pyotp

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
    

def main():
    secret = pyotp.random_base32()
    issuer = "Google email"
    account_name = "braydenedwards1205@gmail.com"
    filename = "totp_qr_code.png"
    generate_totp_qr_code(secret=secret, issuer=issuer, account_name=account_name, filename=filename)
    print("QR code file created")
    print(f"Secret Key: {secret}")
    
if __name__ == "__main__":
    main()