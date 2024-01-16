import sys
import re


#boucle pour lire le fichier adn.txt donné dans l'énoncé
if __name__ == '__main__':
    compteur=0
    i=1
    seq=''
    var=''
    id_seq, id_var = None, None
    for line in sys.stdin:
        line=line.rstrip()
        if not line.startswith(';'):
            #if line.startswith('>seq20_var1'):

            if line.startswith('>'):
                if id_seq is None:
                    id_seq = line[1:]
                elif id_var is None:
                    id_var = line[1:]
                else:
                    #print(id_seq,'  ',seq,id_var,'  ',var,i)
                    seq=''
                    var=''
                    id_seq=line[1:]
                    id_var=None
                    i=i+1 
            elif re.match('[ACTG]*$',line):
                if id_var is None:
                    seq=seq+line
                else:
                    var=var+line


def needleman(seq1,seq2):
    col=len(seq1)+1
    lig=len(seq2)+1
    matrix = [[0 for k in range(col)] for k in range(lig)]
    mismatch=-1
    matche=1
    indel=-1
    d={}

    #initialisation des colonnes et des lignes
    for i in range(lig):
        matrix[i][0]=i*indel
    for j in range(col):
        matrix[0][j]=j*indel
    
    #fill the matrix
    for i in range(1,len(matrix)):
        for j in range(1,len(matrix[0])):
            match = matrix[i - 1][j - 1] + (matche if seq1[j - 1] == seq2[i - 1] else mismatch)
            delete = matrix[i - 1][j] + indel
            insert = matrix[i][j - 1] + indel
            matrix[i][j] = max(match, delete, insert)
            
    #traceback to find the alignment
    align1=''
    align2=''
    i=len(seq2)
    j=len(seq1)
    while i>0 and j>0:

        if i > 0 and j > 0 and matrix[i][j] == matrix[i - 1][j - 1] + (matche if seq1[j - 1] == seq2[i - 1] else mismatch):
            align1=seq1[j-1]+align1
            align2=seq2[i-1]+align2
            i=i-1
            j=j-1
        elif j > 0 and matrix[i][j] == matrix[i][j - 1] + indel:

            align1=seq1[j-1]+align1
            align2='-'+align2
            j=j-1

        elif i > 0 and matrix[i][j] == matrix[i - 1][j] + indel:

            align1='-'+align1
            align2=seq2[i-1]+align2
            i=i-1
        else:
            raise ValueError('Algorithm error')
    return [matrix,align1,align2]

def test_alignement(seq1,seq2):
    result=needleman(seq1,seq2)
    matrix,align1,align2=result
    print("Séquence 1:", seq1)
    print("Séquence 2:", seq2)
    print("Alignement 1:", align1)
    print("Alignement 2:", align2)
    print("Score:", matrix[-1][-1])


    
   
"""
    if __name__ == '__main__':  
    #Pour tester le programme 
    print(seq,'\n',var,'\n','--------------')
    print(needleman(seq,var)[1],'\n',needleman(seq,var)[2])

    #test_alignement(seq,var)
    seq1 = "GTCCAAAAATTGGGGGGAGTAGATTGACCGTTCAGGGTCTCATATTTCGTGGTGCCGACA"
    seq2 = "GTCCAAATATTGGGGAGAGTAGATTGATCGTTCAGGGTCTCATATTTCGGTGCCGACA"
    test_alignement(seq1,seq2)

    #seq3 = "TAGCTGCTAGTCACATTATATAACTGTTATCGCAAAAACGTGTACATTTGCACAGAGATA"
    #seq4 = "TCCGCTTCCCATTATATAACTGTTATCGCAAAAACGTGTACACTTGCACAGAGATA"
    #test_alignement(seq3, seq4)

    """
