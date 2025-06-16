import base64

HEX_STRING = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

def convert_hex_b64(hex_string):
    data = bytearray.fromhex(HEX_STRING)
    print(data)
    BASE64_VAL = base64.b64encode(data)
    print(BASE64_VAL)

def main():
    convert_hex_b64(HEX_STRING)



if __name__ == "__main__":
    main()