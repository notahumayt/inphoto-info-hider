from PIL import Image
import io
import random
import string
import sys
import tqdm

Image.MAX_IMAGE_PIXELS = 10**20


codir = 'utf-8'

def text_to_bits(s):
    l = ''
    for i in s:
        l += format(ord(i), '08b').zfill(8)
    return l

def text_from_bits(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

print('.png information hider by HumaYT v 1.3\n')
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

    print('Enter file we are hiding...')
    input_name = input()
    try:
        s = io.open(input_name).read()
        sbits = text_to_bits(s)
    except FileNotFoundError:
        print('[ERROR] NO SUCH FILE OR DIRECTORY')
        input()
        sys.exit()
    except UnicodeDecodeError:
        print('Reading hard file...')
        sbits = ''
        with open(input_name, 'rb') as f:
            #sbits = ''.join(format(i, 'b').zfill(8) for i in f.read())
            for i in tqdm.tqdm(f.read()):
                sbits += format(i, 'b').zfill(8)

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

    print('Enter output hiding file')
    save_name = input()

    img = Image.open(load_name).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    l = ''
    countl = 0
    with open(save_name, 'wb+') as f:
        for i in tqdm.tqdm(range(height)):
            for j in range(width):
                if countl <= lenz:
                    codebit = int(key_bits[(((i * width + j) % 64) - 1) * 2] + key_bits[(((i * width + j) % 64) - 1) * 2 + 1],2)
                    l+=bin(pixels[j, i][codebit])[-1]
                    countl += 1
                    if len(l)%8==0:
                        f.write(int(l,2).to_bytes(1, byteorder='big'))
                        l = ''
                else:
                    break

    print('Successfully decrypted result to', save_name)
    input()