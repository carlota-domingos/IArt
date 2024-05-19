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
    # extra bit for wheter the pice has been visited or not
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

rotated_dict = {
    0b1000: [0b1000, 0b0100, 0b0010, 0b0001],
    0b0100: [0b0100, 0b0010, 0b0001, 0b1000],
    0b0010: [0b0010, 0b0001, 0b1000, 0b0100],
    0b0001: [0b0001, 0b1000, 0b0100, 0b0010],
    0b1101: [0b1101, 0b1011, 0b0111, 0b1110],
    0b1011: [0b1011, 0b0111, 0b1110, 0b1101],
    0b0111: [0b0111, 0b1110, 0b1101, 0b1011],
    0b1110: [0b1110, 0b1101, 0b1011, 0b0111],
    0b1100: [0b1100, 0b1001, 0b0011, 0b0110],
    0b1001: [0b1001, 0b0011, 0b0110, 0b1100],
    0b0011: [0b0011, 0b0110, 0b1100, 0b1001],
    0b0110: [0b0110, 0b1100, 0b1001, 0b0011],
    0b1010: [0b1010, 0b0101],
    0b0101: [0b0101, 0b1010],
}


class PipeManiaState:
    state_id = 0

    def __init__(self, board, coord):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
        self.coordinate = coord

    def __lt__(self, other):
        """Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas."""
        return self.id < other.id


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
        self.initial = PipeManiaState(board, (0, 0))
        self.setpieces = np.zeros((board.rows, board.cols))
        self.limit = board.rows // 2 + board.rows % 2

    @staticmethod
    def rotate(piece: int, n: int) -> int:
        """Roda a peça 'piece' n vezes."""
        # rotated piece a number of times counter clockwise
        rotated_piece = piece
        for i in range(n):
            rotated_piece = (rotated_piece << 1) | (rotated_piece >> 3)
            rotated_piece = rotated_piece & 0b1111
        return rotated_piece

    @staticmethod
    def check_compatibility(piece: int, second_piece: int, direction: int) -> bool:
        """checks if two pieces either have a connection or face opposite directions"""
        if direction == 0:
            return (bool(piece & N) and bool(second_piece & S)) or (
                not bool(piece & N) and not bool(second_piece & S)
            )
        if direction == 1:
            return (bool(piece & E) and bool(second_piece & W)) or (
                not bool(piece & E) and not bool(second_piece & W)
            )
        if direction == 2:
            return (bool(piece & S) and bool(second_piece & N)) or (
                not bool(piece & S) and not bool(second_piece & N)
            )
        if direction == 3:
            return (bool(piece & W) and bool(second_piece & E)) or (
                not bool(piece & W) and not bool(second_piece & E)
            )
        return False

    @staticmethod
    def get_next_coord(state: PipeManiaState, current_piece):
        if (
            current_piece[0] == state.board.rows - 1
            and current_piece[1] == state.board.cols - 1
        ):
            return (0, 0)
        if current_piece[1] == state.board.cols - 1:
            return (current_piece[0] + 1, 0)
        return (current_piece[0], current_piece[1] + 1)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        current_piece = state.coordinate
        flag = False
        initial = state.coordinate
        while True:
            if current_piece == initial and flag:
                # print("lista de acoes", [])
                return []
            flag = True

            piece = state.board.get_value(current_piece[0], current_piece[1])
            actionslst = []
            rotated_pieces = rotated_dict[piece]
            adj_coords = [
                (current_piece[0] - 1, current_piece[1]),
                (current_piece[0], current_piece[1] + 1),
                (current_piece[0] + 1, current_piece[1]),
                (current_piece[0], current_piece[1] - 1),
            ]
            for rotated in rotated_pieces:
                add = True
                for i, adj in enumerate(adj_coords):
                    if (
                        adj[0] >= 0
                        and adj[0] < state.board.rows
                        and adj[1] >= 0
                        and adj[1] < state.board.cols
                    ):
                        second_piece = state.board.get_value(adj[0], adj[1])
                        if self.setpieces[adj[0]][adj[1]] != 0:
                            second_piece = int(self.setpieces[adj[0]][adj[1]])

                    else:
                        second_piece = 0
                    if (
                        second_piece == 0 or (self.setpieces[adj[0]][adj[1]] != 0)
                    ) and not self.check_compatibility(rotated, second_piece, i):
                        #
                        # print ("2nd:", second_piece,"rotated", rotated,"i", i)
                        add = False
                        break
                if add:
                    actionslst.append((current_piece[0], current_piece[1], rotated))

            if len(actionslst) == 1:
                state.coordinate = current_piece
                self.setpieces[current_piece[0], current_piece[1]] = actionslst[0][2]
                return actionslst
            else:
                current_piece = self.get_next_coord(state, current_piece)

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board = state.board
        # print("before")
        # for line in board.grid:
        #     for piece in line:
        #         print(board.convert_piece(piece), end=" ")
        #     print()
        # print(action)

        new_board = [
            [board.get_value(row, col) for col in range(board.cols)]
            for row in range(board.rows)
        ]
        # print("new")
        new_board[action[0]][action[1]] = action[2]

        # for line in new_board:
        #     for piece in line:
        #         print(board.convert_piece(piece), end=" ")
        #     print()
        # print()
        return PipeManiaState(
            Board(board.rows, board.cols, new_board),
            self.get_next_coord(state, state.coordinate),
        )

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        n_visited = 0
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

            up, down = state.board.adjacent_vertical_values(node[0], node[1])
            left, right = state.board.adjacent_horizontal_values(node[0], node[1])

            next_node = (node[0] + 1, node[1])
            if next_node not in visited and piece & S and down & N:
                if next_node[0] < state.board.rows:
                    stack.append(next_node)
            elif ((piece & S) and not (down & N)) or (not (piece & S) and down & N):
                # xor operator uses integers converting to boolean and then back to integer would be more time consuming
                return False

            next_node = (node[0], node[1] + 1)
            if next_node not in visited and piece & E and right & W:
                if next_node[1] < state.board.cols:
                    stack.append(next_node)
            elif ((piece & E) and not (right & W)) or (not (piece & E) and right & W):
                return False

            next_node = (node[0] - 1, node[1])
            if next_node not in visited and piece & N and up & S:
                if next_node[0] >= 0:
                    stack.append(next_node)
            elif ((piece & N) and not (up & S)) or (not (piece & N) and up & S):
                return False

            next_node = (node[0], node[1] - 1)
            if next_node not in visited and piece & W and left & E:
                if next_node[1] >= 0:
                    stack.append(next_node)
            elif ((piece & W) and not (left & E)) or (not (piece & W) and left & E):
                return False
        return n_visited == state.board.rows * state.board.cols

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # Number of remaining actions as heuristic
        return 1


if __name__ == "__main__":
    board = Board.parse_instance()
    pipe = PipeMania(board)

    node = depth_first_tree_search(pipe)

    for line in node.state.board.grid:
        for piece in line:
            print(board.convert_piece(piece), end="\t")
        print()
    pass

    # para ver o tabuleiro
    # for line in board.grid:
    #     for piece in line:
    #         print(f"{piece:>04b}", end=" ")
    #         print(board.convert_piece(piece), end=" ")
