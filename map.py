import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import pickle
import urllib.request as urllib
import io
try:
    from PIL import Image
except ImportError:
    import Image

mapStatus = {'currentOverworld'   :   "",
             'currentCombat'      :   "",
             'pogLocations'       :   []}
             
mapData = {'name'       :   "",
           'size'       :   [0,0],
           'gridSize'   :   64}

maps = []

def saveMaps():
    with open('./data/mapList.pkl', 'wb+') as f:
        pickle.dump(maps, f, pickle.HIGHEST_PROTOCOL)
    with open('./data/mapStatus.pkl', 'wb+') as f:
        pickle.dump(mapStatus, f, pickle.HIGHEST_PROTOCOL)

def loadMaps():
    with open('./data/mapList.pkl', 'rb') as f:
        global maps
        maps = pickle.load(f)
    with open('./data/mapStatus.pkl', 'rb') as f:
        global mapStatus
        mapStatus = pickle.load(f)


class map():
    def __init__(self,bot):
        self.bot = bot
        try:
            loadMaps()
        except:
            print("Map file not found")
        
    # Code taken and adapted from https://stackoverflow.com/questions/20368413/draw-grid-lines-over-an-image-in-matplotlib
    @commands.command(pass_context = True) 
    async def genGrid(self, ctx, *args):
        
        if len(args) < 3:
            pixelSize = 32
        else:
            pixelSize = args[2]
            
        await self.bot.say("Generating map.\nFile            :    {0}\nName        :   {1}\nPixel size  :   {2}".format(args[0], args[1], pixelSize))   
        
        # Download image file from the web
        f = io.BytesIO(urllib.urlopen(args[0]).read())
        image = Image.open(f)
        print(image.size)
        # Resize to 64x64 tiles
        image = image.resize((int(image.size[0] * 64/pixelSize), int(image.size[1] * 64/pixelSize)), Image.ANTIALIAS)
        my_dpi=300.
        await self.bot.say("File Loaded")
        
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
                
        #pog = Image.open('testPog.png')
        #ax.imshow(pog, extent=(10*64,11*64,7*64,8*64), zorder = 3)

        # Save the figure
        plt.savefig("./maps/combat/" + args[1] + '.png',dpi=my_dpi)
        print("Saving fig")
        newMap = dict(mapData)
        newMap['name'] = args[1]
        newMap['size'] = [nx, ny]
        newMap['gridSized'] = myInterval
        global maps
        maps.append(newMap)
        saveMaps()
        print("saved map")
        
        #await self.bot.say("Map created and saved as {0}.png".format(args[1]))
        #await self.bot.send_file(ctx.message.channel, "./maps/combat/"+args[1]+'.png')
        
        
def setup(bot):
    bot.add_cog(map(bot))  