import tmap as tm 
import pandas as pd
from map4 import MAP4Calculator
from rdkit import Chem
import csv 

def bring():
    smiles = []
    file = open("SMILES.txt") 
    for line in file.readlines(): #reads each SMILES string from txt file and adds to the array
        smiles.append(line)
    file.close()
    return smiles

def send(fingerprint_list):
    wtr = csv.writer(open ('fingerprints.csv', 'w'), delimiter=';', lineterminator='\n')
    for x in fingerprint_list : 
        wtr.writerow ([x])
    return "done"


smiles_list = bring() 

dim = 1024

MAP4 = MAP4Calculator(dimensions=dim)
ENC = tm.Minhash(dim)

fingerprint_list = []

for item in smiles_list:
    smiles_a = item
    mol_a = Chem.MolFromSmiles(smiles_a)
    map4_a = MAP4.calculate(mol_a)
    fingerprint_list.append(map4_a)

print(send(fingerprint_list))
