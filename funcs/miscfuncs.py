
def exec_opt(funcs):
    options = {0: "exit()"}
    print("{} : {}".format(0, "exit()"))
    for i in range(0, len(funcs)):
        options[i + 1] = funcs[i]
        print("{} : {}".format(i + 1, funcs[i]))
    choice = input("Type a number: ")
    try:
        choice = int(choice)
    except ValueError:
        print("Invalid choice")
    else:
        if choice >= len(options):
            print("Out of range")
        else:
            f = options[choice]
            return f

