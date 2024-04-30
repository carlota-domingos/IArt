# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 93:
# 107016 Carlota Ribeiro Domingos
# 107043 Matilde Nunes Martins dos Santos

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.idnao

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, rows: int, cols: int, grid: list[list[str]]):
        self.rows = rows
        self.cols = cols
        self.grid = grid

    def get_value(self, row: int, col: int) -> str:
        if row >= 0 and row < self.rows and col >= 0 or col < self.cols:
            #verificar se é mais prático usar base 0 ou base 1
            #neste momento está em base 0
            return self.grid[row][col]
        else:
            return None

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[str, str]:
        if row == 0:
            return None, self.grid[row + 1][col]
        elif row == self.rows - 1:
            return self.grid[row - 1][col], None
        else:
            return self.grid[row - 1][col], self.grid[row + 1][col]

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        if col == 0:
            return None, self.grid[row][col + 1]
        elif col == self.cols - 1:
            return self.grid[row][col - 1], None
        else:
            return self.grid[row][col - 1], self.grid[row][col + 1]

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        grid = []
        rows, cols= 0, 0
        while True:
            line = sys.stdin.readline().split() # Lê uma linha do stdin e divide os elementos
            if not line:  # Verifica se a linha está vazia
                break  # Se estiver vazia, interrompe o loop
            rowsize = len(line)
            if rowsize != cols and cols != 0:  # Verifica se o tamanho da linha é diferente do tamanho das linhas anteriores
                raise ValueError('Todas as linhas devem ter o mesmo tamanho')  # Se for diferente, lança uma exceção
            elif cols == 0:  # Se for a primeira linha, guarda o tamanho da linha
                cols = rowsize
            if not all(len(r) == 2 for r in line):
                raise ValueError('Cada elemento do grid deve ter tamanho 2')  # Se o tamanho de algum elemento for diferente de 2, lança uma exceção
            for piece in line:
                if not ((piece[0] in ['F','B','V'] and piece[1] in ['C','B','E','D']) \
                        or (piece[0]=='L' and piece[1] in ['V','H'])):
                    raise ValueError('peça inválida')  # Se a peça não for válida, lança uma exceção
            rows += 1  # Incrementa o número de linhas
            grid.append(line)
        return Board(rows, cols, grid)

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)
    
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        dir1 = ['D','E','C','B']
        dir2 = ['V', 'H']
        actions = [(row, col, state.board.get_value(row, col)[0]+d) for row in range(state.board.rows) for col in range(state.board.cols) 
                   for d in ((dir1 if (state.board.get_value(row, col)[0]) != 'L' else dir2)) 
                   if d != state.board.get_value(row, col)[1]]
        return actions

       

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        actions = self.actions(state)
        board = state.board
        new_board = [[board.get_value(row, col) for col in range(board.cols)] for row in range(board.rows)]
        new_board[action[0]][action[1]] = action[2]
        new_state = PipeManiaState(Board(board.rows, board.cols, new_board))
        return new_state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        #pecas esquerdas não podem ter peças esquerdas ao lado
        #pecas direitas não podem ter peças direitas ao lado
        #pecas de cima não podem ter peças de cima na vertical
        #pecas de baixo não podem ter peças de baixo na vertical
        #horizontal nao pode ter peca esquerdas nem cantos para cima à esquerda nem peças direitas e cantos para baixo à direita
        #vertical nao pode ter peças de cima nem cantos para a direita acima nem peças de baixo podem ter vertical e cantos esquerdos abaixo
        #horizontal nao pode ter pecas para baixo por cima nem pecas para cima por baixo

        #horizontal nao pode ter pecas vazias nos lados
        #vertical nao pode ter pecas vazias em cima e em baixo
        #pecas de fecho nao podem ter pecas vazias para onde estao viradas
        #pecas B so podem enconstar a pecas vazias se esdtas estiverem no lado oposto de onde elas tao viradas
         


        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    pipe = PipeMania(board)
    for line in board.grid:
        print(" ".join(line))
    actions = pipe.actions(pipe.initial)
    print(actions)
    new_state = pipe.result(pipe.initial, actions[0])
    print(new_state.board.grid)

    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
