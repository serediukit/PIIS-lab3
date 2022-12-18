import game

if __name__ == '__main__':
    i = int(input("""
    Choose the agent type you want to use:
    1 - NegamaxAgent
    2 - NegaScoutAgent
    3 - PVSAgent
    """))
    type = ['Negamax', 'NegaScout', 'PVS']

    depth = int(input("Enter depth of search: "))

    game = Game(type[i-1], depth)
    game.start()
