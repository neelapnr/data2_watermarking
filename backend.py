import string

def cesar_cipher(text, key, cipher):
	if type(text) == str and type(key) == int:
		shift = 1 if cipher else -1
		list_of_crypted_chars = []
		for char in text :
			list_of_crypted_chars.append(chr((ord(char) + shift * key) % 1_114_112))

		crypted_text = "".join(list_of_crypted_chars)
		return crypted_text
	else:
		raise(TypeError)


def hack_cesar_cipher(crypted_text, alphabet):
	if type(crypted_text) == str and type(alphabet) == str:
		for possible_key in range(0, 1_114_112):
			possible_uncryption = cesar_cipher(crypted_text, possible_key, cipher=False)
			if possible_uncryption[0] in alphabet:
				print(possible_key)
				print(possible_uncryption)
				print("_"*20)
	else:
		raise(TypeError)


def vigenere_cipher(text, password, cipher):
	list_of_crypted_chars = []
	list_of_keys = [ord(char) for char in password]
	
	for index, current_char in enumerate(text):
		
		current_key = list_of_keys[index % len(list_of_keys)]
		current_crypted_char = cesar_cipher(current_char, current_key, cipher)

		list_of_crypted_chars.append(current_crypted_char)

	crypted_text = "".join(list_of_crypted_chars)

	return crypted_text


if __name__ == "__main__":
	message = "le chocolat est bon"

	crypted_text = cesar_cipher(message, 12, cipher=True) # exo 1
	print(crypted_text)

	initial_message = cesar_cipher(crypted_text, 12, cipher=False) # exo 2
	print(initial_message == message)

	hack_cesar_cipher(crypted_text, alphabet=string.printable) # exo3

	crypted_message = vigenere_cipher(text=message, password="Azerty12345!", cipher=True)
	print(crypted_message)
	initial_message = vigenere_cipher(text=crypted_message, password="Azerty12345!", cipher=False)
	print(initial_message)


from PIL import Image
import numpy as np

def print_pixel_value(image, x, y):
    value = image[y, x]                                                                                                          
    print("Valeur du pixel :", value)
    print(f"Position x: {x} Position y: {y}")
   

def text_to_binary(text):
    list_of_binary_values = []
    for char in text:
        ascii_value = ord(char)
        binary_ascii_char = bin(ascii_value)[2:]
        binary_ascii_char = binary_ascii_char.zfill(21)
        list_of_binary_values.append(binary_ascii_char)
    binary_text = "".join(list_of_binary_values)
    return binary_text


def get_even_array_image(image):
    even_image = image - image % 2
    return even_image


def watermark_lsb1(even_image, binary_mesage):
    array_of_pixels = even_image.flatten()
    if len(binary_mesage) > len(array_of_pixels):
        raise ValueError("Le message est trop long pour cette image.")
    for index_char in range(len(binary_mesage)):
        bit = binary_mesage[index_char]
        if bit == '1':
            array_of_pixels[index_char] += 1
   
    watermarked_image = array_of_pixels.reshape(even_image.shape)
    print("Message encodé dans l'image.")
    return watermarked_image


def get_message_from_watermarked_image(watermarked_image):
    array_of_pixels = watermarked_image.flatten()
    array_binary_message = array_of_pixels % 2
    list_of_chars = []
    for index in range(0, len(array_binary_message), 21):
        binary_ascii_value = array_binary_message[index: index+21]
        if binary_ascii_value.any():
            char = chr(int("".join([str(value) for value in binary_ascii_value]), 2))
            list_of_chars.append(char)
        else:
             break
        print(binary_ascii_value)
    message = "".join(list_of_chars)
    return message


if __name__ == "__main__":
    image = Image.open("/Users/pnr/Desktop/data2_watermarking/image.jpg")
    image = image.convert('L')
    print(f"Taille image : {image.size}")
    image.show()
    array_image = np.array(image)

    # print_pixel_value(image, 10, 15)
   
    message_original = "Salut, ça fonctionne !"
    print("Message original :", message_original)
    even_array_image = get_even_array_image(array_image)
    binary_mesage = text_to_binary(message_original)
    watermarked_array_image = watermark_lsb1(even_array_image, binary_mesage)
    Image.fromarray(watermarked_array_image).save("OIP_watermarked.png")
    print("Image encodée sauvegardée.")
    initial_message = get_message_from_watermarked_image(watermarked_array_image)
    print("Message décodé :", initial_message)
    if message_original == initial_message:
        print("\nLes messages sont identiques.")
    else:
        print("\nLes messages sont différents.")
