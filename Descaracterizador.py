from faker import Faker
import os

import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np


fake = Faker('pt_BR')

#Rotina que percorre todos os diretórios existentes na raiz do programa
rootdir = '.'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.lower() == 'titulares.csv':
           # print(subdir)
            
            df = pd.read_csv(subdir + '/' + file, delimiter="\t")
            for index, row in df.iterrows():
                caracteres = '.-/'
                cpf = fake.cpf()
                cnpj = fake.cnpj()

                valor = df.loc[index, 'CPF_CNPJ_TITULAR']
                if valor <= 99999999999:
                    df.loc[index, 'NOME_TITULAR'] = fake.name()
                    for char in caracteres:
                        cpf = cpf.replace(char,'')
                    df.loc[index, 'CPF_CNPJ_TITULAR'] = cpf                        
                else:
                    df.loc[index, 'NOME_TITULAR'] = fake.company() + " " + fake.company_suffix()
                    for char in caracteres:
                        cnpj = cnpj.replace(char,'')
                    df.loc[index, 'CPF_CNPJ_TITULAR'] = cnpj

                df.loc[index, 'ENDERECO_CIDADE'] = fake.city()

            df.to_csv(subdir + '/' +  file, sep='\t', index=None)


#Preciso descaracterizar Nome, CPF e CNPJ

#print(fake.name())


#fake.address()


#fake.text()