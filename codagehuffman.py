# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 20:59:23 2021

@author: anas elabed elalaoui
"""
import os
import heapq
import collections
import operator
import sys


class Node:
    def __init__(self, character, freq):
        self.character = character
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return other.freq > self.freq


class CodageHuffman:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # créer des dictionnaires de fréquence avec une valeur triée de faible à élevée
    def creer_dictionnaire_de_frequence(self, text):
        dictionnaire = dict(collections.Counter(text))
        sort = collections.OrderedDict(
            sorted(
                dictionnaire.items(),
                key=operator.itemgetter(1),
                reverse=False))
        return sort

    #creer une pile contenant les noeuds 
    def creer_les_feuilles(self, freq_dict):
        for key in freq_dict:
            noeud = Node(key, freq_dict[key])
            self.heap.append(noeud)

    # construction de l'arbre
    #cette fonction extrait depuis notre pile les deux feuilles ayant la fréquence minimal et créer un nouveau noeud qui est la somme des deux puis elle l'ajoute à la pile
    def fusion_des_noueuds(self):
        while len(self.heap) > 1:
            noeud1 = heapq.heappop(self.heap)
            noeud2 = heapq.heappop(self.heap)
            fusion = Node(None, noeud1.freq + noeud2.freq)
            fusion.left = noeud1
            fusion.right = noeud2
            heapq.heappush(self.heap, fusion)

    #paramatrer l'arc du fils gauche avec la valeur "0" et l'arc droit avec la valeur "1"
    def encode_helper(self, racine, current_code):
        if racine is None:
            return

        if racine.character is not None:
            self.codes[racine.character] = current_code
            return

        self.encode_helper(racine.left, current_code + "0")
        self.encode_helper(racine.right, current_code + "1")
    #phase de codage du texte
    
    def encode(self):
        racine = heapq.heappop(self.heap)
        current_code = ""
        self.encode_helper(racine, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        # obtenir le remplissage supplémentaire du texte encodé
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        # fusionner les "informations" du remplissage supplémentaire dans "chaîne / bit" avec du texte codé 
        padded_info = "{0:08b}".format(extra_padding)
        nouveau_text = padded_info + encoded_text

        return nouveau_text
    #cette fonction retourne le code de chaque charactere dans le texte en bits
    def to_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print('not padded properly')
            exit(0)
        b = bytearray()
        for i in range(
                0, len(padded_encoded_text), 8):  # loop every 8 character
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))  # base 2
        return b

    def compress(self, filename):
        file_text = open(filename, 'r')
        notre_fichier_texte = file_text.read()
        file_text.close()

        freq = self.creer_dictionnaire_de_frequence(notre_fichier_texte)
        self.creer_les_feuilles(freq)
        self.fusion_des_noueuds()
        self.encode()
        encoded_text = self.get_encoded_text(notre_fichier_texte)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array_huff = self.to_byte_array(padded_encoded_text)

        # l'entete
        filename_split = filename.split('.')
        js = open(filename_split[0] + "_compressed.bin", 'wb')
        strcode = str(self.codes)
        js.write(strcode.encode())
        js.close()

        # créer une ligne pour la séparation
        append = open(filename_split[0] + "_compressed.bin", 'a')
        append.write('\n')
        append.close()

        # rajouter le code en bits 
        f = open(filename_split[0] + "_compressed.bin", 'ab')
        f.write(bytes(byte_array_huff))
        f.close()
        
        print('le fichier est compressé!')
        get_original_filesize = os.path.getsize(filename)
        get_compressed_filesize = os.path.getsize(
            filename_split[0] + "_compressed.bin")
        percentage = (get_compressed_filesize / get_original_filesize) * 100
        print(round(percentage, 3), "%")


huffman = CodageHuffman()
if __name__ == '__main__':
   if sys.argv[1] == 'compress':
        huffman.compress(sys.argv[2])
   else:
        print("command not found")
        exit(0)
