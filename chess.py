class MoveError(Exception):
    pass

class BasePiece:
    sym = {}
    def __init__(self,colour):
        if type(colour) != str:
            raise TypeError('colour argument must be str')
        elif colour.lower() not in {'white','black'}:
            raise ValueError('colour must be {white,black}')
        else:
            self.colour = colour

    def __repr__(self):
        return f'BasePiece({repr(self.colour)})'
    
    def __str__(self):
        try:
            return f'{self.colour} {self.name}'
        except NameError:
            return f'{self.colour} piece'

    def symbol(self):
        return f'{self.sym[self.colour]}'
    @staticmethod
    def vector(start, end):
        x = end[0] - start[0]
        y = end[1] - start[1]
        dist = abs(x) + abs(y)
        return x, y, dist


class King(BasePiece):
    name = 'king'
    sym = {'white': '♔', 'black': '♚'}

    def __repr__(self):
        return f"King('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        King can move one step in any direction
        horizontally, vertically, or diagonally.
        '''
        x, y, dist = self.vector(start, end)
        return (dist == 1) or (abs(x) == abs(y) == 1)


class Queen(BasePiece):
    name = 'queen'
    sym = {'white': '♕', 'black': '♛'}

    def __repr__(self):
        return f"Queen('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Queen can move any number of steps horizontally,
        vertically, or diagonally.
        '''
        x, y, _ = self.vector(start, end)
        return (abs(x) == abs(y) != 0) \
               or ((abs(x) == 0 and abs(y) != 0) \
                   or (abs(y) == 0 and abs(x) != 0))


class Bishop(BasePiece):
    name = 'bishop'
    sym = {'white': '♗', 'black': '♝'}

    def __repr__(self):
        return f"Bishop('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''Bishop can move any number of steps diagonally.'''
        x, y, _ = self.vector(start, end)
        return (abs(x) == abs(y) != 0)


class Knight(BasePiece):
    name = 'knight'
    sym = {'white': '♘', 'black': '♞'}

    def __repr__(self):
        return f"Knight('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Knight moves 2 spaces in any direction, and
        1 space perpendicular to that direction, in an L-shape.
        '''
        x, y, dist = self.vector(start, end)
        return (dist == 3) and (abs(x) != 3 and abs(y) != 3)


class Rook(BasePiece):
    name = 'rook'
    sym = {'white': '♖', 'black': '♜'}

    def __repr__(self):
        return f"Rook('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Rook can move any number of steps horizontally
        or vertically.
        '''
        x, y, _ = self.vector(start, end)
        return (abs(x) == 0 and abs(y) != 0) \
               or (abs(y) == 0 and abs(x) != 0)


class Pawn(BasePiece):
    name = 'pawn'
    sym = {'white': '♙', 'black': '♟'}

    def __repr__(self):
        return f"Pawn('{self.name}')"


    def isvalid(self, start: tuple, end: tuple):
        '''
        Pawn can only always move 1 step forward and 2 steps during the first move. Pawn can only capture diagonally forward.
        '''
        if self.colour == "black":
            if start[1] == 6:
                first_move = True
            else:
                first_move = False
        else:
            if start[1] == 1:
                first_move = True
            else:
                first_move = False
        x, y, dist = self.vector(start, end)

        if not first_move:
            if abs(x) < 2:
                if (x == 0) or (abs(x) == 1):
                    if self.colour == 'black':
                        return (y == -1)
                    elif self.colour == 'white':
                        return (y == 1)
                    else:
                        return False
                return False
            return False
        else:
            if x == 0:
                if dist == 1:
                    if (x == 0) or (abs(x) == 1):
                        if self.colour == 'black':
                            return (y == -1)
                        elif self.colour == 'white':
                            return (y == 1)
                        else:
                            return False
                    return False

                elif dist == 2:
                    if self.colour == 'black':
                        return (y == -2)
                    elif self.colour == 'white':
                        return (y == 2)
            return False


