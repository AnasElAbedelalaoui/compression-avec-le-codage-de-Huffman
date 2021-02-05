
import chess
import chess.polyglot

from evaluation import evaluation
from save_pgn import SaveGame

class ModeJoueurContreJoueur:
    
    def __init__(self):
        
        #Initialize variables
        self.player1 = input("Nom du joueur 1 : ")
        self.player2 = input("Nom du joueur 2 : ")
        self.winner = None
        self.turnId = 0 #Id of the turn
        
        self.board = chess.Board()
        
        self.gam = SaveGame(self.board)
        self.gam.headers(["test",None,None,None,None,None,None])
        print("Affichage PGN :")
        self.listCoups = [] 
        
        #We print the board
        print(self.board)
        
    def partieEstFinie(self):
        return not self.board.is_game_over()
        
    def getAction(self):
        bestMove = ""
        with chess.polyglot.open_reader("bookfish.bin") as reader:
            for entry in reader.find_all(self.board):
                bestMove = entry.move.__str__()
                break
        
        action = input("Donner une action à réaliser (ex:" + bestMove  + ") : ")
        
        while(self.moveEstLegal(action) == False):
            print("L'action n'est pas autorisée, veuillez recommencer")
            action = input("Donner une action à réaliser (ex:" + bestMove  + ") : ")
            
        return chess.Move.from_uci(action)
    
    def moveEstLegal(self, action):
        
        try:
            tempMove = chess.Move.from_uci(action)
        except:
            return False
        
        if (tempMove in self.board.legal_moves):
            return True
        else: return False
        
    def notificationTourJoueur(self):
        #Un joueur choisi une action (on annonce le tour du joueur, si id%2 == 0 alors blanc sinon noir)
        if(self.turnId%2 == 0):
            print("C'est au tour de", self.player1)
        else:
            print("C'est au tour de", self.player2)
            
        print(evaluation(self.board.fen()))
    
    def finDePartie(self):
        self.gam.save_game(self.listCoups)
        
        if (self.turnId%2 == 0):
            print(self.player1, " a gagné")
        else:
            print(self.player2, " a gagné")
    
    def commencerPartie(self):
        #Tant que un des deux joueurs n'est pas game over
        while(self.partieEstFinie()):
            
            self.notificationTourJoueur()
                
            move = self.getAction()
            
            #Si l'action est possible alors on la réalise
            self.board.push(move)
        
            #On print le plateau et c'est au joueur suivant de jouer si il n'est pas en echec et mat
            print(self.board)
            
            self.listCoups.append(move)
            
            #On incremente l'id
            self.turnId += 1
            
        self.finDePartie()