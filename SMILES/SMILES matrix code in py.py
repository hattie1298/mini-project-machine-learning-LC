import numpy as np
import pandas as pd
##smiles = []
df= pd.read_csv(r'C:\Users\cathe\Documents\SMILES_full.csv')
## check its reading the file right
if 'SMILES' not in df.columns:
    raise ValueError("CSV does not contain a column named 'SMILES'. Please check the file.")
##smiles_list= smiles_list[['SMILES']]
## Convert column to a list of strings and remove anything unwanted
smiles_list = df['SMILES'].dropna().astype(str).str.strip().str.replace(r'\s+', '', regex=True).tolist()
## set vocab up and enumerate (i.e. give each character a numerical value corresponding to position in list)
vocab = ('#', '%', "(", ")",'@','+','-','0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'B', 'C', 'F', 'H', 'I', 'N', 'O', 'P', 'S', "[", "]", 'c', 'i', 'l', 'n',"o", 'r', 's','/', "\\",".")
char_to_ind = {char: ind for ind, char in enumerate(vocab)}
## define the matrix as N x L where N is charcters in vocab and L is the length of smiles string
vocab_size=len(vocab)
## store all matrices in one big list 
one_hot_matrices = [] 
##find the max smiles length for padded matrices
max_smiles_length= max(len(smiles)for smiles in smiles_list)   
for smiles in smiles_list:
        smiles_length= len(smiles)
        one_hot_matrix = np.zeros((smiles_length,vocab_size), dtype=int) ## make a massive matrix of zeros
        print("This is an empty matrix")
        print(one_hot_matrix)
        for i, char in enumerate(smiles):
            if char in char_to_ind:
            ## using char_to_ind as a dictionary
                one_hot_matrix[i, char_to_ind[char]]= 1
            else: 
                ## for every value in smiles, if it is also in vocab change the 0 to a 1. If the value in smiles 
    ## is non existent in vocab, throw an error and say what the character was. 
                raise ValueError("the character",char,"does not exist in the vocabulary")
        ## make padded matrices for consistency
        padded_matrix= np.pad(one_hot_matrix,((0,max_smiles_length - smiles_length),(0, 0)), mode='constant',constant_values=0)
        ##convert matrices to data frame for processing
        df_matrix= pd.DataFrame(padded_matrix)
        ## add label row to identify which SMILES string that matrix corresponds to
        label_row= pd.Dataframe([[smiles]+["-"]*(vocab_size - 1)], columns=df_matrix.columns)
        one_hot_matrices.append(label_row)
        ## add the dataframe matrix
        one_hot_matrices.append(df_matrix)
        ## seperator row full of -1's to idenitfy when a matrix has ended
        one_hot_matrices.append(pd.DataFrame([[-1]*vocab_size]))

##combine all into one hot matrix
final_df = pd.concat(one_hot_matrices, ignore_index=True)
## where its going to be saved
output_path = r"C:\Users\cathe\Documents\All_one_hot_matrices_labelled.csv"
## add the matrcies to the file
final_df.to_csv(output_path, index=False, header= False)

print(f"one hot matrices all saved to{output_path} with SMILES labels and seperators added.")

##for i, matrix in enumerate(one_hot_matrices):
    ##print(f"One-hot matrix for SMILES {i + 1} ({smiles_list[i]}):")
    ##print(matrix)  
##one_hot_matrix= one_hot_encode_smiles(smiles, vocab)
##print(one_hot_matrices)
   