class Board:
    '''
    ATTRIBUTES
    turn <{'white', 'black'}>
        The current player's colour.
    
    winner <{'white', 'black', None}>
        The winner (if game has ended).
        If game has not ended, returns None
    checkmate <{'white', 'black', None}>
        Whether any player is checkmated.
    METHODS
    
    start()
        Start a game. White goes first.
    display()
        Print the game board.
    prompt(colour)
        Prompt the player for input.
    next_turn()
        Go on to the next player's turn.
    isvalid(start, end)
        Checks if the move (start -> end) is valid for this turn.
    update(start, end)
        Carries out the move (start -> end) and updates the board.
    '''
    def __init__(self, **kwargs):
        self.debug = kwargs.get('debug', False)
        self._position = {}
        self.winner = None
        self.checkmate = None
    
    def coords(self):
        return list(self._position.keys())

    def pieces(self):
        return list(self._position.values())

    def add(self, coord: tuple, piece):
        self._position[coord] = piece

    def move(self, start, end):
        piece = self.get_piece(start)
        self.remove(start)
        self.add(end, piece)
        self.get_piece(end).notmoved = False

    def remove(self, pos):
        del self._position[pos]

    def castle(self, start, end):
        '''Carry out castling move (assuming move is validated)'''
        self.move(start, end)
        # Move the king
        row = start[1]
        if start[0] == 0:
            self.move((4, row), (2, row))
        elif start[0] == 7:
            self.move((4, row), (6, row))

    def get_piece(self, coord):
        '''
        Retrieves the piece at `coord`.
        `coord` is assumed to be a 2-ple of ints representing
        (col,row).
        Return:
        BasePiece instance
        or None if no piece found
        '''
        return self._position.get(coord, None)

    def alive(self, colour, name):
        for piece in self.pieces():
            if piece.colour == colour and piece.name == name:
                return True
        return False
    
    def pawnscanpromote(self):
        for coord in self.coords():
            row = coord[1]
            piece = self.get_piece(coord)
            for opprow, colour in zip([0, 7], ['black', 'white']):
                if row == opprow and piece.name == 'pawn' and piece.colour == colour:
                    return True
        return False


    def promotepawns(self, PieceClass=None):
        for coord in self.coords():
            row = coord[1]
            piece = self.get_piece(coord)
            for opprow, colour in zip([0, 7], ['black', 'white']):
                if row == opprow and piece.name == 'pawn' and piece.colour == colour:
                    promoted_piece = eval(PieceClass+"(colour)")
                    self.remove(coord)
                    self.add(coord, promoted_piece)

    def king_and_rook_unmoved(self, colour, rook_coord):
        row = rook_coord[1]
        king = self.get_piece((4, row))
        rook = self.get_piece(rook_coord)
        return king.notmoved and rook.notmoved

    def no_pieces_between_king_and_rook(self, colour, rook_coord):
        row = rook_coord[1]
        rook_col = rook_coord[0]
        if rook_col == 0:
            columns = (1, 2, 3)
        elif rook_col == 7:
            columns = (5, 6)
        else:
            raise MoveError('Invalid move: castling from {rook_coord}')
        for col in columns:
            if self.get_piece((col, row)) is not None:
                return False
        return True

    def movetype(self, start, end):
        '''
        Determines the type of board move by:
        1. Checking if the player is moving a piece of their
           own colour
        2. Checking if the piece at `start` and the piece at
           `end` are the same colour
        3. Checking if the move is valid for that piece type
        Returns:
        'move' for normal moves
        'capture' for captures
        'castling' for rook castling
        None for invalid moves
        '''
        if self.debug:
            print(f'== movetype({start}, {end}) ==')
        if start is None or end is None:
            return None
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if self.debug:
            print(f'START_PIECE: {start_piece}')
            print(f'END_PIECE: {end_piece}')
        if start_piece is None \
                or start_piece.colour != self.turn:
            return None
        if end_piece is not None:
            if end_piece.colour != start_piece.colour:
                return 'capture'
            # handle special cases
            elif start_piece.name == 'pawn' \
                    and end_piece.colour != start_piece.colour \
                    and start_piece.isvalid(start, end, capture=True):
                return 'capture'
            else:
                return None
        else:  # end piece is None
            if start_piece.name == 'rook' \
                    and start_piece.isvalid(start, end, castling=True) \
                    and self.king_and_rook_unmoved(self.turn, start) \
                    and self.no_pieces_between_king_and_rook(self.turn, start):
                return 'castling'
            elif start_piece.isvalid(start, end):
                return 'move'
            else:
                return None
        return True

    @classmethod
    def promoteprompt(cls):
        choice = input(f'Promote pawn to '
                    '(r=Rook, k=Knight, b=Bishop, '
                    'q=Queen): ').lower()
        if choice not in 'rkbq':
            return cls.promoteprompt()
        elif choice == 'r':
            return Rook
        elif choice == 'k':
            return Knight
        elif choice == 'b':
            return Bishop
        elif choice == 'q':
            return Queen

    def printmove(self, start, end, **kwargs):
        startstr = f'{start[0]}{start[1]}'
        endstr = f'{end[0]}{end[1]}'
        print(f'{self.get_piece(start)} {startstr} -> {endstr}', end='')
        if kwargs.get('capture', False):
            print(f' captures {self.get_piece(end)}')
        elif kwargs.get('castling', False):
            print(f' (castling)')
        else:
            print('')

    def start(self):
        colour = 'black'
        self.add((0, 7), Rook(colour))
        self.add((1, 7), Knight(colour))
        self.add((2, 7), Bishop(colour))
        self.add((3, 7), Queen(colour))
        self.add((4, 7), King(colour))
        self.add((5, 7), Bishop(colour))
        self.add((6, 7), Knight(colour))
        self.add((7, 7), Rook(colour))
        for x in range(0, 8):
            self.add((x, 6), Pawn(colour))

        colour = 'white'
        self.add((0, 0), Rook(colour))
        self.add((1, 0), Knight(colour))
        self.add((2, 0), Bishop(colour))
        self.add((3, 0), Queen(colour))
        self.add((4, 0), King(colour))
        self.add((5, 0), Bishop(colour))
        self.add((6, 0), Knight(colour))
        self.add((7, 0), Rook(colour))
        for x in range(0, 8):
            self.add((x, 1), Pawn(colour))
        
        self.turn = 'white'

        for piece in self.pieces():
            piece.notmoved = True

    def display(self):
        '''
        Displays the contents of the board.
        Each piece is represented by a coloured symbol.
        '''
        # helper function to generate symbols for piece
        # Row 7 is at the top, so print in reverse order
        rows = [[' ',0,1,2,3,4,5,6,7]]
        for row in range(7,-1,-1):
            row_append = []
            for col in range(-1,8):
                coord = (col, row)
                if col == -1:
                    row_append.append(str(row))
                else:
                    if coord in self.coords():
                        piece = self.get_piece(coord)
                        row_append.append(f'{piece.symbol()}')
                    else:
                        piece = None
                        row_append.append(' ')
            rows.append(row_append)
        return rows


    def parseinput(self, inputstr):
        '''
        Input format should be two ints,
        followed by a space,
        then another 2 ints
        e.g. 07 27
        '''

        def valid_format(inputstr):
            '''
            Ensure input is 5 characters: 2 numerals,
            followed by a space,
            followed by 2 numerals
            '''
            return len(inputstr) == 5 and inputstr[2] == ' ' \
                   and inputstr[0:1].isdigit() \
                   and inputstr[3:4].isdigit()

        def valid_num(inputstr):
            '''Ensure all inputted numerals are 0-7.'''
            for char in (inputstr[0:2] + inputstr[3:5]):
                if char not in '01234567':
                    return False
            return True

        def split_and_convert(inputstr):
            '''Convert 5-char inputstr into start and end tuples.'''
            start, end = inputstr.split(' ')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            return (start, end)

        if not valid_format(inputstr):
            return f'Invalid input. Please enter your move in the following format: __ __, _ represents a digit.'
        elif not valid_num(inputstr):
            return f'Invalid input. Move digits should be 0-7.'
        else:
            start, end = split_and_convert(inputstr)
            if self.valid_move(start, end):
                left, right = inputstr.split(' ')
                left = str(left)
                right = str(right)
                return True
            else:
                return f'Invalid move for {self.get_piece(start)}.'
    
    def valid_move(self, start, end):
        '''
        Returns True if all conditions are met:
        1. There is a start piece of the player's colour
        2. There is no end piece, or end piece is not of player's colour
        3. The move is not valid for the selected piece
        Returns False otherwise
        '''
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if start_piece is None or start_piece.colour != self.turn:
            return False
        elif end_piece is not None and end_piece.colour == self.turn:
            return False
        elif not start_piece.isvalid(start, end):
            return False
        return True

    def update(self, start, end):
        '''
        Update board according to requested move.
        If an opponent piece is at end, capture it.
        '''
        if self.debug:
            print('== UPDATE ==')
        movetype = self.movetype(start, end)
        if movetype is None:
            raise MoveError(f'Invalid move ({self.printmove(start, end)})')
        elif movetype == 'castling':
            self.printmove(start, end, castling=True)
            self.castle(start, end)
        elif movetype == 'capture':
            self.printmove(start, end, capture=True)
            self.remove(end)
            self.move(start, end)
        elif movetype == 'move':
            self.printmove(start, end)
            self.move(start, end)
        else:
            raise MoveError('Unknown error, please report '
                             f'(movetype={repr(movetype)}).')
        if not self.alive('white', 'king'):
            self.winner = 'black'
        elif not self.alive('black', 'king'):
            self.winner = 'white'

    def next_turn(self):
        if self.debug:
            print('== NEXT TURN ==')
        if self.turn == 'white':
            self.turn = 'black'
        elif self.turn == 'black':
            self.turn = 'white'