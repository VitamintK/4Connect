import random
import time
import numpy

TILES = '#', 'O'

class Board:
    def __init__(self,x,y,winlength, blank = ' '):
        self.blank = blank
        self.board = [[blank for i in range(y)] for j in range(x)]
        self.winlength = winlength

    def clear(self):
        self.board = [[self.blank for i in j] for j in self.board]
        #change this to change the value of each element in self.board
        #to ' ' instead of creating an entirely new list.

    def visualize(self):
        #for column in [list(i) for i in reversed(zip(*self.board))]:
        #    print '|' + ".".join(column) + '|'

        print('\n'.join(['|' + ".".join(column) + '|' for column in [list(i) for i in reversed(list(zip(*self.board)))]]))
    def vis_with_num(self):
        self.visualize()
        print(' ' + ' '.join([str(x%10) for x in range(len(self.board))]) + ' ')
    def is_game_over_with_piece(self,x,y): #or do I make piece a class?
        #bad implementation probably
        piece_value = self.board[x][y]
        for streak in self.get_surrounding_streaks([piece_value],x,y):
            if streak >= self.winlength:
                return piece_value

        if self.col_is_full(self.board[x]):
            for i in self.board:
                if not self.col_is_full(i):
                    break
            else:
                return self.blank

    def col_is_full(self,col: list):
        if self.blank in col:
            return False
        else:
            return True        #replace usage of this with next_space and delete this method.

    def get_surrounding_streaks(self,values,x,y): #either pass a parameter count_spaces = False OR change the value paramater to values list. 
        if self.board[x][y] in values:
            startat = 1
        else:
            startat = 0
        for hor_dif,ver_dif in [(1,0),(1,1),(0,1),(-1,1)]:
            streak = startat + self.get_streak(values, x, y, hor_dif, ver_dif) + self.get_streak(values, x, y, -1*hor_dif, -1*ver_dif)
            yield streak

    def get_bi_streaks(self, values, x, y, hor_dif, ver_dif):
        if self.board[x][y] in values:
            startat = 1
        else:
            startat = 0
        return startat + self.get_streak(values, x, y, hor_dif, ver_dif) + self.get_streak(values, x, y, -1*hor_dif, -1*ver_dif)

    def get_streak(self,values,x,y,hor_dif,ver_dif,streak=0):
        newx, newy = x+hor_dif, y+ver_dif
        try:
            if newx>=0 and newy>=0 and self.board[newx][newy] in values:
                return self.get_streak(values,newx,newy,hor_dif,ver_dif,streak+1)
            else:
                return streak
        except IndexError:
            return streak

    def next_space(self,col):
        for index, space in enumerate(col):
            if space == self.blank:
                return index
        return False

    def add_piece(self,col_num,piece) -> ('col_num', 'row_num') or False: #move piece to first parameter
        next_space = self.next_space(self.board[col_num])
        if next_space is not False:
            self.board[col_num][next_space] = piece
            return col_num, next_space
        else:
            return False
#todo: make  piece class which is basically a node
# - it should basically have 8 tuples for streaks (or 4).  dunno if each pair will need to be separated (1,1) and (-1,-1) combined?
# - tuple has 2 streaks: the piece value, and the piece value + blank space.
# - and an "update" method which recomputes its own streak in a certain direction and recursively
# - calls the "update" method of the adjacent piece in that direction.

class Piece:
    def __init__(self,value,x,y,board):
        self.value = value
        self.x = x
        self.y = y
        self.streaks = [None, None, None, None]
        
        neighbors = [[None, None, None],[None, None, None],[None, None, None]]
        for hor_dif, ver_dif in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
            neighbor = self.board.board[x+hor_dif][y+ver_dif]
            neighbor.neighbors[-1*hor_dif][-1*ver_dif] = self
            #or
            #neighbor.update_next(hor_dif, ver_dif)
            self.neighbors[hor_dif][ver_dif] = neighbor

        for hor_dif, ver_dif in [(1,0),(1,1),(0,1),(-1,1)]:
            #step one: find the endpoint, save the streak in that direction.
            newx, newy = x+hor_dif, y+ver_dif
            streaka = 0
            while True:
                newx, newy = newx + 1, newy + 1
                streaka += 1
                try:
                    if newx>=0 and newy>=0 and self.board.board[newx][newy] == self.value:
                        pass
                    else:
                        break
                except IndexError:
                    break

            #step two: find the other endpoint by stepping through nodes 1 by 1, and saving the streak in that direction.


            #step 2b: add the two streaks together
            # step three: call each node's 
            
    def update_surrounding(self):
        for hor_dif, ver_dif in [(1,0),(1,1),(0,1),(-1,1)]:
            neighbor = board[x+hor_dif, y+ver_dif]
            neighbor.update_surrounding

    def update_next(self, hor_dif, ver_dif):
        self.neighbors[hor_dif][ver_dif]
        


