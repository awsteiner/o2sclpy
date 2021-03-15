import math
from PIL import Image
import operator
import functools
img1=Image.open('../figures/near_blue_doc.png').histogram()
img2=Image.open('near_blue.png').histogram()
rms = math.sqrt(functools.reduce(operator.add,
                       map(lambda a,b: (a-b)**2, img1, img2))/len(img1))
print(rms)
