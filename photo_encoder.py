from PIL import Image
import io
import random
import string

codir = 'utf-8'

def text_to_bits(text, encoding=codir, errors="ignore"):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding=codir, errors="ignore"):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0' # , 'big'

print('.png information hider by HumaYT v 1.1\n\n')
print('Choose mode:')
print('1 - Paste information inside .png')
print('2 - Get information out of .png')

mode = int(input())
while (mode != 1) and (mode != 2):
    print('Wrong mode! Try again!')
    mode = int(input())

if mode == 1:
    print('Enter input .png filename (with extension)')
    load_name = input()

    print('Enter input encryption filename (.txt)')
    s = open(input(), encoding=codir).read()

    print('Enter output .png filename')
    save_name = input()

    print('Enter key filename')
    key_file = input()

    print('Generating key...')
    key = ''.join(random.choices(string.printable, k=32))
    print('Key:',key)

    key_bits = text_to_bits(key)

    img = Image.open(load_name).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    sbits = text_to_bits(s)
    lens = len(sbits)

    if lens > width * height:
        print('[ERROR] TOO MUCH INFORMATION FOR THIS .PNG FILE!')
        input()
    else:
        for i in range(height):
            for j in range(width):
                if i*width + j < len(sbits):
                    pp = [pixels[j, i][0],pixels[j, i][1],pixels[j, i][2],pixels[j, i][3]]
                    codebit = int(key_bits[(((i*width+j) % 64)-1) * 2] + key_bits[(((i*width+j) % 64)-1) * 2 + 1],2)
                    pp[codebit] = int(str(bin(pixels[j, i][codebit])[2:])[:-1] + sbits[(i*width) + j],2)
                    pixels[j, i] = tuple(pp)

        img.save(save_name)

        with open(save_name, 'a') as file:
            file.write('\n' + str(lens))

        print('\n')
        print('Saved to',save_name)

        with open(key_file, 'a+') as file:
            file.write('\n' + str(key))

        print('Saved key to', key_file)

        input()
else:
    print('Enter input .png filename (with extension)')
    load_name = input()

    print('Enter key filename')
    key_file = input()

    key = io.open(key_file, errors="ignore", encoding=codir).readlines()[-1]
    key_bits = text_to_bits(key)

    print('Sucessfully initialized key',key)


    print('Enter output decrypted filename (.txt)')
    save_name = input()

    l = ''
    lenz = int(io.open(load_name, errors="ignore", encoding=codir).readlines()[-1])

    img = Image.open(load_name).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    for i in range(height):
        for j in range(width):
            if len(l) < lenz:
                codebit = int(key_bits[(((i * width + j) % 64) - 1) * 2] + key_bits[(((i * width + j) % 64) - 1) * 2 + 1],2)
                l += bin(pixels[j, i][codebit])[-1]
    with open(save_name, 'a+') as file:
        file.write(text_from_bits(l))

    print('Succesfully decrypted result to', save_name)
    input()