
import chess
import chess.svg

from evaluation import evaluation
from save_pgn import SaveGame
from IPython.display import SVG, display
from MinMax import MinMax

class ModeOrdinateurContreOrdinateur:
    
    def __init__(self):
        self.nameAI1 = "Bot 1"
        self.nameAI2 = "Bot 2"
        self.turnId = 0
        
        self.board = chess.Board()
        
        self.gam = SaveGame(self.board)
        self.gam.headers(["test",None,None,None,None,None,None])
        print("Affichage PGN :")
        self.listCoups = []        
        
    def commencerPartie(self):
        
        lastMove = None
        
        while(self.partieEstFinie()):
            
            self.notificationTourJoueur()
                
            #Si l'action est possible alors on la réalise
            move = self.getAction()
            self.board.push(move)
        
            #On print le plateau et c'est au joueur suivant de jouer si il n'est pas en echec et mat
            if(lastMove == None):
                display(SVG(chess.svg.board(board=self.board, lastmove = move)))
            else:
                display(SVG(chess.svg.board(board=self.board, lastmove = lastMove)))
                
            #On incremente l'id
            self.turnId += 1
            
            self.listCoups.append(move)
            
            lastMove = move
            
        self.finDePartie()
        
    def notificationTourJoueur(self):
        #Un joueur choisi une action (on annonce le tour du joueur, si id%2 == 0 alors blanc donc joueur sinon noir)
        if(self.turnId%2 == 0):
            print("C'est au tour de", self.nameAI1)
        else:
            print("C'est au tour de", self.nameAI2)
            
        print(evaluation(self.board.fen()))
    
    def getAction(self):
        bestMove = ""
        with chess.polyglot.open_reader("bookfish.bin") as reader:
            for entry in reader.find_all(self.board):
                bestMove = entry.move.__str__()
                break
        
        #If the try succeed we can use bookfish, else we use min max with aplha beta
        try:
            move = chess.Move.from_uci(bestMove)
            method = "(Move by Bookfish)"
            
        except:   
            move = MinMax.minimaxRoot(3,self.board,True)
            method = "Move by Min Max and Alpha Beta pruning"
        
        #Player
        if(self.turnId%2 == 0):
            print(self.nameAI1 + " a joue " + str(move), method)
            return move
        else:
            print(self.nameAI2 + " a joue " + str(move), method)
            return move
        
    def partieEstFinie(self):
        return not self.board.is_game_over()
    
    def finDePartie(self):
        self.gam.save_game(self.listCoups)
        
        if (self.turnId%2 == 0):
            print(self.nameAI1, " a gagné")
        else:
            print(self.nameAI2, " a gagné")