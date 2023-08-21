import atlas

#list of tuples command, expected result
#(meaning of a message, not exact message. I don't remember them or too lazy to write them)
#cannot test command "exit" this way
commands = [("hello", "gretting"),
            ("show all", "empty list"),
            ("add record jony +380(44)978-60-13 ", "succesfully added"),
            ("phone jony", "+380(44)978-60-13 "),
            ("change jony +380(44)978-60-13 +380(44)978-60-14", "succesfully changed"),
            ("phone jony", "+380(44)978-60-14"),
            ("show all", "shows johny"),
            ("not a command", "unknown kommand"),
            ("ShOw AlL", "shows johny"),
            ("add record", "need name"),
            ("add record carl", "added"),
            ("add record jony", "user already in list"),
            ("add phone jony +380(44)978-60-14", "phone already in the list"),
            ("add phone jony +380(45)978-60-14", "added succesfully"),
            ("add phone carl +380(44)978-60-1-3", "not a valid number"),
            ("add phone carl +380(44)978-72-14", "succesfully added"),
            ("change", "need name and number"),
            ("change bruce", "user not found"),
            ("change carl", "need name and number"),
            ("phone", "need name"),
            ("phone bruce", "user not found"),
            ("show all", "carl and jony"),
            ("add record sam +380(44)978-60-24 2000.01.02", "succesfully added"),
            ("add record mistral +380(44)978-60-32 2000.13.33", "date invalid"),
            ("add birthday carl 1999.12.28", "succesfully added"),
            ("days to birthday carl", "this year"),
            ("days to birthday sam", "next year"),
            ("add record bruce", "added"),
            ("show all", "shows with division on pages"),
            ("find not", "not found"),
            ("find a", "found carl, sam"),
            ("find 60-14", "finds johny"),
            ("add note Igor Hello", "add note"),  #Gievskiy 05022023
            ("add tag Igor tag1", "add tag")  #Gievskiy 05022023
            ] 
#Бачу можливість зробити вивід зручнішим для читання. 
#Замість того, щоб всі команди були в одному списку можна розбити його на підсписки,
#кожен з яких буде відповідати за тестування певного модуля.

for c in commands:
    print('command: ' + c[0])
    print('expected result - ', c[1])
    print('real result - ')
    command = atlas.parce(c[0])
    if command:
        print(command[0](command[1:]))
    else:
        print("unknown command")