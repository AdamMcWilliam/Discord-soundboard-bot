import sched, time, json

#setup timer
s = sched.scheduler(time.time, time.sleep)

def restoreMana(sc):
    with open('json/mana.json', 'r+') as manaFile:
        data = json.load(manaFile)

        for value in data:
            data[f"{value}"]['mana'] = 3
            

        manaFile.seek(0)
        json.dump(data, manaFile, indent=2)
        manaFile.close()
        print("mana restored")

        s.enter(60, 1, restoreMana, (sc,))

        

s.enter(10, 1, restoreMana, (s,))
s.run()

