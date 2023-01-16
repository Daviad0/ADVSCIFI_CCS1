import pygame
import random
import math

pygame.init()

class Sprite():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())



class Statusbar(Sprite):
    def __init__(self, x, y, image, name, value, max_value):
        super().__init__(x, y, image)
        self.name = name
        self.value = value
        self.max_value = max_value

class City(Sprite):
    def __init__(self, x, y, image, name, population, max_population):
        super().__init__(x, y, image)
        self.name = name
        self.population = population
        self.max_population = max_population
        self.occupied = True
        
        self.cityOptions = {
            "Send Ship": [1,5],
            "Retrive Ship": [1,5],
            "Host Knowledge Festival": [1,5],
            "Gage Loyalty & Happiness": [1,5],
            "Denounce City": [1,6]
        }
        self.loyalty = random.randint(15, 25)
        self.happiness = random.randint(35, 50)
        self.knownHappiness = self.happiness
        self.knownLoyalty = self.loyalty
        


DISPLAY = pygame.display.set_mode((1200, 800))
CLOCK = pygame.time.Clock()
FONT_MEDIUM = pygame.font.Font("assets/MartianMono-Regular.ttf", 20)
FONT_LARGE = pygame.font.Font("assets/MartianMono-Regular.ttf", 32)
FONT_SMALL = pygame.font.Font("assets/MartianMono-Regular.ttf", 12)


moveSound = pygame.mixer.Sound('assets/move.wav')
selectSound = pygame.mixer.Sound('assets/select.wav')

populationMarker= pygame.image.load("assets/population.png")
loyaltyMarker= pygame.image.load("assets/loyalty.png")
loyaltyMarkerG= pygame.image.load("assets/loyalty_gray.png")
happinessMarker= pygame.image.load("assets/happiness.png")
happinessMarkerG= pygame.image.load("assets/happiness_gray.png")
intelligenceBar = pygame.image.load("assets/intelligence.png")
selector = Sprite(0, 0, pygame.image.load("assets/selector.png"))
sideMenu = Sprite(-100, 100, pygame.image.load("assets/sidemenu.png"))
titleMenu = Sprite(0, 0, pygame.image.load("assets/titlemenu.png"))
titleMenu.rect.center = [600, 400]
controlItem = pygame.image.load("assets/controlitem.png")
controlItem = pygame.transform.scale(controlItem, (240, 40))

leftarrow = pygame.image.load("assets/leftarrow.png")
rightarrow = pygame.image.load("assets/rightarrow.png")

# start implementing "loyalty bar"
loyaltyBar = Sprite(0, 0, pygame.image.load("assets/loyaltybar.png"))
loyaltyBar.rect.center = [600, 700]
knownGoodLoyalty = pygame.Surface((8, 72))
knownGoodLoyalty.fill((0, 255, 0))
knownBadLoyalty = pygame.Surface((32, 72))
knownBadLoyalty.fill((255, 0, 0))
unknownLoyalty = pygame.Surface((360, 72))
unknownLoyalty.fill((120, 120, 120))
loyalties = {
    "Good": 2,
    "Bad": 8,
    "Unknown": 90
}
# loyalty bar has 2* width for every point


policyMarker = pygame.image.load("assets/policies.png")
policyMarker = pygame.transform.scale(policyMarker, (120, 120))
policyMarkerRect = policyMarker.get_rect()
policyMarkerRect.center = [420, 720]

globalMarker = pygame.image.load("assets/global.png")
globalMarker = pygame.transform.scale(globalMarker, (100, 100))
globalMarkerRect = globalMarker.get_rect()
globalMarkerRect.center = [300, 730]

nextButton = pygame.image.load("assets/nextturn.png")
nextButton = pygame.transform.scale(nextButton, (200, 80))
nextButtonRect = nextButton.get_rect()
nextButtonRect.center = [600, 720]

turn = 1
intelligence = 0

background = pygame.image.load("assets/background_2.png")
background = pygame.transform.scale(background, (1400, 800))
dimBg = pygame.Surface((1400, 800), flags=pygame.SRCALPHA)
dimBg.fill((0, 0, 0, 64))
winBg = pygame.Surface((1400, 800))
winBg.fill((85, 147, 174))
gameState = "game"

