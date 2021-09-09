from faker import Faker
import os
import re

import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np


fake = Faker('pt_BR')

#Rotina que percorre todos os diretórios existentes na raiz do programa
rootdir = '.'
alterados = {}
caracteres = '.-/'


def obterDadosFake():
    cpfFake = fake.cpf()
    nomeFake = fake.name()
    cnpjFake = fake.cnpj()
    nomeEmpresaFake = fake.company() + " " + fake.company_suffix()

    #cnpj = fake.cnpj()
    for char in caracteres:
        cpfFake = cpfFake.replace(char,'')
        cnpjFake = cnpjFake.replace(char, '')   

    return nomeFake, cpfFake, cnpjFake, nomeEmpresaFake

def getChaveNome(cpf_cnpj):
    if cpf_cnpj not in alterados:
        nomeFake, cpfFake, cnpjFake, nomeEmpresaFake = obterDadosFake()      
        alterados[cpf_cnpj] = { 'cpfFake': cpfFake, 'nomeFake': nomeFake, 
            'cnpjFake': cnpjFake, 'nomeEmpresaFake': nomeEmpresaFake}
        
        if cpf_cnpj <= 99999999999:
            return (cpfFake, nomeFake)               
        else:
            return (cnpjFake, nomeEmpresaFake)  
    else:
        dadosFake = alterados[cpf_cnpj]
        if cpf_cnpj <= 99999999999:
            #É CPF
            return (dadosFake['cpfFake'], dadosFake['nomeFake'])        
        else:
            return (dadosFake['cnpjFake'], dadosFake['nomeEmpresaFake'])


for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        investigados = re.search("investigado", file.lower())
        if investigados:
            #print(file)
            df = pd.read_csv(subdir + '/' + file, delimiter="\t", header=None)
            for index, row in df.iterrows():
                cpf_cnpj = df.iloc[index][1]
                #nomeInvestigado = df.iloc[index][2]

                (df.loc[index, 1], df.loc[index, 2]) = getChaveNome(cpf_cnpj)


            df.to_csv(subdir + '/' +  "investigado_alt.txt", sep='\t', index=None, header=None)

        titulares = re.search("titulares", file.lower())
        if titulares:
            df = pd.read_csv(subdir + '/' + file, delimiter="\t", header=None)
            for index, row in df.iterrows():
                cpf_cnpj = df.iloc[index][7]
                #nomeInvestigado = df.iloc[index][8]
                
                (df.loc[index, 7], df.loc[index, 8]) = getChaveNome(cpf_cnpj)

            df.to_csv(subdir + '/' +  "titulares_alt.txt", sep='\t', index=None, header=None)

        origemDestino = re.search("origem_destino", file.lower())
        if origemDestino:
            DTYPES = {
                 1: 'str',
                 2: 'str',
                 3: 'str',
                 4: 'str',
                 5: 'str',
                 6: 'str',
                 7: 'str',
                 8: 'str'
            }

            df = pd.read_csv(subdir + '/' + file, delimiter="\t", header=None, dtype=DTYPES)

            for index, row in df.iterrows():
                if not np.isnan(df.iloc[index][9]):
                    cpf_cnpj = df.iloc[index][9]
                    #nomeInvestigado = df.iloc[index][10]
                    (df.loc[index, 9], df.loc[index, 10]) = getChaveNome(cpf_cnpj)

                    #df.loc[index, 4] = pd.to_numeric(df.loc[index, 4], errors='coerce').astype('Int64')                    

                    #if not pd.isna(df.loc[index, 4]) : df.loc[index, 4] = int(df.loc[index, 4])
                    #if not pd.isna(df.loc[index, 5]) : df.loc[index, 5] = int(df.loc[index, 5])
                    #if not pd.isna(df.loc[index, 6]) : df.loc[index, 6] = int(df.loc[index, 6])
                    #if not pd.isna(df.loc[index, 7]) : df.loc[index, 7] = int(df.loc[index, 7])
                    #if not pd.isna(df.loc[index, 8]) : df.loc[index, 8] = int(df.loc[index, 8])

                    print(type(df.loc[index, 4]))

            df.to_csv(subdir + '/' +  "origem_destino_alt.txt", sep='\t', index=None, header=None)

        

