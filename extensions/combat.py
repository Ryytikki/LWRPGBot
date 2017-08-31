import discord
from discord.ext import commands
import matplotlib.pyplot as plt
from server import *

try:
    from PIL import Image
except ImportError:
    import Image

def drawMap():
    global mapStatus
    global maps
    # Open image file
    image = Image.open('maps/combatBase.png')
    my_dpi=300.
    
    # Set up figure
    fig=plt.figure(figsize=(float(image.size[0])/my_dpi,float(image.size[1])/my_dpi),dpi=my_dpi)
    ax=fig.add_subplot(111)

    # Remove whitespace from around the image
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    for pog in mapdata["pogLocations"]:
        pog = Image.open('tokens/' + pog['name'] + '.png')
        loc = pog['loc']
        x = maps[mapStatus['currentCombat']]['size'][0]
        x = math.floor(loc[0]/x)
        pos = [x,loc[1] - x]
        ax.imshow(pog, extent=(pos[0]*64,(pos[0]+1)*64,pos[1]*64,(pos[1]+1)*64), zorder = 3)
    
    # Save the figure
    fig.savefig('maps/combat.png',dpi=my_dpi)
    
class combat():
    def __init__(self,bot):
        self.bot = bot
         
 def setup(bot):
    bot.add_cog(map(combat))