citiesSelectMap = {
    "Los Angeles": ["", "New York", "New York", "Brasília"],
    "New York": ["Los Angeles", "London", "", "Brasília"],
    "London": ["New York", "Moscow", "", "Lagos"],
    "Brasília": ["Los Angeles", "Brasília", "Los Angeles", ""],
    "Canberra": ["Brasília", "", "Moscow", ""],
    "Moscow": ["London", "Canberra", "", "Canberra"],
    "Lagos": ["Brasília", "Canberra", "London", ""],
}
# 0: Left, 1: Right, 2: Up, 3: Down
cities = []
cities.append(City(110, 210, pygame.image.load("assets/city.png"), "Los Angeles", random.randint(1,5), 100))
cities.append(City(280, 110, pygame.image.load("assets/city.png"), "New York", random.randint(1,5), 100))
cities.append(City(530, 120, pygame.image.load("assets/city.png"), "London", random.randint(1,5), 100))
cities.append(City(290, 420, pygame.image.load("assets/city.png"), "Brasília", random.randint(1,5), 100))
cities.append(City(910, 510, pygame.image.load("assets/city.png"), "Canberra", random.randint(1,5), 100))
cities.append(City(700, 170, pygame.image.load("assets/city.png"), "Moscow", random.randint(1,5), 100))
cities.append(City(530, 400, pygame.image.load("assets/city.png"), "Lagos", random.randint(1,5), 100))

# Turns Left, Turns Added
sideMenuOptions = {
    "Make Public Statement" : [1, 5],
    "Appoint New Leader" : [1, 10],
    "Make New Law" : [1, 15]
}

optionsList = {
    0: [
        "W/S/A/D - Change City",
        "Space - Select City",
        "P - Determine Policies",
        "Enter - Start Next Turn"
    ],
    1: [
        "W/S - Change Option",
        "Space - Select Option",
        "Esc - Go Back"
    ],
    2: [
        "W/S - Change Option",
        "Space - Select Option",
        "Esc - Go Back"
    ],
    3: [
        "Left Arrow - First Option",
        "Right Arrow - Second Option",
        "Esc - Go Back"
    ],
    4: [
        "Esc - Cancel Next Turn"
    ]
}


possiblePolicies = [{
    "prompt": "A citizen in CITY has been caught spreading mass false information about the Overlords. Should the citizen be punished, or should they be allowed to voice their concerns?",
    "options": [
        {
            "name": "Punish",
            "loyalty": 5,
            "happiness": -5,
            "intelligence": 2
        },
        {
            "name": "Allow",
            "loyalty": -2,
            "happiness": 2,
            "intelligence": -1
        }
    ]
    
},
{
    "prompt": "A citizen from CITY stowed away on one of the Overlord's ships travelling back to their planet. Should the citizen be killed and made an example of or treated to and brought back?",
    "options": [
        {
            "name": "Killed",
            "loyalty": -4,
            "happiness": -2,
            "intelligence": 6
        },
        {
            "name": "Treated",
            "loyalty": 3,
            "happiness": 3,
            "intelligence": -2
        }
    ]
    
},
{
    "prompt": "There are plans of an insurrection from the opposition of the Overlords. Should the oppositionists be given a fair trial or removed immediately?",
    "options": [
        {
            "name": "Tried",
            "loyalty": -2,
            "happiness": 8,
            "intelligence": 4
        },
        {
            "name": "Killed",
            "loyalty": 4,
            "happiness": -5,
            "intelligence": -2
        }
    ]
    
}]
currentPolicy = None
currentPolicyLines = []

def determineLines(text):
    words = text.split(" ")
    lines = []
    currentLine = ""
    while len(words) > 0:
        w = words.pop(0)
        currentLine += w + " "
        if(len(currentLine) >= 45):
            lines.append(currentLine)
            currentLine = ""
    if(not currentLine == ""):
        lines.append(currentLine)
    return lines

