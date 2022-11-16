import urllib.request
import json
#https://api.sr.se/api/documentation/v2/index.html
#https://api.sr.se/api/documentation/v2/generella_parametrar.html
#https://api.sr.se/api/documentation/v2/metoder/kanaler.html
#https://api.sr.se/api/documentation/v2/metoder/kanaler.html
import menu

def getChannels():
    api_url = "http://api.sr.se/api/v2/channels/?format=json"
    response = urllib.request.urlopen(api_url)
    answer = response.read()
    dictionary = json.loads(answer)
    channels = dictionary["channels"]
    #List Channels
    for channel in channels:
        print(channel['name'])
    return channels


if __name__ == '__main__':
    channels = getChannels()
    menu.menuOptions(channels)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

"""
Inlämning 1: Radioguiden
Introduktion och syfte
Målet är att sätta sig in i hur man använder ett JSON-API för att hämta information, samt hur man skriver ett Python-program för detta.

Uppgift
Uppgiften går ut på att skriva ett program som hämtar information från Sveriges Radios publika API och presenterar detta för användaren.
Ert program ska låta användaren hämta information från Sveriges Radio på ett enkelt sätt.
Programmet ska presentera en meny för användaren där man först kan välja en radiokanal.
När användaren har valt en radiokanal ska programmet skriva ut information om tablån för användaren.

Uppgiften är fri att göra lite lättare eller lite svårare, beroende på vilken ambition och kunskapsnivå man har. En enkel lösning kan hämta alla tillgängliga radiostationer, be användaren välja en, och sedan skriva ut information. En svårare kan till exempel låta användaren välja vilken information man vill se på olika sätt.

I mitt exempel nedan skriver jag ut de kommande 5 programmen. Detta val är upp till er. Ni kan välja att skriva ut hela programtablån, visa de kommande programmen, eller göra något mer avancerat.

Exempel
Menu – Choose a radio station:
1. P1




(…)

### Choice? 3
Showing the next 5 programs:
> 13:00 – P3 Nyheter
> 13:02 – P3 Med
> 16:00 – P3 Nyheter
> 16:02 – Eftermiddag i P3
> 18:30 – P3 Med
Referenser
https://api.sr.se/api/documentation/v2/index.html
https://www.postman.com/downloads/

Bedömning

I denna inlämning kan man få betygen G eller VG. Betyget grundas på följande kriterier:

    Självständigt arbete
    Struktur och funktion på programmets kod
    Svårigheten i de problem ni har valt att lösa
    Demonstration av att ni förstår bra arbetssätt och strukturerad kommunikation med API, samt hur man arbetar med JSON.

Jag tar hänsyn till alla punkterna ovanför när jag gör bedömning av betyg.

Redovisning
Källkoden ska vara pushad till ett eget repository på GitHub. Uppgiften ska genomföras i grupper om 1-3 personer. Fullständiga namn ska finnas med i README.md i repots main-branch (master).

Inlämningen sker genom att en länk till gitrepot skickas in av en av personerna i Omniway.
(De andra i gruppen behöver också skicka in, men det kan vara tomt.)
"""