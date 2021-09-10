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
dadosPessoas = {}
caracteres = '.-/'

def limpaCpfCnpj(valor):
    if isinstance(valor, np.int64):
        return valor
    elif isinstance(valor, np.float64):
        return valor
    elif isinstance(valor, float):
        return valor
    elif isinstance(valor, int):
        return valor
    else: 
        for char in caracteres:
            valor = valor.replace(char,'')
        return int(valor)    


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

def getDadosPorCPFCNPJ(cpf_cnpj, nomeOriginal):

    cpf_cnpj = limpaCpfCnpj(cpf_cnpj)

    if cpf_cnpj not in alterados:
        nomeFake, cpfFake, cnpjFake, nomeEmpresaFake = obterDadosFake()      
        
        alterados[cpf_cnpj] = { 'cpfFake': cpfFake, 'nomeFake': nomeFake, 
            'cnpjFake': cnpjFake, 'nomeEmpresaFake': nomeEmpresaFake, 'nomeOriginal': nomeOriginal}
        
        dadosPessoas[nomeOriginal] = { 'cpfCnpj': cpf_cnpj}
        
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


def getChavePOrNome(pNome):
    valor = [value for key, value in dadosPessoas.items() if pNome in key]
    
    if valor:
        return valor[0]['cpfCnpj']

  

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #Busca de dados de INVESTIGADOS
        investigados = re.search("investigado", file.lower())
        if investigados:
            #print(file)
            df = pd.read_csv(subdir + '/' + file, delimiter="\t", header=None)
            for index, row in df.iterrows():
                cpf_cnpj = df.iloc[index][1]
                nomeOriginal = df.iloc[index][2]

                (df.loc[index, 1], df.loc[index, 2]) = getDadosPorCPFCNPJ(cpf_cnpj, nomeOriginal)


            df.to_csv(subdir + '/' +  "investigado_alt.txt", sep='\t', index=None, header=None)

        #Busca de dados de TITULARES
        titulares = re.search("titulares", file.lower())
        if titulares:
            df = pd.read_csv(subdir + '/' + file, delimiter="\t", header=None)
            for index, row in df.iterrows():
                cpf_cnpj = df.iloc[index][7]
                nomeOriginal = df.iloc[index][8]
                
                (df.loc[index, 7], df.loc[index, 8]) = getDadosPorCPFCNPJ(cpf_cnpj, nomeOriginal)

            df.to_csv(subdir + '/' +  "titulares_alt.txt", sep='\t', index=None, header=None)

        #Busca de dados de ORIGEM E DESTINO
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
                    nomeOriginal = df.iloc[index][10]
                    
                    (df.loc[index, 9], df.loc[index, 10]) = getDadosPorCPFCNPJ(cpf_cnpj, nomeOriginal)

            df.to_csv(subdir + '/' +  "origem_destino_alt.txt", sep='\t', index=None, header=None)


       #Busca de dados de TITULARES
        dados_ccs = re.search("dados_ccs", file.lower())
        if dados_ccs:
            df = pd.read_csv(subdir + '/' + file, delimiter="\t", usecols= ['Banco','Agencia', 'Conta','Tipo de Conta', 'Nome', 'CPF/CNPJ', 'Tipo de Relacao', 'Data Inicial', 'Data Final','Investigado'])

            for index, row in df.iterrows():
                cpf_cnpj = df.iloc[index][5]
                nomeOriginal = df.iloc[index][4]
                
                (df.loc[index][5], df.loc[index][4]) = getDadosPorCPFCNPJ(cpf_cnpj, nomeOriginal)

            df.to_csv(subdir + '/' +  "dados_ccs_alt.txt", sep='\t', index=None)

 

