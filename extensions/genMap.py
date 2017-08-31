# Code taken and adapted from https://stackoverflow.com/questions/20368413/draw-grid-lines-over-an-image-in-matplotlib

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import urllib.request as urllib
import sys
try:
    from PIL import Image
except ImportError:
    import Image

args = sys.argv

if len(args) < 3:
    pixelSize = 32
else:
    pixelSize = int(args[3])
    
# Open image file
urllib.urlretrieve(args[1], "mapBase.png")
image = Image.open("mapBase.png")
image = image.resize((image.size[0] * 2, image.size[1] * 2), Image.ANTIALIAS)
my_dpi=300.

# Set up figure
fig=plt.figure(figsize=(float(image.size[0])/my_dpi,float(image.size[1])/my_dpi),dpi=my_dpi)
ax=fig.add_subplot(111)

# Remove whitespace from around the image
fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

# Set the gridding interval: here we use the major tick interval
myInterval=pixelSize * 2.
loc = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

# Add the grid
ax.grid(which='major', axis='both', linestyle='-')

# Add the image
ax.imshow(image, zorder = 1)

# Find number of gridsquares in x and y direction
nx=abs(int(float(ax.get_xlim()[1]-ax.get_xlim()[0])/float(myInterval)))
ny=abs(int(float(ax.get_ylim()[1]-ax.get_ylim()[0])/float(myInterval)))

plt.xlim([0, nx*myInterval])
plt.ylim([ny*myInterval, 0])

# Add some labels to the gridsquares
for j in range(ny):
    y=myInterval/2+j*myInterval
    for i in range(nx):
        x=myInterval/2.+float(i)*myInterval
        ax.text(x,y,'{:d}'.format(i+j*nx),color='w',ha='center',va='center', size='3', zorder = 2)

# Save the figure
fig.savefig("./maps/combat/" + args[2] + '.png',dpi=my_dpi)