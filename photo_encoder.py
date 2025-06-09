from PIL import Image
import io

codir = 'utf-8'

def text_to_bits(text, encoding=codir, errors="ignore"):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding=codir, errors="ignore"):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0' # , 'big'

print('.png information hider by HumaYT v 1.0\n\n')
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

    img = Image.open(load_name).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    sbits = text_to_bits(s)
    lens = len(sbits)

    if lens > width * height:
        print('[ERROR] TOO MUCH INFORMATION FOR THIS .PNG FILE!')
        input()
    else:
        with open('debug.txt', 'a+') as dbg_file:
            for i in range(height):
                for j in range(width):
                    if i*width + j < len(sbits):
                        pixels[j, i] = pixels[j, i][0], pixels[j, i][1], int(str(bin(pixels[j, i][2])[2:])[:-1] + sbits[(i*width) + j],2), pixels[j, i][3]

        img.save(save_name)

        with open(save_name, 'a') as file:
            file.write('\n' + str(lens))

        print('Saved to',save_name)
        input()
else:
    print('Enter input .png filename (with extension)')
    load_name = input()

    print('Enter output decrypted filename (.txt)')
    save_name = input()

    l = ''
    z = io.open(load_name, errors="ignore", encoding=codir).readlines()
    lenz = int(z[-1])

    img = Image.open(load_name).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    for i in range(height):
        for j in range(width):
          if len(l) < lenz:
            l += bin(pixels[j, i][2])[-1]
    with open(save_name, 'a+') as file:
        file.write(text_from_bits(l))

    print('Succesfully decrypted result to', save_name)
    input()