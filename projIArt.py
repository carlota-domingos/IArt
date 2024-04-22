from sys import stdin

class PipeManiaState:
    state_id = 0
    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

class Board:
    """ Representação interna de uma grelha de PipeMania. """
    def __init__(self, rows: int, cols: int, grid: list[list[str]]):
        self.rows = rows
        self.cols = cols
        self.grid = grid

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[str, str]:
        if row == 0:
            return (None, self.grid[row + 1][col])
        elif row == self.rows - 1:
            return (self.grid[row - 1][col], None)
        else:
            return (self.grid[row - 1][col], self.grid[row + 1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        
        if col == 0:
            return (None, self.grid[row][col+1])
        elif col == self.cols - 1:
            return (self.grid[row][col-1], None)
        else:
            return (self.grid[row][col-1], self.grid[row][col+1])
       

    @staticmethod
    def parse_instance():
        """Lê a instância do problema do standard input (stdin)
        e retorna uma instância da classe Board.
        Por exemplo:
        $ python3 pipe_mania.py < input_T01
        > from sys import stdin
        > line = stdin.readline().split()
        """
        # TODO
        # matrix = []
        # line = stdin.readline().split()
        # matrix.append(line)

        
        #pass
    def ler_tabuleiro_do_stdin():
        tabuleiro = []
        while True:
            linha = stdin.readline().split() # Lê uma linha do stdin e divide os elementos
            if not linha:  # Verifica se a linha está vazia
                break  # Se estiver vazia, interrompe o loop
            
            tabuleiro.append(linha)  # Adiciona a linha à lista de tabuleiro
        return tabuleiro

    def imprimir_tabuleiro(tabuleiro):
        for linha in tabuleiro:
            print(' '.join(linha))  # Imprime cada linha do tabuleiro separando os elementos por espaço


        

class PipeMania:
    def __init__(self, initial: Board):
        """ O construtor especifica o estado inicial. """
        # TODO
        pass
    def actions(self, state: State):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass
    def result(self, state: State, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # TODO
        pass
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
