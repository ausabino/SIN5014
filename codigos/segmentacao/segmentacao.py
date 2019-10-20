################################################################################
#       ARQUIVO: segmentacao.py
#
#     DESCRIÇÃO: Aplicar tecnicas de segmentação e pré-processamento
#
#        OPÇÕES: ---
#    REQUISITOS: openCV
#         NOTAS: Biblioteca 'openCV' pode apresentar problemas com
#                distribuições Linux com interface baseada em Qt
#         AUTOR: Alan U. Sabino <alan.sabino@usp.br>
#        VERSÃO: 1.0
#       CRIAÇÃO: 19/10/2019
#       REVISÃO: ---
################################################################################

import cv2 as biblimagem
import numpy as np

from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

import sys
sys.setrecursionlimit(10000)

def deteccao_linha(matriz_pixels):
    matriz_template = np.array(([-1, -1, 1, 1], [-1, 1, -1, 1], [-1, -1, 1, -1]), dtype='i')
    posicionamento_reta = np.array([0,0,0], dtype='i')
    altura, largura = matriz_pixels.shape[0:2]
    for linha in range(0, altura-1):
        for coluna in range(0, largura-1):
            for posicionamento in range(0, 3):
                resultado = matriz_pixels[linha][coluna][0] * matriz_template[posicionamento][0] + matriz_pixels[linha][coluna+1][0] * matriz_template[posicionamento][1] + matriz_pixels[linha+1][coluna][0] * matriz_template[posicionamento][2] + matriz_pixels[linha+1][coluna+1][0] * matriz_template[posicionamento][3]
                if resultado > 0:
                    posicionamento_reta[posicionamento] += 1
                resultado = 0
    if posicionamento_reta[0] > posicionamento_reta[1] and posicionamento_reta[0] > posicionamento_reta[2]:
        return "horizontal"
    elif posicionamento_reta[1] > posicionamento_reta[0] and posicionamento_reta[1] > posicionamento_reta[2]:
        return "vertical"
    else:
        return "inclinada"

def quantidade_objetos(matriz_pixels):
    altura, largura = matriz_pixels.shape[0:2]
    matriz_flag = np.zeros((altura, largura), dtype='i')
    num_objetos = 0
    for linha in range(0, altura):
        for coluna in range(0, largura):
            if matriz_pixels[linha][coluna][0] != 255 and matriz_flag[linha][coluna] != 1:
                num_objetos += 1
                flag_regiao( linha, coluna, matriz_pixels, matriz_flag)
    return num_objetos

def flag_regiao(linha, coluna, matriz_pixels, matriz_flag):
    altura, largura = matriz_flag.shape[0:2]
    if linha == altura or coluna == largura or coluna < 0 or linha < 0:
        return 0
    elif matriz_pixels[linha][coluna][0] == 255 or matriz_flag[linha][coluna] == 1:
        return 0
    else:
        matriz_flag[linha][coluna] = 1
        flag_regiao( linha, coluna+1, matriz_pixels, matriz_flag)
        flag_regiao( linha+1, coluna+1, matriz_pixels, matriz_flag)
        flag_regiao( linha+1, coluna, matriz_pixels, matriz_flag)
        flag_regiao( linha, coluna-1, matriz_pixels, matriz_flag)
        flag_regiao( linha+1, coluna-1, matriz_pixels, matriz_flag)
        flag_regiao( linha-1, coluna, matriz_pixels, matriz_flag)
        flag_regiao( linha-1, coluna-1, matriz_pixels, matriz_flag)
        flag_regiao( linha-1, coluna+1, matriz_pixels, matriz_flag)

def selecionar_imagem():
    global painelA, caminho
    caminho = filedialog.askopenfilename()
    if len(caminho) > 0:
        imagem_original = biblimagem.imread(caminho)
        imagem = biblimagem.cvtColor(imagem_original, biblimagem.IMREAD_GRAYSCALE)
        imagem = Image.fromarray(imagem)
        imagem = ImageTk.PhotoImage(imagem)
        if painelA is None:
            painelA = Label(image=imagem)
            painelA.image = imagem
            painelA.pack(side="left", padx=10, pady=10)
        else:
            painelA.configure(image=imagem)
            painelA.image = imagem
            if painelB is not None:
                painelB.configure(image='')

def posicionamento():
    if len(caminho) > 0:
        resultado  = deteccao_linha(biblimagem.imread(caminho))
        messagebox.showinfo("Posicionamento da reta na imagem", "A reta esta na posição "+resultado)

def contagem():
    if len(caminho) > 0:
        resultado  = quantidade_objetos(biblimagem.imread(caminho))
        messagebox.showinfo("Quantidade de objetos", "Há "+str(resultado)+" objeto(s) na imagem")

root = Tk()
painelA = None
painelB = None

verificar_posicionamento = Button(root, text="Verificar posicionamento", command=posicionamento)
verificar_posicionamento.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
contar_objetos = Button(root, text="Contar objetos", command=contagem)
contar_objetos.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
abrir_imagem = Button(root, text="Selecionar Imagem", command=selecionar_imagem)
abrir_imagem.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

root.mainloop()

