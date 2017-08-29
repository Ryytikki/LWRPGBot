import discord
from discord.ext import commands
import pickle


charSheet = {'ID'       :   0,
             'name'     :   '',
             'token'    :   '',
             'bio'      :   '',
             'playerID' :   0,
             'str'      :   0,
             'int'      :   0,
             'cun'      :   0,
             'luc'      :   0,
             'bra'      :   0,
             'init'     :   0,
             'res'      :   0}
             
charList = []

def saveChars():
    with open('./data/charList.pkl', 'wb+') as f:
        pickle.dump(charList, f, pickle.HIGHEST_PROTOCOL)

def loadChars():
    with open('./data/charList.pkl', 'rb') as f:
        global charList 
        charList = pickle.load(f)
        
             
class charSheets():
    def __init__(self,bot):
        self.bot = bot
        try:
            loadChars()
        except:
            print("Character file not found")
        
    @commands.command(pass_context = True)
    async def createPlayer(self, ctx):
        global charList
        id = 0
        # Check if the player already has a character
        for char in charList:
            if char['playerID'] == ctx.message.author:
                await self.bot.say("You've already been assigned a character. Currently only 1 character per player is supported")
                return
            id += 1
                
        # Create a new sheet        
        player = dict(charSheet)
        player['playerID'] = ctx.message.author
        player['ID'] = id
        charList.append(player)
        await self.bot.say("Character created for {0}. Dont forget to add their info!".format(ctx.message.author.mention))
        
        # Save data to file
        saveChars()
        
    @commands.command(pass_context = True)
    async def setName(self, ctx, *args):
        global charList
        # Form the name
        name = ' '.join(args)
        
        # Find the character
        for char in charList:
            if char['playerID'] == ctx.message.author:
                # Assign the name
                await self.bot.say("Old name: {0}\nNew name: {1}".format(char['name'], name))
                char['name'] = name
                saveChars()
                return
                
    @commands.command(pass_context = True)
    async def setBio(self, ctx, *args):
        global charList
        # Form the name
        bio = ' '.join(args)
        
        # Find the character
        for char in charList:
            if char['playerID'] == ctx.message.author:
                char['bio'] = bio
                saveChars()
                await self.bot.say("Bio set!")
                return

    @commands.command(pass_context = True)
    async def setToken(self, ctx, *args):
        global charList
        # Form the name
        token = ' '.join(args)
        
        # Find the character
        for char in charList:
            if char['playerID'] == ctx.message.author:
                char['token'] = token
                await self.bot.say("Token set!")
                return
                
    @commands.command(pass_context = True)
    async def setStats(self, ctx, *args):
        global charList
        # Find the character
        for char in charList:
            if char['playerID'] == ctx.message.author:
                # Assign the stats
                char['str'] = args[0]
                char['int'] = args[1]
                char['cun'] = args[2]
                char['luc'] = args[3]
                char['bra'] = args[4]
                char['init'] = args[5]
                char['res'] = args[6]
                saveChars()
                await self.bot.say("Stats set to: STR {0}/INT {1}/CUN {2}/LUC {3}/BRA {4}/INIT {5}/DEF {6}".format(args[0], args[1], args[2], args[3], args[4], args[5], args[6]))
                return
                
    @commands.command(pass_context = True)           
    async def mySheet(self, ctx):
        global charList
        # Find the character
        for char in charList:
            if char['playerID'] == ctx.message.author:
                await self.bot.say("```Name: {0}\nPlayer: {8}\nBio: {6}\nToken: {7}\n\nStats:\nSTR: {1}\nINT: {2}\nCUN: {3}\nLUC: {4}\nBRA: {5}```".format(char['name'], char['str'], char['int'], char['cun'], char['luc'], char['bra'], char['bio'], char['token'], char['playerID'].display_name))
                return
    
    @commands.command()           
    async def listChars(self):
        global charList
        output = ""
        for char in charList:
            output = output + "{0}  :   {1}\n".format(char['ID'], char['name'])
        
        await self.bot.say("```{0}```".format(output))
        
def setup(bot):
    bot.add_cog(charSheets(bot))           