class Player:
    def __init__(self,value,board,players=None):
        self.value = value
        self.board = board
        self.players = players
    def sort_players(self, players = None):
        """sorts the list so self is the 0th item"""
        if players:
            self.players = players
        self.players.sort(key= lambda x: False if x is self else True)
    def move(self) -> ('col_num', 'row_num'):
        pass


class Human(Player):
    def move(self) -> ('col_num', 'row_num'):
        while True:
            col = input("which column? ")
            if col == 'q':
                return 'quit'
            try:
                col = int(col)
                if col in range(len(self.board.board)):
                    piece = self.board.add_piece(col,self.value)
                    if piece == False:
                        print("that column is full")
                    else:
                        return piece
                else: print("not a valid column")
            except ValueError:
                print("that's not a number.  type 'q' to quit.")
            
            

class AI(Player):
    pass

class ShitAI(AI):
    """ShitAI moves in a random column each turn."""
    def move(self) -> ('col_num', 'row_num'):
        while True:
            col_num = random.randint(0,len(self.board.board)-1)
            if not self.board.col_is_full(self.board.board[col_num]):
            #get col_is_full to accept col num instead?
                #print ' '*(1 + col_num * 2) + 'V'
                return self.board.add_piece(col_num, self.value)

class TrashAI(AI):
    """TrashAI moves in a column that it chooses randomly based on
    a binomial distribution centered at the middle column."""
    def move(self) -> ('col_num', 'row_num'):
        while True:
            col_num = numpy.random.binomial(len(self.board.board)-1,0.5)
            if not self.board.col_is_full(self.board.board[col_num]):
            #get col_is_full to accept col num instead?
                #print ' '*(1 + col_num * 2) + 'V'
                return self.board.add_piece(col_num, self.value)

class DumbAI(AI):
    """DumbAI moves to the space where it either creates the longest line of its own pieces
    or prevents a longer streak of opponent pieces."""
    def move(self) -> ('col_num', 'row_num'):
        streaks = [max(x) for x in zip(*[list(self.max_surrounding_streaks(player.value)) for player in self.players])]
        if max(streaks) > 0:
            return self.board.add_piece(streaks.index(max(streaks)), self.value)
        else:
            return TrashAI.move(self)

    def max_surrounding_streaks(self, value = None):
        """This method iterates through each column. For each column, it finds the next space, and yields
        an int that represents the largest (amount of pieces of one color in a row through that space)."""
        if value is None:
            value = self.value
        for col_num, col in enumerate(self.board.board):
            next_space = self.board.next_space(col)
            if next_space is not False:
                yield max(self.board.get_surrounding_streaks([value],col_num,next_space))
            else:
                yield False

class InfantAI(DumbAI):
    """This AI is as smart as a 3 year old.
    It plays like dumbAI (placing its piece where it creates the longest streak of its own pieces
    OR prevents a longer streak of opponent pieces), BUT without as extreme short-sightedness, because
    3yoAI will not place a piece that will allow its opponent to win the game immediately."""
    def move(self) -> ('col_num', 'row_num'):
        streaks = [max(x) for x in zip(*[list(self.max_surrounding_streaks(player.value)) for player in self.players])]
        sorted_streaks = sorted(enumerate(streaks), key = lambda x: x[1], reverse = True) #(index, streak value) ordered by highest value first.
        if sorted_streaks[0][1] <= 0: #CHANGE THIS TO A SUPER CALL FROM SHITAI
            return TrashAI.move(self)
        for considered_column in sorted_streaks:
            if considered_column[1] is not False:
                if (not self.board.next_space(self.board.board[considered_column[0]]) + 1 < len(self.board.board[considered_column[0]])) or (
                    considered_column[1] >= self.board.winlength - 1) or all([max(self.board.get_surrounding_streaks(
                        [player.value],considered_column[0], self.board.next_space(
                        self.board.board[considered_column[0]]) + 1)) < self.board.winlength - 1 for player in self.players]):
                    return self.board.add_piece(considered_column[0], self.value)
        else:
            return self.board.add_piece(sorted_streaks[0][0], self.value) #this should prefer blocking self over losing immediately
            
