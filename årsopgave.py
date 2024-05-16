import math
import arcade
import arcade.gui
import random
import pyautogui
import matplotlib.pyplot as plt




SKÆRM_BREDDE = 1500
SKÆRM_HØJDE = 800
#Laver variablen her, så den kan blive tilgåeet steder ud over funktionen
skærm= None
#Variable til tid plotted
#Variabler til farver
CELLE_FARVE=(166, 71, 3)
VIRUS_FARVE=(0, 255, 0)
VACCINE_FARVE=arcade.color.DARK_BLUE
VACCINET_CELLE_FARVE=(204, 191, 16)
INAKTIV_VIRUS_FARVE=(25, 212, 156)
SPISE_LYD=arcade.load_sound("mixkit-game-ball-tap-2073.wav")
DØDE_LYD=arcade.load_sound("mixkit-small-hit-in-a-game-2072.wav")


class VaccineKnap(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        tilføj_vaccine()

#En klasse til en knap til at genstarte
class Genstart_knap(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        genstart_fun()
#Klasse tila t visse graf
class Graf_knap(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        hvis_graf()

def genstart_fun():
    #Sætter værdie til nogle prompts
    skærm.mængede_celler = antal_af_x_prompt("Celler")
    skærm.mængede_viruser = antal_af_x_prompt("virusser")

    skærm.setup()

#Funktion til at vise en graf
def hvis_graf():
    #Laver try, fordi det er først efter 1sekund at de her vil har værdier
    try:
        graf(skærm.xlist,skærm.graf_lister,skærm.graf_lister_navn)
    except:
        print("Vent lige et sekund")
    
    
def tilføj_vaccine():
    skærm.vaccinere_celler()


#En klasse til cirkler, som bliver parent class til de forskellige
class Cirkel:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 8
        self.x_hastighed = 0
        self.y_hastighed = 0

# En klasse til viruser


class Virus(Cirkel):
    def __init__(self):

        super().__init__()
        self.tid_i_live = 0
        self.farve = VIRUS_FARVE
        self.max_tid = 15
        self.mæt = False
        self.tid_siden_spist=0
        self.in_aktiv=False

    def updater(self, delta_tid):

        # Sætter værdierne til hvad en funktion er, som holder styr på dens lokation
        self.x, self.y, self.x_hastighed, self.y_hastighed = bounce_væg(self.x, self.y, self.x_hastighed,
                                                                        self.y_hastighed,self.radius)
        # Stiger hvor lang tid den har levet
        self.tid_i_live += delta_tid
        if self.mæt==True:
            self.tid_siden_spist+=delta_tid
        if self.tid_siden_spist>=5:
            self.tid_siden_spist=0

    # Methode til at tegne det
    def tegn(self):
        arcade.draw_circle_filled(center_x=self.x, center_y=self.y, radius=self.radius, color=self.farve)


# En klasse til cellere
class Celler(Cirkel):
    def __init__(self):
        # Giver nogen værdier der bliver ændret senere
        super().__init__()
        self.farve = CELLE_FARVE
        self.vacine_skyd=0
        self.radius_af_vacine_skyd=2

    # Funktion når den skal blive opdateredet
    def updater(self):
        # Præcis det samme som med virus
        self.x, self.y, self.x_hastighed, self.y_hastighed = bounce_væg(self.x, self.y, self.x_hastighed,
                                                                        self.y_hastighed,self.radius)

    def tegn(self):
        # Tegner cirkelerne
        arcade.draw_circle_filled(center_x=self.x, center_y=self.y, radius=self.radius, color=self.farve)
        #Der er intet galt med koden nede under, den skader bare perfermence for meget
        """
        #Tegner små vaccine prikker til at være hvor mange der er tilbage
        for i in range(1,self.vacine_skyd+1):
            #Laver en vinkel
            vinkel=math.radians(i*(360/self.vacine_skyd))
            #placerden den det rigte sted
            arcade.draw_circle_filled(center_x=self.x+(self.radius-self.radius_af_vacine_skyd-1)*math.cos(vinkel),
                                      center_y=self.y+(self.radius-self.radius_af_vacine_skyd-1)*math.sin(vinkel),
                                      radius= self.radius_af_vacine_skyd,color=VACCINE_FARVE)
            """


#En klasse til vacinerne
class Vaccine(Cirkel):
    def __init__(self):
        super().__init__()
        self.farve = VACCINE_FARVE
    #Methode til at updater
    def update(self):
        self.x+=self.x_hastighed
        self.y += self.y_hastighed

    #Methode til at tegne
    def tegn(self):
        arcade.draw_circle_filled(center_x=self.x, center_y=self.y, radius=self.radius, color=self.farve)


# En klasse til vindues
class Vindue(arcade.Window):
    def __init__(self, widt, height, titel):

        super().__init__(widt, height, titel)
        #Sætter nogle værdier
        self.mængede_viruser = 1
        self.mængede_celler = 100
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        vaccine_knap = VaccineKnap(text="Vaccine(T)", width=200, y=-200)
        genstart_knap = Genstart_knap(text="Genstart(G)", width=200, y=-200)
        graf_knap=Graf_knap(text="Vis graf(V)",widt=200,y=-200)
        self.v_box.add(genstart_knap)
        self.v_box.add(vaccine_knap)
        self.v_box.add(graf_knap)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )



        # Sætter en baground
        arcade.set_background_color((0, 0, 0))
        # Starter en render
        arcade.start_render()

        # En metode til at sæt alting up

    def setup(self):
        #Værdier til at lave grafer
        self.time = 0
        self.i = 0
        self.xlist = []
        self.ylist = []
        self.ylist2 = []
        self.ylist3 = []
        self.ylist4 = []


        # Laver de forskellige lister, som der skal være objekter inde i
        self.liste_af_virus = []
        self.liste_af_celler = []
        self.liste_af_vaccine_skyd=[]
        self.liste_af_jagtedet_viruser=[]



        #self.mængede_celler=100
        #self.mængede_viruser=1
        # Listerne bliver sat lige med en liste, der bliver udregnet i en funktion
        self.liste_af_virus = lav_forskellige_bolde(self.mængede_viruser, (2, 3), (2, 3), Virus, self.liste_af_virus)
        self.liste_af_celler = lav_forskellige_bolde(self.mængede_celler, (1, 2,), (1, 2), Celler, self.liste_af_celler)

        # Laver en liste af de forsekllie lister
        self.liste_af_lister = [self.liste_af_virus, self.liste_af_celler]
        # Tilføjer dem til scenen

    # Laver en funktion, som er update der kommer til at updater de forskellige ting
    def update(self, delta_tid):
        # Ændre værdien i forhold til en funktion der updater en virus,laver en ny liste, for at sikre at den bliver ændret i listen
        self.ny_liste_af_virus = updater_virus(self.liste_af_virus, delta_tid)
        self.ny_liste_af_celler = updater_celler(self.liste_af_celler, delta_tid)
        self.time +=1
        if (self.time % 60 == 0):
            self.i += 1
            self.xlist.append(self.i)
            self.ylist.append(len(self.liste_af_celler))
            self.ylist2.append(len(self.liste_af_virus))
            self.graf_lister=[self.ylist,self.ylist2]
            self.graf_lister_navn=["Celler","Virusser"]

        # Der er problemer med at sætte en list til en anden list
        # Så problemerne bliver løst ved at clear den og så extender listend
        # Looper igennem listen og clear den
        for liste in self.liste_af_lister:
            liste.clear()
        self.liste_af_virus.extend(self.ny_liste_af_virus)
        self.liste_af_celler.extend(self.ny_liste_af_celler)

        #laver et for loop til at checke om de er inde i hinanden
        #For loppedet giver både index værdien og hvad der er på dens postion
        for virus in self.liste_af_virus:
            #If statement til at sikre at det ikke kan ske hvis de er inaktiv
            if virus.in_aktiv is False:
                for celle in self.liste_af_celler:
                    #Checker hvis de overlapper
                    #Ved hjælp af den her (R0 - R1) ^ 2 <= (x0 - x1) ^ 2 + (y0 - y1) ^ 2 <= (R0 + R1) ^ 2
                    if (virus.radius-celle.radius)**2<=(virus.x-celle.x)**2 +(virus.y-celle.y)**2 <=(virus.radius+celle.radius)**2:
                       #Fjerner cellen der rammer en virus
                        self.liste_af_celler.remove(celle)
                        arcade.play_sound(SPISE_LYD)

                        virus.mæt=True

        #If statement til at checke afstand mellem de vacinerdet og virusserne
        for celle in self.liste_af_celler:
            for virus in self.liste_af_virus:
                if celle.vacine_skyd>0 and math.sqrt((celle.x-virus.x)**2+(celle.y-virus.y)**2)<=150 and virus not in self.liste_af_jagtedet_viruser:

                    #Grunden til at det er en tubel, er for at have en virus de jagter
                    self.liste_af_vaccine_skyd.append((Vaccine(),virus))

                    self.liste_af_vaccine_skyd[-1][0].x=celle.x
                    self.liste_af_vaccine_skyd[-1][0].y = celle.y

                    #Ændre mængede af vacine skyd der er
                    celle.vacine_skyd-=1
                    #Tilføjer virus til den her liste for at sikre at der ikke er flere end en der jagter dem.
                    #De bliver ikke fjernet for at sikre at en inaktiv virus ikke bliver jagtedet
                    self.liste_af_jagtedet_viruser.append(virus)



        #For loop til at ændre ders position
        for tuple in self.liste_af_vaccine_skyd:
            #Checker om de har ramt hinanden
            if (tuple[0].radius-tuple[1].radius)**2<=(tuple[0].x-tuple[1].x)**2 +(tuple[0].y-tuple[1].y)**2 <=(tuple[0].radius+tuple[1].radius)**2:
                #Fjerner object
                self.liste_af_vaccine_skyd.remove(tuple)
                #Ændre virus værdien
                tuple[1].in_aktiv=True
                #Ændre farven på virusen
                tuple[1].farve=INAKTIV_VIRUS_FARVE
            #Sikre at virus stadig ekister
            elif tuple[1] in self.liste_af_virus:
                #Updater virusen
                tuple[0].x_hastighed,tuple[0].y_hastighed=updater_vaccine_skyd(tuple[1].x,tuple[1].y,tuple[0].x,tuple[0].y)
                #Updater virus
                tuple[0].update()
            else:
                #Fjerner skyden fra listen siden den har ramt dens mål
                self.liste_af_vaccine_skyd.remove(tuple)
                
                
    def on_key_press(self,key,modifiers):
        if key == arcade.key.T:
            tilføj_vaccine()
        if key == arcade.key.G:
            genstart_fun()
        if key == arcade.key.V:
            hvis_graf()



    # Funktion til når den tegner
    def on_draw(self):
        self.clear()
        self.manager.draw()

        # Køre igennem hvert element af listen
        for lister in self.liste_af_lister:
            # Køre de enkele objekter igennem af liste og tegner den
            for object in lister:
                object.tegn()
        for vacine_skyd in self.liste_af_vaccine_skyd:
            vacine_skyd[0].tegn()

        arcade.draw_text(text=f"Virusser:{len(self.liste_af_virus)}",start_x=0,start_y=SKÆRM_HØJDE-20)
        arcade.draw_text(text=f"Celler:{len(self.liste_af_celler)}",start_x=0,start_y=SKÆRM_HØJDE-40)

    #En funktion til at vacinere celler
    def vaccinere_celler(self):
        #Bruger index og len i stedet for det andet, siden kun det halve
        for i in range((len(self.liste_af_celler)//2)):
            self.liste_af_celler[i].vacine_skyd=4
            self.liste_af_celler[i].farve=VACCINET_CELLE_FARVE


# Laver en funktion til at updater alle intageoiner i en liste. Den tag listen og delta_tid
def updater_virus(liste, delta_tid):
    # Der skal blive lave en kopi for at undgå out of index error
    kopi_liste = liste.copy()
    # gøre igennem listen
    for værdi in liste:
        # Gøre methoden updater
        værdi.updater(delta_tid)
        # Fjener dem hvis du når up på max tid
        if værdi.tid_i_live >= værdi.max_tid:
            # Sætter listen til at være kopien
            kopi_liste.remove(værdi)
            arcade.play_sound(DØDE_LYD)
        if værdi.mæt:
            # Sætter timeren til nul
            værdi.tid_i_live = 0
            # Ændre mæt til at være falsk
            værdi.mæt = False
            # Laver en til
            kopi_liste.append(Virus())
            #Kopier værdien
            kopi_liste[-1].__dict__ = værdi.__dict__.copy()


            #Sikre at de ikke er den samme værdi
            while kopi_liste[-1].x_hastighed == værdi.x_hastighed or kopi_liste[-1].y_hastighed == værdi.y_hastighed:
                # Ændre værdinerne
                random_tal=random.randint(1,4)
                if random_tal==1:
                    kopi_liste[-1].x_hastighed *= -1
                    kopi_liste[-1].x_hastighed+=random.random()
                    kopi_liste[-1].y_hastighed+=random.random()*0.1
                elif random_tal==2:
                    kopi_liste[-1].y_hastighed*=-1
                    kopi_liste[-1].y_hastighed+=random.random()
                    kopi_liste[-1].x_hastighed += random.random() * 0.1
                elif random_tal==3:
                    kopi_liste[-1].y_hastighed *= -1
                    kopi_liste[-1].y_hastighed += random.random()
                    kopi_liste[-1].x_hastighed *= -1
                    kopi_liste[-1].x_hastighed += random.random()
                elif random_tal==4:
                    kopi_liste[-1].x_hastighed/random.random()


                # Returnerne kopi listen
    # print(len(kopi_liste))
    return kopi_liste


# Laver en funktion til at updater cellerne
def updater_celler(liste, delta_tid):
    # Der skal blive lave en kopi for at undgå out of index error
    kopi_liste = liste.copy()
    # gøre igennem listen
    for værdi in liste:
        # Gøre methoden updater
        værdi.updater()
    return kopi_liste


# En funktion til at beregne, hvor objekterne som bouncer på væggene er
def bounce_væg(x, y, x_hastighed, y_hastighed,radius):
    # If statement hvis den er ved borderen og radius, til at være når de rammer og ikke midten , og så ændre hastighed til det modsatte
    if x >= SKÆRM_BREDDE-radius or x <= radius:
        x_hastighed*=-1
    if y >= SKÆRM_HØJDE-radius or y <= radius:
        y_hastighed = -y_hastighed
    # Tilføjer hastighed til deres position
    x += x_hastighed
    y += y_hastighed
    # Retunere de forskellige værdier
    return x, y, x_hastighed, y_hastighed

#Funktion til at updater vaccine skyde position
def updater_vaccine_skyd(virus_x,virus_y,vaccine_x,vaccine_y):
    #Variable til ændringer af fart
    hastighed=4
    #If statements til at checke hvilken vej den skal går
    if vaccine_x>virus_x:
        vaccine_x_fart=-hastighed
    else:
        vaccine_x_fart=hastighed

    if vaccine_y > virus_y:
        vaccine_y_fart = -hastighed
    else:
        vaccine_y_fart = hastighed
    #returner hvor retningerne skal være
    return vaccine_x_fart,vaccine_y_fart


# En funktion til at lave de forskellige ting, som er cirkler forskell virus ved hjælp af en funktion, for at minimere koden der skal skrives
def lav_forskellige_bolde(antal_af_bolde, x_hastigheder, y_hastigheder, Klasse, liste):
    # Sætter min og max hastigheder
    x_min_hastighed, x_max_hastighed = x_hastigheder

    y_min_hastighed, y_max_hastighed = y_hastigheder
    # Laver loop til de forskellige
    for i in range(antal_af_bolde):
        # Tilføjer et objekt af en klasse til en list
        liste.append(Klasse())
        # Bruger 10 bare så de ikke er inde i væggen
        liste[i].x = random.randint(10, SKÆRM_BREDDE - 10)
        liste[i].y = random.randint(10, SKÆRM_HØJDE - 10)
        liste[i].x_hastighed = random.randint(x_min_hastighed, x_max_hastighed)
        liste[i].y_hastighed = random.randint(y_min_hastighed, y_max_hastighed)

    # Returner listen
    return liste

#Funktion til at lave en prompt
def antal_af_x_prompt(navn):
    værdi=None
    # Laver nogle prompt til hvor mange af de forskellige ting
    while værdi== None:
        værdi = pyautogui.prompt(text=f'Hvor mange {navn} skal der være?', title=f'{navn}')
        try:
            værdi= int(værdi)
        except:
            pyautogui.alert(text='Det er ikke en int', title='Fejl', button='OK')
            print(værdi)
            værdi = None
    return værdi

#En funktion til at gøre så, hvis de rammer en anden af en slag, så bouncer de tilbage
def bounce_back(liste):
    #Den virker ikke helt, og det var heller ikke mening at der skulle være der

    for element_1 in liste:
        for element_2 in liste:
            if element_1!=element_2:
                if (element_1.radius + element_2.radius)**2 >= (element_1.x - element_2.x)**2 + (element_1.y - element_2.y)**2:
                    element_1.x_hastighed*=-1
                    element_1.y_hastighed *= 1
                    element_2.x_hastighed *= 1
                    element_2.y_hastighed *= -1
    return liste

# Main funktion
def main():
    # Køre funktion der starter de forksellige ting
    start_up_fun()

def start_up_fun():
    # Sætter en alert til at infomere brugen hvad der sker
    pyautogui.alert("Det her er en simulation af cornavirus og celler.\n"
                    "De røde er celler\n"
                    "De grønne er viruser\n"
                    "De gule er celler der er blive vacineret\n"
                    "De cyane er inaktive virusser\n"
                    "De blå er vacinen\n"
                    "Tryk på vaccine knappen før at starte vaccinen\n"
                    "Tryk på genstart for at genstarte simulationen\n"
                    "Når virusen rammer en celle, så spiser den cellen, og den kan formere sig\n"
                    "Måden vaccien virker på er, når vaccine knappet bliver trygget på bliver halvdelen af cellerne vacinneret.\n"
                    "Når en celle bliver vaccinet vil den har nogle skyd, som jagter en virus, hvis virusen er inde for rækkevidte,"
                    "når en virus bliver ramt med en vaccine, så den kan hverken spise eller former sig ",title="Infomation")
    #Gøre den global så den kan blive ændret
    global skærm

    # Diffinere skærmen
    skærm = Vindue(SKÆRM_BREDDE, SKÆRM_HØJDE, "Simulation")

    skærm.setup()


    arcade.run()

#Funktion til at lave en graf
def graf(tid_liste,liste_af_lister,liste_af_navne):
    #For loop til at gøre igennem listerne
    for index,liste in enumerate(liste_af_lister):
        #Plotter linjerne
        plt.plot(tid_liste,liste,label=liste_af_navne[index])
    #navningeing af  akser
    plt.xlabel("Tid(s)")
    plt.ylabel("Antal af stoffer")
    plt.title("Graf af de forskellige ting")
    plt.legend()
    plt.show()



if __name__ == '__main__':
    main()
