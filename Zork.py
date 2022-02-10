from random import randint
import json

state = {
    "hp": 5,
    "position": "Menue",
    "dragonAlive": True,
    "swordAvail": True,
    "treasureAvail": True,
}


def show_invetory():
    print("Du hast %d Lebenspunkte." % state["hp"],
        "Du hast ein Schwert." if not state["swordAvail"] else "",
        "Du hast den Schatz." if not state["treasureAvail"] else "")


def speichern(mem, state):
    if mem == "S)":
        with open('save.json', 'w') as fp:
            fp.write(json.dumps(state))
        return {**state, "hp": 0}
    else:
        return state 


def spiel_menue(state):
    memory = input("Spielmenü:\n1) Neues Spiel\n2) Spiel laden\n-- ")
    if memory == "1)":
        print("Spiel wird gestartet...") #Zusatzidee
        return {**state, "position" : "Eingang"}
    elif memory == "2)":
        with open("save.json","r") as fp:
            newstate = json.loads("%s" %fp.read())
        return newstate
    return state


def room_eingang(state):
    print("Du befindest dich im EINGANG.",
        "Du kannst in die Schatzkammer oder zum Händler gehen.")
    show_invetory()
    if state["treasureAvail"]:
        memory = input("1) Schatzkammer\n2) Händler\nS) Speichern und Beenden\n-- ")
        if memory == "1)":
            return {**state, "position" : "Schatzkammer"}
        elif memory == "2)":
            return {**state, "position" : "Handler"}
        else:
            return speichern(memory, state)
    elif not state["treasureAvail"]:
        memory = input("1) Schatzkammer\n2) Händler\n3) Beenden\nS) Speichern und Beenden\n-- ")
        if memory == "1)":
            return {**state, "position" : "Schatzkammer"}
        elif memory == "2)":
            return {**state, "position" : "Handler"}
        elif memory == "3)":
            return {**state, "hp": 0}
        else:
            return speichern(memory, state)
    return state

def room_schatzk(state):
    print("Du befindest dich in der SCHATZKAMMER."
        " Du musst nun gegen den Drachen kämpfen,"
        " indem du würfelst oder du gehst zurück.")
    show_invetory()

    if state["dragonAlive"]:
        memory = input("1) Drachen bekämpfen\n2) Zurück\nS) Speichern und Beenden\n-- ")
        if memory == "1)":
            randomint = randint(1, 6)
            if ((randomint < 4 and not state["swordAvail"])
                    or (randomint == 6 and state["swordAvail"])):
                print("Du hast den Drachen besiegt!")
                return {**state, "dragonAlive": False}
            else:
                return {**state, "hp": state["hp"] - 1}
        elif memory == "2)":
            return {**state, "position" : "Eingang"}
        else:
            return speichern(memory, state)
    elif not state["dragonAlive"] and state["treasureAvail"]:
        memory = input("1) Schatz aufheben\n2) Zurück\nS) Speichern und Beenden\n-- ")
        if memory == "1)":
            print("Schatz aufgehoben!")
            return {**state, "treasureAvail": False}
        elif memory == "2)":
            return {**state, "position" : "Eingang"}
        else:
            return speichern(memory, state)
    elif not state["dragonAlive"] and not state["treasureAvail"]:
        if input("1) Zurück\nS) Speichern und Beenden\n-- ") == "1)":
            return {**state, "position" : "Eingang"}
        else:
            return speichern(memory, state)
    return state


def room_handler(state):
    print("Du befindest dich beim HÄNDLER.",
        " Du kannst ein Schwert für einen Lebenspunkt kaufen oder zurück"
        " gehen.")
    show_invetory()

    if state["swordAvail"]:
        memory = input("1) Schwert Kaufen\n2) Zurück\nS) Speichern und Beenden\n-- ")
        if memory == "1)":
            return {**state, "swordAvail": False, "hp": state["hp"] - 1}
        elif memory == "2)":
            return {**state, "position" : "Eingang"}
    else:
        memory = input("1) Zurück\nS) Speichern und Beenden\n-- ")
        if memory == "1)":
            return {**state, "position" : "Eingang"}
        else:
            return speichern(memory, state)
    return state


while state["hp"] > 0:
    if state["position"] == "Menue":
        state = spiel_menue(state)

    elif state["position"] == "Eingang":
        state = room_eingang(state)

    elif state["position"] == "Schatzkammer":
        state = room_schatzk(state)

    elif state["position"] == "Handler":
        state = room_handler(state)