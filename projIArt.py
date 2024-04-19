
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
    def adjacent_vertical_values(self, row: int, col: int) -> tuple[str, str]:
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        # TODO
        pass
    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        # TODO
        pass
        # TODO: outros metodos da classe

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
        pass

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
