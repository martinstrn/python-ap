import align

def test_needleman():
    assert align.needleman("","")==[[[0]],"",""]
    
    #exemple simple
    assert align.needleman("ATA",'AA')[1:]==['ATA', 'A-A']

    #exemple de la page wikipedia
    assert align.needleman("GCAGCG","GATTACA")[1:]==['GCA--GCG', 'G-ATTACA']
