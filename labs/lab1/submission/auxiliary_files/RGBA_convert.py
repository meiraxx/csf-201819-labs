import PIL
from PIL import Image

img = Image.open("black.png")
width, height = img.size
conv = img.convert('RGBA').getdata()
original = open("original.txt","w")
a = str(list(conv))
original.write(a)
original.close()
modified = open("modified.txt","w")
imgB = Image.open("black-stego.png")
width, height = imgB.size
convB = imgB.convert('RGBA').getdata()
b = str(list(convB))
modified.write(b)
modified.close()