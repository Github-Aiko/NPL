import os
from PIL import Image

for filename in os.listdir('./cat'):
    img = Image.open(os.path.join('./cat', filename))
    img.save(os.path.join('./cat', filename.replace('.jfif', '.jpg')))
    os.remove(os.path.join('./cat', filename))