def determinePolicyLines():
    global currentPolicyLines
    currentPolicyLines = determineLines(currentPolicy["prompt"])
    
    


currentCity = cities[0]
currentSideMenu = 0
currentCityOption = 0

currentSelectionCategory = 0
# 0 - Cities
# 1 - Side Menu
# 2 - City Options
# 3 - Policy

moveTimer = 0
delaySelect = 0

# Game Stats
turn = 0
loyalty = 15 # 100: WIN, 0: LOSE
minds = 0 # 100: WIN
rage = 0 # 100: LOSE

actionsLeft = 3
actionMarker = pygame.image.load("assets/actionToken.png")


nextTurnHold = 0

while True:
    if(gameState == "won"):
        
        DISPLAY.blit(winBg, (0, 0))
        DISPLAY.blit(FONT_LARGE.render("You Won!", True, (255, 255, 255)), (500, 300))
        DISPLAY.blit(FONT_SMALL.render("On Turn " + str(turn), True, (255, 255, 255)), (550, 350))
        
        
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
    elif(gameState == "game"):
        DISPLAY.blit(background, (-100, 0))
        DISPLAY.blit(dimBg, (0, 0))
        events = pygame.event.get()
        for event in events:
            if(event.type == pygame.QUIT):
                pygame.quit()
            if(event.type == pygame.MOUSEBUTTONDOWN):
                
                
                pos = pygame.mouse.get_pos()
                if(policyMarkerRect.collidepoint(pos)):
                    currentSelectionCategory = 3
                    if(currentPolicy == None):
                        currentPolicy = random.choice(possiblePolicies)
                        determinePolicyLines()
                if(globalMarkerRect.collidepoint(pos)):
                    currentSelectionCategory = 1
                    currentSideMenu = 0
                elif(nextButtonRect.collidepoint(pos)):
                    if(not currentSelectionCategory == 4 and actionsLeft > 0):
                        currentSelectionCategory = 4
                    else:
                        currentSelectionCategory = 0
                        turn += 1
                        for c in cities:
                            
                            addPop = random.randint(-1, 2)
                            sadnessPopModifier = (c.happiness+20)/50
                            addPop += sadnessPopModifier
                            addPop = round(addPop)
                            c.population += addPop
                            if(c.population > c.max_population):
                                c.population = c.max_population
                            elif(c.population < 1):
                                c.population = 1
                            
                            for m in list(c.cityOptions.keys()):
                                c.cityOptions[m][0] -= 1
                                if(c.cityOptions[m][0] < 0):
                                    c.cityOptions[m][0] = 0
                                    
                            loyaltyScore = round((c.happiness-40)/15)
                            c.loyalty += loyaltyScore - (actionsLeft*.25)
                            if(c.happiness > 60):
                                intelligence += 0.3
                            elif(c.happiness < 20):
                                intelligence -= 0.3
                            if(c.loyalty > 60):
                                intelligence += 0.3
                                c.happiness += 1
                            elif(c.loyalty < 30):
                                c.happiness -= 1
                                
                            c.loyalty = round(c.loyalty,1)
                            c.happiness = round(c.happiness,1)
                        # prevent from accidently going into further turn
                        nextTurnHold = -10000
                        actionsLeft = 3
                        currentPolicy = None
        
        # KEYBOARD
        
        keys = pygame.key.get_pressed()
        
        if(keys[pygame.K_RETURN]):
            nextTurnHold += 1
            pygame.mixer.Channel(1).play(selectSound)
            if(nextTurnHold > 60):
                # NEXT TURN
                currentSelectionCategory = 0
                turn += 1
                for c in cities:
                    addPop = random.randint(-1, 2)
                    sadnessPopModifier = (c.happiness+20)/50
                    addPop += sadnessPopModifier
                    addPop = round(addPop)
                    c.population += addPop
                    if(c.population > c.max_population):
                        c.population = c.max_population
                    elif(c.population < 1):
                        c.population = 1
                    
                    for m in list(c.cityOptions.keys()):
                        c.cityOptions[m][0] -= 1
                        if(c.cityOptions[m][0] < 0):
                            c.cityOptions[m][0] = 0
                            
                    loyaltyScore = round((c.happiness-40)/15)
                    c.loyalty += loyaltyScore - (actionsLeft*.25)
                    if(c.happiness > 60):
                        intelligence += 0.3
                    elif(c.happiness < 20):
                        intelligence -= 0.3
                    if(c.loyalty > 60):
                        intelligence += 0.3
                        c.happiness += 1
                    elif(c.loyalty < 30):
                        c.happiness -= 1
                    
                    c.loyalty = round(c.loyalty,1)
                    c.happiness = round(c.happiness,1)
                # prevent from accidently going into further turn
                nextTurnHold = -10000
                actionsLeft = 3
                currentPolicy = None
                    
        else:
            nextTurnHold = 0

        
        
        if(keys[pygame.K_q] and delaySelect > 10):
            # GOTO Side Menu
            delaySelect = 0
            currentSelectionCategory = 1
            pygame.mixer.Channel(1).play(selectSound)
            currentSideMenu = 0
        elif(keys[pygame.K_ESCAPE]):
            currentSelectionCategory = 0
            pygame.mixer.Channel(0).play(moveSound)
        elif(keys[pygame.K_p] and delaySelect > 10):
            pygame.mixer.Channel(1).play(selectSound)
            delaySelect = 0
            currentSelectionCategory = 3
            if(currentPolicy == None):
                currentPolicy = random.choice(possiblePolicies).copy()
                if("CITY" in currentPolicy["prompt"]):
                    ranCity = random.choice(cities)
                    currentPolicy["prompt"] = currentPolicy["prompt"].replace("CITY", ranCity.name)
                determinePolicyLines()

        if(currentSelectionCategory == 0):
            if((keys[pygame.K_w] or keys[pygame.K_UP]) and moveTimer > 5):
                moveTimer = 0
                # try go up
                
                if(citiesSelectMap[currentCity.name][2] != ""):
                    for c in cities:
                        if(c.name == citiesSelectMap[currentCity.name][2]):
                            currentCity = c
                            pygame.mixer.Channel(0).play(moveSound)
                            break
            elif((keys[pygame.K_s] or keys[pygame.K_DOWN]) and moveTimer > 5):
                moveTimer = 0
                # try go down
                if(citiesSelectMap[currentCity.name][3] != ""):
                    for c in cities:
                        if(c.name == citiesSelectMap[currentCity.name][3]):
                            currentCity = c
                            pygame.mixer.Channel(0).play(moveSound)
                            break
            elif((keys[pygame.K_a] or keys[pygame.K_LEFT]) and moveTimer > 5):
                moveTimer = 0
                # try go left
                if(citiesSelectMap[currentCity.name][0] != ""):
                    for c in cities:
                        if(c.name == citiesSelectMap[currentCity.name][0]):
                            currentCity = c
                            pygame.mixer.Channel(0).play(moveSound)
                            break
            elif((keys[pygame.K_d] or keys[pygame.K_RIGHT]) and moveTimer > 5):
                moveTimer = 0
                # try go right
                if(citiesSelectMap[currentCity.name][1] != ""):
                    for c in cities:
                        if(c.name == citiesSelectMap[currentCity.name][1]):
                            currentCity = c
                            pygame.mixer.Channel(0).play(moveSound)
                            break
            elif(keys[pygame.K_SPACE] and delaySelect > 20):
                # goto city options
                pygame.mixer.Channel(1).play(selectSound)
                currentSelectionCategory = 2
                currentCityOption = 0
                delaySelect = 0
                
        elif(currentSelectionCategory == 1):
            # get length of dictionary
            if((keys[pygame.K_w] or keys[pygame.K_UP]) and moveTimer > 5):
                moveTimer = 0
                currentSideMenu -= 1
                pygame.mixer.Channel(0).play(moveSound)
                if(currentSideMenu < 0):
                    currentSideMenu = len(sideMenuOptions) - 1
            elif((keys[pygame.K_s] or keys[pygame.K_DOWN]) and moveTimer > 5):
                moveTimer = 0
                currentSideMenu += 1
                pygame.mixer.Channel(0).play(moveSound)
                if(currentSideMenu > len(sideMenuOptions) - 1):
                    currentSideMenu = 0
            elif(keys[pygame.K_SPACE] and delaySelect > 20 and actionsLeft > 0):
                action = list(sideMenuOptions.keys())[currentSideMenu]
                canPerform = True
                
                if(sideMenuOptions[action][0] == 0):
                    # can use
                    pygame.mixer.Channel(1).play(selectSound)
                    if(action == "Make Public Statement"):
                        reception = 0
                        for c in cities:
                            reception += (c.happiness-40)/15
                            c.loyalty += (c.happiness-40)/15
                            c.happiness += 1
                        if(reception > 0):
                            intelligence += 0.8
                        else:
                            intelligence -= 0.4
                        delaySelect = 0
                        actionsLeft -= 1
                        sideMenuOptions[action][0] = sideMenuOptions[action][1]
                    elif(action == "Appoint New Leader"):
                        reception = 0
                        for c in cities:
                            reception += -(c.loyalty-70)/15
                            c.happiness = -(c.loyalty-70)/15
                            c.loyalty += 1
                        if(reception > 0):
                            intelligence += 0.5
                        else:
                            intelligence -= 0.2
                        delaySelect = 0
                        actionsLeft -= 1
                        sideMenuOptions[action][0] = sideMenuOptions[action][1]
                    elif(action == "Make New Law"):
                        for c in cities:
                            c.happiness -= 1
                            c.loyalty += 1
            
        elif(currentSelectionCategory == 2):
            if((keys[pygame.K_w] or keys[pygame.K_UP]) and moveTimer > 5):
                moveTimer = 0
                currentCityOption -= 1
                pygame.mixer.Channel(0).play(moveSound)
                if(currentCityOption < 0):
                    currentCityOption = len(currentCity.cityOptions) - 1
            elif((keys[pygame.K_s] or keys[pygame.K_DOWN]) and moveTimer > 5):
                moveTimer = 0
                currentCityOption += 1
                pygame.mixer.Channel(0).play(moveSound)
                if(currentCityOption > len(currentCity.cityOptions) - 1):
                    currentCityOption = 0
                    
            if(keys[pygame.K_SPACE] and delaySelect > 20 and actionsLeft > 0):
                # submit action
                action = list(currentCity.cityOptions.keys())[currentCityOption]
                canPerform = True
                if(currentCity.cityOptions[action][0] == 0):
                    pygame.mixer.Channel(1).play(selectSound)
                    if action == "Send Ship":
                        if(currentCity.occupied == False):
                            currentCity.occupied = True
                            currentSelectionCategory = 0
                            currentCity.cityOptions[action][0] = currentCity.cityOptions[action][1]
                            currentCity.loyalty += round(currentCity.loyalty*0.1)
                            currentCity.happiness -= round(currentCity.happiness*0.1)
                            delaySelect = 0
                            actionsLeft -= 1
                    elif action == "Retrive Ship":
                        if(currentCity.occupied == True):
                            currentCity.occupied = False
                            currentSelectionCategory = 0
                            currentCity.cityOptions[action][0] = currentCity.cityOptions[action][1]
                            currentCity.loyalty -= round(currentCity.loyalty*0.1)
                            currentCity.happiness += round(currentCity.happiness*0.1)
                            delaySelect = 0
                            actionsLeft -= 1
                    elif action == "Host Knowledge Festival":
                        
                        currentCity.loyalty += 2
                        currentCity.happiness += 4
                        intelligence += (currentCity.happiness-20)/50
                        currentSelectionCategory = 0
                        currentCity.cityOptions[action][0] = currentCity.cityOptions[action][1]
                        delaySelect = 0
                        actionsLeft -= 1
                    elif action == "Gage Loyalty & Happiness":
                        
                        currentCity.loyalty += 1
                        currentCity.happiness += 1
                        
                        currentCity.knownLoyalty = currentCity.loyalty
                        currentCity.knownHappiness = currentCity.happiness
                        
                        print("Loyalty: " + str(currentCity.loyalty))
                        print("Happiness: " + str(currentCity.happiness))
                        currentSelectionCategory = 0
                        currentCity.cityOptions[action][0] = currentCity.cityOptions[action][1]
                        delaySelect = 0
                        actionsLeft -= 1
                    elif action == "Denounce City":
                        currentCity.loyalty += 3
                        currentCity.happiness -= 3
                        currentSelectionCategory = 0
                        currentCity.cityOptions[action][0] = currentCity.cityOptions[action][1]
                        delaySelect = 0
                        actionsLeft -= 1
                        
                        
                        
        elif(currentSelectionCategory == 3):
            # get length of dictionary
            if(keys[pygame.K_LEFT] and moveTimer > 5 and actionsLeft > 0):
                # first option
                pygame.mixer.Channel(1).play(selectSound)
                adjustLoyalty = currentPolicy["options"][0]["loyalty"]
                adjustHappiness = currentPolicy["options"][0]["happiness"]
                adjustIntelligence = currentPolicy["options"][0]["intelligence"]
                intelligence += adjustIntelligence * ((c.happiness-20) / 50)
                moveTimer = 0
                totalPopulation = 0
                for c in cities:
                    totalPopulation += c.population
                for c in cities:
                    c.loyalty += adjustLoyalty * (c.population / totalPopulation)
                    c.happiness += adjustHappiness * (c.population / totalPopulation)
                    c.loyalty = round(c.loyalty, 1)
                    c.happiness = round(c.happiness, 1)
                    #c.intelligence += adjustIntelligence / len(cities)
                
                currentPolicy = None
                currentSelectionCategory = 0
                actionsLeft -= 1
                
                currentPolicy = None
                
                pass
            elif(keys[pygame.K_RIGHT] and moveTimer > 5 and actionsLeft > 0):
                # second option
                pygame.mixer.Channel(1).play(selectSound)
                adjustLoyalty = currentPolicy["options"][1]["loyalty"]
                adjustHappiness = currentPolicy["options"][1]["happiness"]
                adjustIntelligence = currentPolicy["options"][1]["intelligence"]
                moveTimer = 0
                intelligence += adjustIntelligence * ((c.happiness-20) / 50)
                for c in cities:
                    c.loyalty += adjustLoyalty / len(cities)
                    c.happiness += adjustHappiness / len(cities)
                    #c.intelligence += adjustIntelligence / len(cities)
                
                currentPolicy = None
                currentSelectionCategory = 0
                actionsLeft -= 1
                
                currentPolicy = None
                
                pass
            
        
            
        moveTimer += 1
        delaySelect += 1
        
        
        # DRAWING
        for c in cities:
            DISPLAY.blit(c.image, (c.x, c.y))
            
            if(currentSelectionCategory == 0 and c.name == currentCity.name):
                DISPLAY.blit(selector.image, (currentCity.x, currentCity.y))
            DISPLAY.blit(populationMarker, (c.x, c.y-40))
            if(c.loyalty == c.knownLoyalty):
                DISPLAY.blit(loyaltyMarker, (c.x-45, c.y+50))
            else:
                DISPLAY.blit(loyaltyMarkerG, (c.x-45, c.y+50))
            if(c.happiness == c.knownHappiness):
                DISPLAY.blit(happinessMarker, (c.x+45, c.y+50))
            else:
                DISPLAY.blit(happinessMarkerG, (c.x+45, c.y+50))
            if(c.name == currentCity.name):
                DISPLAY.blit(FONT_MEDIUM.render(c.name, True, (255, 255, 0)), (c.x+10, c.y - 30))
            else:
                DISPLAY.blit(FONT_MEDIUM.render(c.name, True, (0, 0, 0)), (c.x+10, c.y - 20))
            DISPLAY.blit(FONT_SMALL.render(str(c.population), True, (255, 255, 255)), (c.x+c.rect.width/2-7, c.y + c.rect.height/2-50))
            DISPLAY.blit(FONT_SMALL.render(str(c.knownLoyalty) + "%", True, (255, 255, 255)), (c.x+c.rect.width/2-52, c.y + c.rect.height/2+40))
            DISPLAY.blit(FONT_SMALL.render(str(c.knownHappiness) + "%", True, (255, 255, 255)), (c.x+c.rect.width/2+38, c.y + c.rect.height/2+40))
        
        
        
        DISPLAY.blit(policyMarker,policyMarkerRect)
        DISPLAY.blit(globalMarker,globalMarkerRect)
        
        DISPLAY.blit(intelligenceBar, [940,670])
        intelligence = round(intelligence, 1)
        DISPLAY.blit(FONT_SMALL.render("Turn " + str(turn), True, (255, 255, 255)), (1005, 700))
        DISPLAY.blit(FONT_MEDIUM.render(str(intelligence) + "%", True, (255, 255, 255)), (1005, 715))
        
        
        
        if(currentSelectionCategory == 0):
            nextButtonRect.center = [600, 720]
            DISPLAY.blit(nextButton,nextButtonRect)
        elif(currentSelectionCategory == 1):
            DISPLAY.blit(dimBg, (0, 0))
            DISPLAY.blit(sideMenu.image, (sideMenu.x, sideMenu.y))
            # loop through each key in sideMenuOptions
            for i, key in enumerate(sideMenuOptions):
                if(i == currentSideMenu):
                    if(sideMenuOptions[key][0] == 0):
                        DISPLAY.blit(FONT_MEDIUM.render(key, True, (255, 255, 0)), (20, sideMenu.y + 40 + i*30))
                    else:
                        DISPLAY.blit(FONT_MEDIUM.render(key + " (" + str(sideMenuOptions[key][0]) +  ")", True, (255, 0, 0)), (20, sideMenu.y + 40 + i*30))
                else:
                    if(sideMenuOptions[key][0] == 0):
                        DISPLAY.blit(FONT_MEDIUM.render(key, True, (255, 255, 255)), (20, sideMenu.y + 40 + i*30))
                    else:
                        DISPLAY.blit(FONT_MEDIUM.render(key + " (" + str(sideMenuOptions[key][0]) +  ")", True, (150, 150, 150)), (20, sideMenu.y + 40 + i*30))
            DISPLAY.blit(FONT_SMALL.render("ESC to Exit...", True, (150, 150, 150)), (20, sideMenu.rect.bottom - 55))
        elif(currentSelectionCategory == 2):
            DISPLAY.blit(dimBg, (0, 0))
            DISPLAY.blit(titleMenu.image, titleMenu.rect)
            DISPLAY.blit(FONT_LARGE.render(currentCity.name, True, (255, 255, 255)), (titleMenu.rect.left + 60, titleMenu.rect.top + 40))
            for i, key in enumerate(currentCity.cityOptions):
                if(i == currentCityOption):
                    if(currentCity.cityOptions[key][0] == 0):
                        DISPLAY.blit(FONT_MEDIUM.render(key, True, (255, 255, 0)), (titleMenu.rect.left + 40, titleMenu.rect.top + 120 + i*30))
                    else:
                        DISPLAY.blit(FONT_MEDIUM.render(key + " (" + str(currentCity.cityOptions[key][0]) +  ")", True, (255, 0, 0)), (titleMenu.rect.left + 40, titleMenu.rect.top + 120 + i*30))
                else:
                    if(currentCity.cityOptions[key][0] == 0):
                        DISPLAY.blit(FONT_MEDIUM.render(key, True, (255, 255, 255)), (titleMenu.rect.left + 40, titleMenu.rect.top + 120 + i*30))
                    else:
                        DISPLAY.blit(FONT_MEDIUM.render(key + " (" + str(currentCity.cityOptions[key][0]) +  ")", True, (150, 150, 150)), (titleMenu.rect.left + 40, titleMenu.rect.top + 120 + i*30))
            DISPLAY.blit(FONT_SMALL.render("ESC to Exit...", True, (150, 150, 150)), (titleMenu.rect.left + 60, titleMenu.rect.bottom - 55))
        elif(currentSelectionCategory == 3):
            DISPLAY.blit(dimBg, (0, 0))
            DISPLAY.blit(titleMenu.image, titleMenu.rect)
            DISPLAY.blit(FONT_LARGE.render("Determine Policy", True, (255, 255, 255)), (titleMenu.rect.left + 60, titleMenu.rect.top + 40))
            for l in range(len(currentPolicyLines)):
                DISPLAY.blit(FONT_SMALL.render(currentPolicyLines[l], True, (255, 255, 255)), (titleMenu.rect.left + 40, titleMenu.rect.top + 120 + l*20))
            DISPLAY.blit(leftarrow, (titleMenu.rect.left + 60, titleMenu.rect.bottom - 170))
            DISPLAY.blit(rightarrow, (titleMenu.rect.left + 220, titleMenu.rect.bottom - 170))
            DISPLAY.blit(FONT_MEDIUM.render(currentPolicy["options"][0]["name"], True, (100, 100, 255)), (titleMenu.rect.left + 80, titleMenu.rect.bottom - 120))
            DISPLAY.blit(FONT_MEDIUM.render(currentPolicy["options"][1]["name"], True, (100, 100, 255)), (titleMenu.rect.left + 240, titleMenu.rect.bottom - 120))
            DISPLAY.blit(FONT_SMALL.render("ESC to Exit...", True, (150, 150, 150)), (titleMenu.rect.left + 60, titleMenu.rect.bottom - 55))
        elif(currentSelectionCategory == 4):
            DISPLAY.blit(dimBg, (0, 0))
            DISPLAY.blit(titleMenu.image, titleMenu.rect)
            DISPLAY.blit(FONT_LARGE.render("Are you sure?", True, (255, 255, 255)), (titleMenu.rect.left + 60, titleMenu.rect.top + 40))
            
            lines = determineLines("You still have " + str(actionsLeft) + " actions left. Skipping these and going to the next turn will result in a penalty of " + str(actionsLeft*.25) + " loyalty.")
            
            for l in range(len(lines)):
                DISPLAY.blit(FONT_SMALL.render(lines[l], True, (255, 255, 255)), (titleMenu.rect.left + 40, titleMenu.rect.top + 120 + l*20))
            
            nextButtonRect.center = [600, titleMenu.rect.bottom - 200]
            
            DISPLAY.blit(nextButton,nextButtonRect)
            DISPLAY.blit(FONT_SMALL.render("ESC to Cancel...", True, (150, 150, 150)), (titleMenu.rect.left + 60, titleMenu.rect.bottom - 55))
        for i in range(0, actionsLeft):
            DISPLAY.blit(actionMarker, (1116-(i*74), 20))
        
        if(nextTurnHold > 0):
            fillS = pygame.Surface(((1200/60)*nextTurnHold, 20))
            fillS.fill((0,255,0))
            DISPLAY.blit(fillS, (0, 0))
        elif(actionsLeft == 0):
            fillS = pygame.Surface((1200, 20))
            fillS.fill((255,255,0))
            DISPLAY.blit(fillS, (0, 0))
            DISPLAY.blit(FONT_SMALL.render("You are out of actions... Press ENTER to go to next turn!", True, (180, 180, 0)), (300, 5))
        
        if(currentSelectionCategory == 2):
            o = 0
            for option in optionsList[currentSelectionCategory]:
                if(not "Space" in option or list(currentCity.cityOptions.keys())[currentCityOption][0] == 0):
                    DISPLAY.blit(controlItem, (960, 120 + o*50))
                    DISPLAY.blit(FONT_SMALL.render(option, True, (255, 255, 255)), (974, 132 + o*50))
                    o += 1
        else:
            o = 0
            for option in optionsList[currentSelectionCategory]:
                DISPLAY.blit(controlItem, (960, 120 + o*50))
                DISPLAY.blit(FONT_SMALL.render(option, True, (255, 255, 255)), (974, 132 + o*50))
                o += 1
        if(intelligence >= 100):
            gameState = "won"
        elif(intelligence <= 0):
            intelligence = 0
        
    
    
    
    
    pygame.display.update()
    CLOCK.tick(60)
