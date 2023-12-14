import sys
import re

compteur=0

def traitement(seqence,variant):
    return

i=1
seq=''
var=''
id_seq, id_var = None, None
for line in sys.stdin:
    line=line.rstrip()
    if not line.startswith(';'):
        if line.startswith('>seq20_var1'):
            print("ok20",id_seq,id_var)
        if line.startswith('>'):
            if id_seq is None:
                id_seq = line[1:]
            elif id_var is None:
                id_var = line[1:]
            else:
                print(id_seq,'  ',seq,id_var,'  ',var,i)
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
    indel=-2
    d={}

    #initialisation des colonnes et des lignes
    for i in range(lig):
        matrix[i][0]=i*mismatch
    for j in range(col):
        matrix[0][j]=j*mismatch
    
    #fill the matrix
    for i in range(1,len(matrix)):
        for j in range(1,len(matrix[0])):
            if matrix[i-1]==matrix[j-1]:
                pass
    

        
