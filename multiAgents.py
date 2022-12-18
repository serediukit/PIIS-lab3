import chess

pieces = {
    chess.PAWN: 1,
    chess.BISHOP: 3,
    chess.KNIGHT: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9
}

class Agent:
    def getMove() -> chess.Move:
        raise NotImplementedError()


class NegamaxAgent(Agent):
    def __init__(self, board: chess.Board, depth: int):
        self.board = board
        self.color = board.turn
        self.depth = depth

    def getMove(self):
        bestMove = chess.Move.null
        bestSc = -float('inf')

        for move in self.board.legal_moves:
            self.board.push(move)
            sc = -self.negamax(0)
            self.board.pop()

            if sc > bestSc:
                bestSc = sc
                bestMove = move

        return bestMove

    def negamax(self, depth: int):
        if depth == self.depth:
            return evaluateHeuristic(self.board, self.color)

        bestSc = -float('inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            sc = -self.negamax(depth + 1)
            self.board.pop()

            if sc > bestSc:
                bestSc = sc

        return bestSc


class NegaScoutAgent(Agent):
    def __init__(self, board: chess.Board, depth: int):
        self.board = board
        self.color = board.turn
        self.depth = depth

    def getMove(self):
        bestMove = chess.Move.null
        bestSc = -float('inf')

        for move in self.board.legal_moves:
            self.board.push(move)
            sc = -self.negaScout(0, -float('inf'), float('inf'))
            self.board.pop()

            if sc > bestSc:
                bestSc = sc
                bestMove = move

        return bestMove

    def negaScout(self, depth: int, alpha: float, beta: float):
        if depth == self.depth:
            return evaluateHeuristic(self.board, self.color)

        i = 0
        for move in self.board.legal_moves:
            self.board.push(move)
            sc = -self.negaScout(depth + 1, -beta, -alpha)
            self.board.pop()

            if sc > alpha and sc < beta and depth < self.depth - 1 and i > 0:
                alpha = -self.negaScout(depth + 1, -beta, -sc)

            if sc > alpha:
                alpha = sc

            if alpha >= beta:
                return alpha

            beta = alpha + 1
            i += 1

        return alpha


class PVSAgent(Agent):
    def __init__(self, board: chess.Board, depth: int):
        self.board = board
        self.color = board.turn
        self.depth = depth

    def getMove(self):
        bestMove = chess.Move.null
        bestSc = -float('inf')

        for move in self.board.legal_moves:
            self.board.push(move)
            sc = -self.PVS(0, -float('inf'), float('inf'))
            self.board.pop()

            if sc > bestSc:
                bestSc = sc
                bestMove = move

        return bestMove

    def PVS(self, depth: int, alpha: float, beta: float):
        if depth == self.depth:
            return evaluateHeuristic(self.board, self.color)

        PVSflag = True
        for move in self.board.legal_moves:
            self.board.push(move)

            if PVSflag:
                sc = -self.PVS(depth + 1, -beta, -alpha)
            else:
                sc = -self.PVS(depth + 1, -alpha - 1, -alpha)

                if sc > alpha and sc < beta:
                    sc = -self.PVS(depth + 1, -beta, -alpha)

            self.board.pop()

            if sc >= beta:
                return beta

            if sc > alpha:
                alpha = sc
                PVSflag = False

        return alpha

def evaluateHeuristic(board: chess.Board, color) -> int:

    if board.is_checkmate():
        if board.turn == color:
            return -9999
        else:
            return 9999

    sc = 0
    tempSc = 0

    for i in range(64):
        piece = board.piece_type_at(chess.SQUARES[i])

        if piece in pieces:
            tempSc = pieces[piece]
            sc += tempSc

        if not board.color_at(chess.SQUARES[i]) == color:
            sc -= 2 * tempSc

    return sc
