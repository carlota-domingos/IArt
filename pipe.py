# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 93:
# 107016 Carlota Ribeiro Domingos
# 107043 Matilde Nunes Martins dos Santos

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

E = 0b1000
N = 0b0100
W = 0b0010
S = 0b0001

binary_dict = {
    "FD": 0b1000,
    "FC": 0b0100,
    "FE": 0b0010,
    "FB": 0b0001,
    "BD": 0b1101,
    "BC": 0b1110,
    "BE": 0b0111,
    "BB": 0b1011,
    "VD": 0b1100,
    "VC": 0b0110,
    "VE": 0b0011,
    "VB": 0b1001,
    "LH": 0b1010,
    "LV": 0b0101,
}


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas."""
        return self.id < other.idnao

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, rows: int, cols: int, grid: list[list[str]]):
        self.rows = rows
        self.cols = cols
        self.grid = np.array(grid)

    def get_value(self, row: int, col: int) -> str:
        if row >= 0 and row < self.rows and col >= 0 or col < self.cols:
            return self.grid[row][col]
        else:
            return ""

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[int, int]:
        up = self.grid[row - 1, col] if row > 0 else 0
        low = self.grid[row + 1, col] if row < self.rows - 1 else 0
        return up, low

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[int, int]:
        left = self.grid[row, col - 1] if col > 0 else 0
        right = self.grid[row, col + 1] if col < self.cols - 1 else 0
        return left, right

        # TODO: outros metodos da classe

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
        rows, cols = 0, 0
        while True:
            line = (
                sys.stdin.readline().split()
            )  # Lê uma linha do stdin e divide os elementos
            if not line:  # Verifica se a linha está vazia
                break  # Se estiver vazia, interrompe o loop
            rowsize = len(line)
            if (
                rowsize != cols and cols != 0
            ):  # Verifica se o tamanho da linha é diferente do tamanho das linhas anteriores
                raise ValueError(
                    "Todas as linhas devem ter o mesmo tamanho"
                )  # Se for diferente, lança uma exceção
            elif cols == 0:  # Se for a primeira linha, guarda o tamanho da linha
                cols = rowsize
            if not all(len(r) == 2 for r in line):
                raise ValueError(
                    "Cada elemento do grid deve ter tamanho 2"
                )  # Se o tamanho de algum elemento for diferente de 2, lança uma exceção
            n_line = []
            for piece in line:
                if not (
                    (piece[0] in ["F", "B", "V"] and piece[1] in ["C", "B", "E", "D"])
                    or (piece[0] == "L" and piece[1] in ["V", "H"])
                ):
                    raise ValueError(
                        "peça inválida"
                    )  # Se a peça não for válida, lança uma exceção
                n_line.append(binary_dict[piece])
            rows += 1  # Incrementa o número de linhas
            grid.append(n_line)
        return Board(rows, cols, grid)

    @staticmethod
    def convert_piece(piece: int) -> str:
        for key, value in binary_dict.items():
            if value == piece:
                return key
        return ""


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)

    @staticmethod
    def rotate(piece: int, n: int) -> int:
        """Roda a peça 'piece' n vezes."""
        # rotated piece a number of times counter clockwise
        rotated_piece = piece
        for i in range(n):
            rotated_piece = (rotated_piece << 1) | (rotated_piece >> 3)
            rotated_piece = rotated_piece & 0b1111
        return rotated_piece

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = set()

        for n in range(1, 4):
            ## verifica cantos
            piece = state.board.get_value(0, 0)
            rotated_piece = self.rotate(piece, n)

            if not rotated_piece & N and not rotated_piece & W:
                actions.add((0, 0, rotated_piece))

            piece = state.board.get_value(0, state.board.cols - 1)
            rotated_piece = self.rotate(piece, n)
            if not rotated_piece & N and not rotated_piece & E:
                actions.add((0, state.board.cols - 1, rotated_piece))

            piece = state.board.get_value(state.board.rows - 1, 0)
            rotated_piece = self.rotate(piece, n)
            if not rotated_piece & S and not rotated_piece & W:
                actions.add((state.board.rows - 1, 0, rotated_piece))

            piece = state.board.get_value(state.board.rows - 1, state.board.cols - 1)
            rotated_piece = self.rotate(piece, n)
            if not rotated_piece & S and not rotated_piece & E:
                actions.add((state.board.rows - 1, state.board.cols - 1, rotated_piece))

            # for loop for the first and last row
            for col in range(1, state.board.cols - 1):
                piece = state.board.get_value(0, col)
                rotated_piece = self.rotate(piece, n)
                (
                    actions.add((0, col, rotated_piece))
                    if not rotated_piece & N and rotated_piece != piece
                    else None
                )
                piece = state.board.get_value(state.board.rows - 1, col)
                rotated_piece = self.rotate(piece, n)
                (
                    actions.add((state.board.rows - 1, col, rotated_piece))
                    if not rotated_piece & S and rotated_piece != piece
                    else None
                )

            # for loop for the first and last column
            for row in range(1, state.board.rows - 1):
                piece = state.board.get_value(row, 0)
                rotated_piece = self.rotate(piece, n)
                (
                    actions.add((row, 0, rotated_piece))
                    if not rotated_piece & W and rotated_piece != piece
                    else None
                )
                piece = state.board.get_value(row, state.board.cols - 1)
                rotated_piece = self.rotate(piece, n)
                (
                    actions.add(
                        (
                            row,
                            state.board.cols - 1,
                            rotated_piece,
                        )
                    )
                    if not rotated_piece & E and rotated_piece != piece
                    else None
                )
            # for loop for the rest of the board where it adds the rest of the actions
            for row in range(1, state.board.rows - 1):
                for col in range(1, state.board.cols - 1):
                    piece = state.board.get_value(row, col)
                    rotated_piece = self.rotate(state.board.get_value(row, col), n)
                    (
                        actions.add(
                            (row, col, self.rotate(state.board.get_value(row, col), n))
                        )
                        if rotated_piece != piece
                        else None
                    )
        return list(actions)

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        actions = self.actions(state)
        board = state.board
        new_board = [
            [board.get_value(row, col) for col in range(board.cols)]
            for row in range(board.rows)
        ]
        if action not in actions:
            raise ValueError("Ação inválida")
        new_board[action[0]][action[1]] = action[2]
        new_state = PipeManiaState(Board(board.rows, board.cols, new_board))
        return new_state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        for col in range(state.board.cols):
            # Top border
            if state.board.get_value(0, col) & N:
                return False
            # Bottom border
            if state.board.get_value(state.board.rows - 1, col) & S:
                return False

        # Check left and right borders
        for row in range(state.board.rows):
            # Left border
            if state.board.get_value(row, 0) & W:
                return False
            # Right border
            if state.board.get_value(row, state.board.cols - 1) & E:
                return False
            rows = state.board.rows
            cols = state.board.cols

        for row in range(1, rows, 2):  # verificar comm cuidado mais tarde
            for col in range(
                row % 2, cols - 2 + (cols % 2) - (row % 2), 2
            ):  # verificar isto com cuidado mais tarde
                piece = state.board.get_value(row, col)
                up, down = state.board.adjacent_vertical_values(row, col)
                left, right = state.board.adjacent_horizontal_values(row, col)

                if not ((piece & N and up & S) or (not (piece & N) and not (up & S))):
                    return False
                if not (
                    (piece & W and left & E) or (not (piece & W) and not (left & E))
                ):
                    return False
                if not (
                    (piece & S and down & N) or (not (piece & S) and not (down & N))
                ):
                    return False
                if not (
                    (piece & E and right & W) or (not (piece & E) and not (right & W))
                ):
                    return False
        return True


def goal_test_it_dfs(self, state: PipeManiaState):
    n_visited = 0
    edges = [(0, N, 0), (0, W, 1)]
    stack = [
        (0, 0),
    ]
    visited = set()

    while stack:
        node = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        n_visited += 1

        piece = state.board.get_value(node[0], node[1])

        _, down = state.board.adjacent_vertical_values(node[0], node[1])
        _, right = state.board.adjacent_horizontal_values(node[0], node[1])
        for edge, direction, n in edges:
            if node[n] == edge and piece & direction:
                return False

        next_node = (node[0] + 1, node[1])
        if next_node not in visited and piece & S and down & N:
            if next_node[0] < state.board.rows:
                stack.append(next_node)
            elif piece & S ^ down & N:
                return False

        next_node = (node[0], node[1] + 1)
        if next_node not in visited and piece & E and right & W:
            if next_node[1] < state.board.cols:
                stack.append(next_node)
            elif piece & E ^ right & W:
                return False
            
    return n_visited == state.board.rows * state.board.cols


def h(self, node: Node):
    """Função heuristica utilizada para a procura A*."""
    # TODO
    pass


# TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    pipe = PipeMania(board)
    for line in board.grid:
        for piece in line:
            # print(f"{piece:>04b}", end=" ")
            print(board.convert_piece(piece), end=" ")
    actions = pipe.actions(pipe.initial)
    print(sorted(actions))  # Fix: Replace 'sort' with 'sorted'
    # new_state = pipe.result(pipe.initial, actions[0])
    # for line in new_state.board.grid:
    # for piece in line:
    #     print(board.convert_piece(piece), end=" ")
    print(pipe.goal_test(pipe.initial))
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
