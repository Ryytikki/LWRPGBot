import discord
from discord.ext import commands
import subprocess
import time
import os
import shutil

from server import *

try:
    from PIL import Image
except ImportError:
    import Image
        

class map():
    def __init__(self,bot):
        self.bot = bot
        try:
            loadMaps()
        except:
            print("Map file not found")    
    
    @commands.command(pass_context = True) 
    async def addMap(self, ctx, *args):
        
        pixelSize = 32
        
        await self.bot.say("Generating map.\nFile       :    {0}\nName      :   {1}\nSize     :   [{2},{3}]".format(args[0], args[1], args[2], args[3]))   
        subprocess.Popen(["python3.5", "./extensions/genMap.py", args[0], args[1], str(pixelSize)])
        
        newMap = dict(mapData)
        newMap['name'] = args[1]
        newMap['size'] = [args[2], args[3]]
        newMap['gridSized'] = pixelSize * 2
        global maps
        maps.append(newMap)
        saveMaps()
        
        await self.bot.say("Starting map generation script. Please give this a minute or two to run before using maps")
    
    @commands.command()    
    async def listMaps(self, *args):
        i = 0
        global maps
        if len(maps) == 0:
            return await self.bot.say("No maps found")
            
        for map in maps:
            await self.bot.say("{0} :   {1}".format(i, map['name']))
            i+=1
        await self.bot.say("Done")
        
    @commands.command()
    async def setMap(self, *args):
        global mapStatus
        global maps
        mapStatus['currentCombat'] = int(args[0])
        map = maps[int(args[0])]
        saveMaps()
        shutil.copy2("./maps/combat/{0}.png".format(maps[mapStatus['currentCombat']]['name']), "./maps/combat.png")
        shutil.copy2("./maps/combat/{0}.png".format(maps[mapStatus['currentCombat']]['name']), "./maps/combatBase.png")
        return await self.bot.say("Combat map set to map ID {0}, {1}".format(args[0], map['name']))
        
    @commands.command(pass_context = True)
    async def deleteMap(self, ctx, *args):
        global mapStatus
        global maps
        
        mapID = int(args[0])
        await self.bot.say("Removing map ID {0}: {1}.".format(mapID, maps[mapID]['name']))
        os.delete("maps/combat/" + maps[mapID]['name'])
        if mapStatus['currentCombat'] == mapID:
            mapStatus['currentCombat'] = -1
            mapStatus['pogLocations'] = []
        elif mapStatus['currentCombat'] > mapID:
            mapStatus['currentCombat'] -= 1
        
        maps.pop(mapID)
        saveMaps()
        
    @commands.command(pass_context = True)
    async def showMap(self, ctx, *args):
        global mapStatus
        if mapStatus['currentCombat'] == -1:
            return await self.bot.say("No map found")
        return await self.bot.send_file(ctx.message.channel, "maps/combat.png")
        
             
    @commands.command(pass_context = True) 
    async def addOverworld(self, ctx, *args):
        await self.bot.say("Generating overworld map.\nFile       :    {0}\nName      :   {1}".format(args[0], args[1]))
        urllib.urlretrieve(args[0], args[1] + ".png")
        await self.bot.say("File saved")
        
        newMap = dict(overworldData)
        newMap['name'] = args[1]
        overworld.append(newMap)
        
        saveMaps()
        
    @commands.command()
    async def listOverworld(self, *args):
        i = 0
        global overworld
        if len(overworld) == 0:
                return await self.bot.say("No maps found")
                
        for map in overworld:
            await self.bot.say("{0} :   {1}".format(i, map['name']))
            i+=1
        await self.bot.say("Done") 
        
    @commands.command(pass_context = True)    
    async def showOverworld(self, ctx, *args)
        await self.bot.say("TODO") 
        
def setup(bot):
    bot.add_cog(map(bot))  