class ToddlerAI(InfantAI):
    #sort this way:
    #1. streaks of n length of my own piece. (max)
    #2. streaks of n length of opponent's piece. (max)
    #3. streaks of n-1 length of my own piece that is also a streak of at least win_length for the values [self.value, blank].
    #4. streaks of n-1 length of opponent's piece that is also a streak of at least win_length for the values [self.value, blank].
    #5. streaks of n-2 length that are like #3 et ak
    #6. streaks of n-2 length that are like #4 et al.
    # . streaks of n-1 length of my own piece that aren't a streak of at least win_length for [self.value, blank] (?)
    def move(self) -> ('col_num', 'row_num'):
        
        streaks = list(zip(*[list(self.max_surrounding_streaks(player.value)) for player in self.players]))
        sorted_streaks = sorted(enumerate(streaks), key = lambda x: (False, max(x[1]), x[1][0]), reverse = True)
        #(index, (mystreak, oppstreak)) ordered by highest value first, mystreak higher priority than oppstreak.
        print(sorted_streaks)
        if max(sorted_streaks[0][1]) <= 0: #CHANGE THIS TO A SUPER CALL FROM SHITAI
            return TrashAI.move(self)
        for considered_column in sorted_streaks: #todo: clean this up more.  make it more readable.
            if max(considered_column[1]) is not False:
                if (not self.board.next_space(self.board.board[considered_column[0]]) + 1 < len(self.board.board[considered_column[0]])) or (
                    max(considered_column[1]) >= self.board.winlength - 1) or all([max(self.board.get_surrounding_streaks(
                        [player.value],considered_column[0], self.board.next_space(
                        self.board.board[considered_column[0]]) + 1)) < self.board.winlength - 1 for player in self.players]):
                    return self.board.add_piece(considered_column[0], self.value)
        else:
            return self.board.add_piece(sorted_streaks[0][0], self.value) #this should prefer blocking self over losing immediately

    def max_surrounding_streaks(self, value = None):
        if value is None:
            value = self.value
        for col_num, col in enumerate(self.board.board):
            next_space = self.board.next_space(col)
            if next_space is not False:

                yield max(self.board.get_surrounding_streaks([value],col_num,next_space))
            else:
                yield False

    def potential(self, value, x, y, hor_dif, ver_dif):
        if self.board.get_bi_streaks([value,self.board.blank],x,y,hor_dif,ver_dif) > self.winlength:
            return True
        else:
            return False



#when opponent plays a move, look for streaks surrounding the piece which is
#freshly opened up - aka the space directly above the piece that the opponent
#just played.  Instead of just streaks of one value, modify get_streak() to look for
#streaks of all values besides opponent values - aka, if AI is 'x', look for streaks
#of all blank spaces and 'x's.

class Game:
    def __init__(self,x,y,winlen,blank = ' ', players = [Human, Human], pause = True):
        self.game_board = Board(x,y,winlen, blank= ' ')
        self.players = [playerclass(x, self.game_board) for x, playerclass in zip(TILES, players)] 
        for player in self.players:
            player.sort_players(self.players[:])
        self.turnplnum = 0
        self.turnpl = self.players[self.turnplnum]
        self.pause = pause
        
    def play(self): #make this function better!!!!!
        while True:
            print('')
            self.game_board.vis_with_num()
            if self.pause and not isinstance(self.turnpl, Human):
                time.sleep(0.7)
            turn_res = self.turn()
            if turn_res == 'quit':
                break
            winner = self.game_board.is_game_over_with_piece(*turn_res)
            if winner:
                print('')
                self.game_board.vis_with_num()
                return winner
            else:
                self.increment_pl()

    def increment_pl(self):
        self.turnplnum = (self.turnplnum + 1)%len(self.players)
        self.turnpl = self.players[self.turnplnum]

    def turn(self):
        return self.turnpl.move()

    def sandbox(self):
        oldplayers = self.players
        print(oldplayers)
        self.players = [playerclass(x, self.game_board) for x, playerclass in zip(TILES, [Human, Human])]
        self.increment_pl()
        self.play()
        self.players = oldplayers
        print(self.players)

    def refresh(self):
        self.players = self.players[1:] + [self.players[0]]
        self.turnplnum = 0
        self.turnpl = self.players[self.turnplnum]
        self.game_board.clear()
        
        

g = Game(7,6,4, players = [Human, DumbAI])

def test(amt = 1):
    g = Game(7,6,4, players = [Human, DumbAI])
    counter = {'#':0, 'O':0, ' ':0}
    for i in range(amt):
        g.refresh()
        counter[g.play()]+=1
    return counter

