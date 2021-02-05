
def evaluation (fen) : 
    liste_a_suppr=["1","2","3","4","5","6","7","8","/"]
    for i in range(len(liste_a_suppr)) :
        fen=fen.replace(liste_a_suppr[i],"")
    fen=fen.split(" ")[0]
    l_pion = ["p","n","b","r","q","k","P","N","B","R","Q","K"]
    valeur =[-1,-3,-3,-4,-7,-100,1,3,3,4,7,100]
    cpt=0
    for j in fen :
        cpt=valeur[l_pion.index(j)]+cpt
    if cpt<0 : 
        res="The black might win"
    elif cpt>0: 
        res="The white might win"
    else : 
        res=" Black or White , that is the question..."
    return(res)