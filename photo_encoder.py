from PIL import Image
import io
import random
import string
import sys
import tqdm

codir = 'utf-8'

def text_to_bits(text, encoding=codir, errors="ignore"):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding=codir, errors="ignore"):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0' # , 'big'

print('.png information hider by HumaYT v 1.2\n')
print('Choose mode:')
print('1 - Paste information inside .png')
print('2 - Get information out of .png')

mode = int(input())
while (mode != 1) and (mode != 2):
    print('Wrong mode! Try again!')
    mode = int(input())

if mode == 1:
    print('Enter input .png filename')
    load_name = input()
    if not(load_name[-4:]=='.png'):
        load_name += '.png'
    try:
        img = Image.open(load_name).convert('RGBA')
        pixels = img.load()
        width, height = img.size
    except FileNotFoundError:
        print('[ERROR] NO SUCH FILE OR DIRECTORY')
        input()
        sys.exit()

    print('Enter input encryption filename (.txt)')
    try:
        s = open(input(), encoding=codir).read()
    except FileNotFoundError:
        print('[ERROR] NO SUCH FILE OR DIRECTORY')
        input()
        sys.exit()

    print('Enter output .png filename')
    save_name = input()
    if not(save_name[-4:]=='.png'):
        save_name += '.png'

    print('\nChoose key mode:')
    print('1 - Generate new key')
    print('2 - Use pre-generated key from file')
    key_mode = int(input())

    while (key_mode != 1) and (key_mode != 2):
        print('Wrong mode! Try again!')
        key_mode = int(input())

    print('Enter key filename')
    key_file = input()

    if key_mode == 1:
        print('Generating key...')
        key = ''.join(random.choices(string.ascii_letters+string.digits, k=32))
        print('Key:',key)
        with open(key_file, 'a+') as file:
            file.write('\n' + str(key))
        print('Saved key to', key_file)
    if key_mode == 2:
        print('Reading key...')
        try:
            key = io.open(key_file, errors="ignore", encoding=codir).readlines()[-1]
            print('Initialized key:', key)
            if len(key) != 32:
                print('[ERROR] WRONG KEY LENGTH. KEY LENGTH SHOULD BE 32 SYMBOLS')
                input()
                sys.exit()
        except FileNotFoundError:
            print('[ERROR] NO SUCH FILE OR DIRECTORY')
            input()
            sys.exit()

    key_bits = text_to_bits(key)
    sbits = text_to_bits(s)
    lens = len(sbits)

    if lens > width * height:
        print('[ERROR] TOO MUCH INFORMATION FOR THIS .PNG FILE!')
        input()
    else:
        print('Starting encoding...')
        for i in tqdm.tqdm(range(height)):
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
        print('Saved result to',save_name)

        input()
else:
    print('Enter input .png filename')
    load_name = input()
    if not(load_name[-4:]=='.png'):
        load_name += '.png'
    try:
        lenz = int(io.open(load_name, errors="ignore", encoding=codir).readlines()[-1])
    except FileNotFoundError:
        print('[ERROR] NO SUCH FILE OR DIRECTORY')
        input()
        sys.exit()
    print('Enter key filename')
    key_file = input()
    try:
        key = io.open(key_file, errors="ignore", encoding=codir).readlines()[-1]
    except FileNotFoundError:
        print('[ERROR] NO SUCH FILE OR DIRECTORY')
        input()
        sys.exit()

    print('Successfully initialized key:',key)
    key_bits = text_to_bits(key)

    print('Enter output decrypted filename (.txt)')
    save_name = input()

    l = ''

    img = Image.open(load_name).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    for i in tqdm.tqdm(range(height)):
        for j in range(width):
            if len(l) < lenz:
                codebit = int(key_bits[(((i * width + j) % 64) - 1) * 2] + key_bits[(((i * width + j) % 64) - 1) * 2 + 1],2)
                l += bin(pixels[j, i][codebit])[-1]
    with open(save_name, 'a+') as file:
        file.write(text_from_bits(l))

    print('Successfully decrypted result to', save_name)
    input()