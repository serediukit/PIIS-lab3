import chess
import multiAgents

class Game:
    def __init__(self, type = 'Negamax', depth = 2):
        self.board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        self.depth = depth
        self.agentType = type

    def start(self):
        while not self.board.is_checkmate():
            self.makeMove()
            self.board.turn *= -1
            print(self.board)
            print('\n\n')


    def makeMove(self):
        if self.agentType == 'Negamax':
            agent = NegamaxAgent(self.board, self.depth)
        elif self.agentType == 'NegaScout':
            agent = NegaScoutAgent(self.board, self.depth)
        elif self.agentType == 'PVS':
            agent = PVSAgent(self.board, self.depth)
        else:
            print('Incorrect Agent type, exiting from the game...')
            exit(0)

        move = agent.getMove()
        self.board.push(move)
