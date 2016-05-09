import csv
import urllib3
import logging
import win_unicode_console
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig(filename='parser.log', format='%(asctime)s %(levelname)s:%(message)s')
print(type(logger))
csvPath = 'C:\\Users\\Harune\\Downloads\\Fantasy War Tactics - Max Stats - Stats (Live).csv'
skillUrlTemplate = 'http://fwt.wikia.com/wiki/{0}/Skills'
characterUrlTemplate = 'http://fwt.wikia.com/wiki/{0}'
wikiaImageUrlTemplate = 'http://fwt.wikia.com/wiki/File:{0}'
imageUrlDict = {}
debug = True


def getImageLink(imageUrl):
    with http.request('GET', imageUrl) as imageToDownloadResponse:
        imageToDownloadSoup = BeautifulSoup(imageToDownloadResponse.data, 'html.parser')
        print('imageToDownloadResponse Status: ' + str(imageToDownloadResponse.status))
        #Parse the src of the img to get the imageToDownloadUrl
        imageToDownloadUrl = imageToDownloadSoup.find('div', attrs={'class':'fullImageLink'}).find('a').get('href')
        if debug == True: logger.info('imageUrl: ' + imageUrl + ' imageToDownloadUrl: ' + imageToDownloadUrl)
        return imageToDownloadUrl

def formatBattleType(battleType):
    if battleType == 'Defence': return 'Defense type'
    if battleType == 'Attack' or battleType == 'Support' or battleType == 'Defense': return battleType + ' type'
    if battleType == 'Area': return battleType + '-attack'
    return battleType

def formatHeroNameForUrl(heroName):
    return ''


def parseSkills(skillUrl):
    return 'fasdfasd'

http = urllib3.PoolManager()
win_unicode_console.enable() #Resolves windows unicode conflict


i = 0
with open(csvPath) as csvFile:
    rowDict = csv.DictReader(csvFile)
    for row in rowDict:
        # print(str(row))

        heroInfoDict = {}
        statInfoDict = {}
        skillInfoDict = {}
        coopInfoDict = {}

        if debug == True: print('Character url: ' + characterUrlTemplate.format(row['Hero']))
        if debug == True:  print('Skill url: ' + skillUrlTemplate.format(row['Hero']))

        #Hero Info
        heroInfoDict['name'] = row['Hero']
        heroInfoDict['title'] = row['Title']
        heroInfoDict['type'] = row['Type']
        heroInfoDict['recruitmentLocation'] = row['Recruitment Info']
        heroInfoDict['genesRequired'] = row['Gene Fragment']
        heroInfoDict['battleType'] = row['Battle Type']

        
        heroInfoDict['terrain'] = 'Terrain'

        # print(str(heroInfoDict))
        try:
            htmlCharacterData = http.request('GET', characterUrlTemplate.format(row['Hero']))
            htmlCharacterSoup = BeautifulSoup(htmlCharacterData.data, 'html.parser')
            infoBox = htmlCharacterSoup.find('table', attrs={'class':'infobox'})
            infoBoxTR = infoBox.find_all('tr')
            if debug == True: print('Response Status For Hero Page: ' + str(htmlCharacterData.status))

            #Type
            #Add image url of type[Paper, Rock, Scissors] if not exist
            currentHeroType = heroInfoDict['type']
            if(currentHeroType not in imageUrlDict):
                urlSuffix = infoBoxTR[0].find('a', attrs={'title':currentHeroType}).find('img').get('data-image-key')
                typeImageUrl = wikiaImageUrlTemplate.format(urlSuffix) #Just Url. Need to find img src within response
                print(typeImageUrl)
                imageUrlDict[currentHeroType] = getImageLink(typeImageUrl)
                #End typeImage parsing

            #Battle Type
            currentHeroBattleType = heroInfoDict['battleType']
            print('currentHeroBattleType: ' + currentHeroBattleType)
            if(currentHeroBattleType not in imageUrlDict):
                formattedBattleType = formatBattleType(currentHeroBattleType)
                urlSuffix = infoBoxTR[0].find('a', attrs={'title':formattedBattleType}).find('img').get('data-image-key')
                battleTypeImageUrl = wikiaImageUrlTemplate.format(urlSuffix)
                print('urlSuffix: ' + urlSuffix)
                print(battleTypeImageUrl)
                imageUrlDict[currentHeroBattleType] = getImageLink(battleTypeImageUrl)

            #Terrain
            heroTerrainElements = infoBoxTR[2].find_all('a')
            terrainToAdd = []
            for heroTerrainElement in heroTerrainElements:
                terrainToAdd.append(heroTerrainElement.get('title'))
            print(str(terrainToAdd))

            #Image Url for Hero, typepe if !exist, battleType if not exist, Terrain if not exist
            #Fill heroInfoDict with Terrain
            # print('infoBox: ' + str(type(infoBox)))




            htmlCharacterData.close()

            print('\n')
        except Exception as e:
            print('Something went wrong')
            print(str(e))
        #End try catch



        # dictList.add(heroInfoDict)

        #Stats | Put it in another block?
        if(i==4):
            break
        i+=1



win_unicode_console.enable()