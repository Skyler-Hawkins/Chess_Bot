from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
from pieces.king import king
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    # HELPER FUNCTIONS FOR CALCULATEB
    # idea: add defenses in here too (like what pieces its defending)
    def get_piece_attacks(self, piece, gametiles):
        attack_value = 0
        piece_values = {
            'p': 30,  # Pawn
            'n': 100,  # Knight
            'b': 120,  # Bishop
            'r': 190,  # Rook
            'q': 300, # Queen
            'k': 500 # King
        }

        legal_moves = piece.legalmoveb(gametiles)
        if legal_moves is not None:
            for move in legal_moves:
                x, y = move
                target_piece = gametiles[x][y].pieceonTile
                if target_piece.alliance != piece.alliance and target_piece.alliance is not None:
                    attack_value += piece_values.get(target_piece.tostring().lower(), 0)
            return attack_value
        else:
            return 0
    # THE function to modify

    '''
    To be done: 
        Need to fix endgame: particularly I want to encourage checks, and somehow make it use several pieces instead of a wild goose
        chase with the queen
        Want to encourage promoting pawns at the end.
        Midgame seems fine.
    '''
    # checking if white king is checked: 
    def check_white_king(self,gametiles):
        x=0
        y=0
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.tostring()=='k'):
                    x=m
                    y=k
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.alliance=='Black'):
                    moves=gametiles[m][k].pieceonTile.legalmoveb(gametiles)
                    if moves!=None:
                        return "checked"
        return "notchecked"

    def calculateb(self,gametiles):
        value=0
        #           IMPLEMENTED:
        #          - Piece-Square Table: this table gives an inherent value modifier to each chess piece based on its position on the board.
        #                                this is valuable since some pieces (like the knight) are more valuable in the center of the board as opposed to the edges
        piece_square_tables = {
            'PawnMidgame': [
                [50, 50, 50, 50, 50, 50, 50, 50],        
                [50, 50, 50, 50, 50, 50, 50, 50], 
                [10, 10, 20, 30, 30, 20, 10, 10], 
                [5, 5, 10, 25, 25, 10, 5, 5],     
                [0, 0, 0, 20, 20, 0, 0, 0],       
                [5, -5, -10, 0, 0, -10, -5, 5],   
                [5, 10, 10, -20, -20, 10, 10, 5], 
                [0, 5, 5, -20, -20, 5, 5, 0]          
            ],
            'PawnEndgame': [
                [200, 200, 200, 200, 200, 200, 200, 200],         
                [100, 100, 100, 100, 100, 100, 100, 100],
                [10, 10, 20, 30, 30, 20, 10, 10], 
                [5, 5, 10, 25, 25, 10, 5, 5],     
                [0, 0, 0, 20, 20, 0, 0, 0],      
                [5, -5, -10, 0, 0, -10, -5, 5],   
                [5, 10, 10, -20, -20, 10, 10, 5], 
                [0, 0, 0, 0, 0, 0, 0, 0]           
            ],
            'Knight': [
                [-50, -40, -30, -30, -30, -30, -40, -50],  
                [-40, -20,  0,  0,  0,  0, -20, -40],     
                [-30,  0, 10, 15, 15, 10,  0, -30],        
                [-30,  5, 15, 20, 20, 15,  5, -30],       
                [-30,  0, 15, 20, 20, 15,  0, -30],       
                [-30,  5, 10, 15, 15, 10,  5, -30],       
                [-40, -20,  0,  5,  5,  0, -20, -40],     
                [-50, -40, -30, -30, -30, -30, -40, -50]  
            ],
            'Bishop': [
                [-20, -10, -10, -10, -10, -10, -10, -20],  # 8th rank
                [-10,  0,  0,  0,  0,  0,  0, -10],       # 7th rank
                [-10,  0,  5, 10, 10,  5,  0, -10],       # 6th rank
                [-10,  5,  5, 10, 10,  5,  5, -10],       # 5th rank
                [-10,  0, 10, 10, 10, 10,  0, -10],       # 4th rank
                [-10, 10, 10, 10, 10, 10, 10, -10],       # 3rd rank
                [-10,  5,  0,  0,  0,  0,  5, -10],       # 2nd rank
                [-20, -10, -10, -10, -10, -10, -10, -20]  # 1st rank   
            ],
            'Rook': [
                [0, 0, 0, 0, 0, 0, 0, 0],   # 8th rank
                [5, 10, 10, 10, 10, 10, 10, 5],  # 7th rank
                [-5, 0, 0, 0, 0, 0, 0, -5],  # 6th rank
                [-5, 0, 0, 0, 0, 0, 0, -5],  # 5th rank
                [-5, 0, 0, 0, 0, 0, 0, -5],  # 4th rank
                [-5, 0, 0, 0, 0, 0, 0, -5],  # 3rd rank
                [-5, 0, 0, 0, 0, 0, 0, -5],  # 2nd rank
                [0, 0, 0, 5, 5, 0, 0, 0]    # 1st rank
            ],
            'Queen': [
                    [-20, -10, -10, -5, -5, -10, -10, -20],  # 8th rank
                    [-10,  0,  0,  0,  0,  0,  0, -10],     # 7th rank
                    [-10,  0,  5,  5,  5,  5,  0, -10],     # 6th rank
                    [-5,  0,  5,  5,  5,  5,  0, -5],       # 5th rank
                    [0,  0,  5,  5,  5,  5,  0, -5],        # 4th rank
                    [-10,  5,  5,  5,  5,  5,  0, -10],     # 3rd rank
                    [-10,  0,  5,  0,  0,  0,  0, -10],     # 2nd rank
                    [-20, -10, -10, -5, -5, -10, -10, -20]  # 1st rank
            ],
            'KingMidgame': [
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 8th rank
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 7th rank
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 6th rank
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 5th rank
                [-20, -30, -30, -40, -40, -30, -30, -20],  # 4th rank
                [-10, -20, -20, -20, -20, -20, -20, -10],  # 3rd rank
                [20,  20,   0,   0,   0,   0,  20,  20],  # 2nd rank
                [20,  30,  10,   0,   0,  10,  30,  20]   # 1st rank
            ],
            'KingEndgame': [
                [-50, -40, -30, -20, -20, -30, -40, -50],  # 8th rank
                [-30, -20, -10,  0,  0, -10, -20, -30],   # 7th rank
                [-30, -10,  20, 30, 30, 20, -10, -30],    # 6th rank
                [-30, -10,  30, 40, 40, 30, -10, -30],    # 5th rank
                [-30, -10,  30, 40, 40, 30, -10, -30],    # 4th rank
                [-30, -10,  20, 30, 30, 20, -10, -30],    # 3rd rank
                [-30, -30,  0,  0,  0,  0, -30, -30],     # 2nd rank
                [-50, -30, -30, -30, -30, -30, -30, -50]  # 1st rank
            ]
        } 
        # tracks the value of the board not including the kings to determine endgame (if a king is gone, game over, so no need to check)
        total_piece_value = 0
        K_pos = [0,0]
        k_pos = [0,0]
        only_has_king = True


        for x in range(8):
            for y in range(8):
                    current_piece_eval = gametiles[y][x].pieceonTile
                    currentPiece = current_piece_eval.tostring()

                    if currentPiece=='P':
                
                        value -= (100 - piece_square_tables['PawnMidgame'][y][x])
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        # value -= attack_value
                        total_piece_value += 100

                    if currentPiece=='N':
                        value -=  300 - piece_square_tables['Knight'][y][x]
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        value -= attack_value
                        total_piece_value += 300

                    if currentPiece=='B':
                        value -= 350 - piece_square_tables['Bishop'][y][x]
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        value -= attack_value
                        total_piece_value += 350
                    if currentPiece=='R':
                        value -= 525 - piece_square_tables['Rook'][y][x]
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        value -= attack_value                 
                        total_piece_value += 525
                        
                    if currentPiece=='Q':
                        value -= 1000 - piece_square_tables['Queen'][y][x]
                        total_piece_value += 1000
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        value -= attack_value
                    # DONE: MOVE THE KING EVALUATION OUTSIDE OF THIS LOOP (track indices of the kings, then evaluate them after the loop based on if its endgame or midgame) 
                    if currentPiece=='K':
                        K_pos = [y,x]
                        # value -= 10000 - piece_square_tables['King'][y][x]

                    if currentPiece=='p':
                        value += 100 + piece_square_tables['PawnMidgame'][7 - y][x]
                        total_piece_value += 100
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        # value += attack_value
                        only_has_king = False
                    if currentPiece=='n':
                        value=value+300 + piece_square_tables['Knight'][7 - y][x]
                        total_piece_value += 300
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        value += attack_value
                        only_has_king = False
                    if currentPiece=='b':
                        value += 350 + piece_square_tables['Bishop'][7 - y][x]
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        value += attack_value
                        total_piece_value += 350
                        only_has_king = False
                    if currentPiece=='r':
                        value += 525 + piece_square_tables['Rook'][7 - y][x]
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        value += attack_value
                        total_piece_value += 525
                        only_has_king = False
                    if currentPiece=='q':
                        value += 1000 + piece_square_tables['Queen'][7 - y][x]
                        attack_value = self.get_piece_attacks(current_piece_eval, gametiles)
                        value += attack_value
                        total_piece_value += 1000
                        only_has_king = False
                    if currentPiece=='k':
                        k_pos = [y,x]
                        # value += 10000 + piece_square_tables['King'][7 - y][x]
        endgame = False
        if total_piece_value < 1500:
            endgame = True
        x, y = K_pos
        x_k, y_k = k_pos
        # TO-DO: Add difference in endgame behavior based on the total piece value, for now am using naive approach of checking for only the enemy king remaining
        if endgame:
            
            value -= 10000 - piece_square_tables['KingEndgame'][y][x]
            value += 10000 + piece_square_tables['KingEndgame'][7 - y_k][x_k]
        else: 
            value -= 10000 - piece_square_tables['KingMidgame'][y][x]
            value += 10000 + piece_square_tables['KingMidgame'][7 - y_k][x_k]
        # dominating: when the opponent only has their king left.
        # need to highly highly prioritize taking the king
        if only_has_king:
        # Here, we can go all-out, highly prioritize checking the king with as many pieces as possible
            king_position = (y_k * 8) + x_k
            white_king = king("White", king_position)
            white_king_moves = white_king.legalmoveb(gametiles)
            # want to really prioritize promoting pawns, and checking the king
            # try to check the king with as many pieces as possible
            try:
                is_checked = self.check_white_king(gametiles)
                if is_checked[0] == "checked":
                    value -= 5000
            except Exception as e:
                print("Error: ", e)

            if len(white_king_moves) == 0:
                print("CHECKMATE HAS BEEN SEEN")
                value = -100000000000
        return value
    


    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()


        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
