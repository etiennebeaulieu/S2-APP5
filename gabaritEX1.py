#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Code pour explorer le premier exercice du laboratoire - APP du cours GIF270

    Le traitement des arguments a Ã©tÃ© inclus:
        Tous les arguments requis sont prÃ©sents et accessibles dans args
        Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments

    Test intÃ©ressant:  avec le fichier fourni pour le laboratoire (mots-francais-sans-accent.txt),
        utiliser "barre" comme mot de dÃ©part, et une distance de 28:
        On observe alors un chemin entre "barre" et "eclat"

    Copyright 2018-2022, FrÃ©dÃ©ric Mailhot et UniversitÃ© de Sherbrooke
"""

import math
import argparse
import glob
import sys
import os
from pythonds3.graphs import Graph


class labo_prob1():
    """Classe Ã  utiliser pour le premier exercice de laboratoire :

        - Contient le code pour crÃ©er le graphe de mots, tel qu'il apparaÃ®t dans le livre de rÃ©fÃ©rence

    Copyright 2018-2022, F. Mailhot et UniversitÃ© de Sherbrooke
    """

    def buildGraph(self,wordFile):
        """CrÃ©ation du graphe de connectivitÃ© entre les mots

        Code tirÃ© de la section 8.8 du livre de rÃ©fÃ©rence
        Voir: <https://runestone.academy/ns/books/published/GIF270/Graphs/BuildingtheWordLadderGraph.html>

        Ã€ adapter pour l'exercice:
       - ajouter un arc entre des mots qui ne sont pas de la mÃªme longueur mais qui ne diffÃ¨rent que par une lettre
       - optionnel: permettre des arcs entre des mots qui diffÃ¨rent par 2, 3, ... lettres (indiquÃ© sur la ligne de commande)

        Produit un graphe oÃ¹ les noeuds reprÃ©sentent des mots et les arcs lient des mots qui ne diffÃ¨rent entre eux
        que tu nombre de caractÃ¨res demandÃ©

        Args:
            wordFile (string) : Nom du fichier de mots Ã  Ã©tudier

        Returns:
            Graph : Retourne le graphe contenant tous les mots, avec des arcs entre les mots qui sont liÃ©s
        """
        d = {}
        g = Graph()
        wfile = open(wordFile, 'r')
        # create buckets of words that differ by one letter
        for line in wfile:
            word = line[:-1]
            for i in range(len(word)):
                bucket = word[:i] + '_' + word[i + 1:]
                if bucket in d:
                    d[bucket].append(word)
                else:
                    d[bucket] = [word]
        # add vertices and edges for words in the same bucket
        for bucket in d.keys():
            for word1 in d[bucket]:
                for word2 in d[bucket]:
                    if word1 != word2:
                        g.add_edge(word1, word2)
        return g

    """
    Vous devez ajouter du code pour accÃ©der au mot de dÃ©part (fourni sur la ligne de commande)
    et ensuite parcourir le graphe jusqu'Ã  une distance D (fournie sur la ligne de commande) du mot d'origine
    """

    def depart(self, mot):
        if g.__contains__(mot):
            vertex = g.get_vertex(mot)
            vertex.set_distance(0)
            return vertex


    def parcourir(self, vertex, distance, voulu):

        if distance == voulu:
            listeMot.append(vertex)
            return

        voisins = vertex.get_neighbors()

        for voisin in voisins:
            if voisin.get_distance() >= distance+1:
                voisin.set_distance(distance+1)
                self.parcourir(voisin, distance+1, voulu)

### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='GIF270 Labo1:Exercice1.py')
    parser.add_argument('-f', required=True, help='Fichier contenant la liste de mots')
    parser.add_argument('-m', required=True, help='Mot de dÃ©part')
    parser.add_argument('-d', required=True, help='Distance du mot de dÃ©part')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    args = parser.parse_args()

    ### Si mode verbose, reflÃ©ter les valeurs des paramÃ¨tres passÃ©s sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Fichier de mots utilisÃ©: " + args.f)
        print("Mot de dÃ©part: " + args.m)
        print("Distance du mot de dÃ©part: " + args.d)

    ### CrÃ©ation de l'objet p1, qui contient la classe avec les fonctions nÃ©cessaires au problÃ¨me 1
    p1 = labo_prob1()

    ### CrÃ©ation du graphe de proximitÃ©, en utilisant le fichier de mots passÃ© en paramÃ¨tre
    g = p1.buildGraph(args.f)
    print("Graph built")

    ### Ã€ partir d'ici, vous devriez inclure les appels requis pour l'utilisation du graphe
    ### Il faut:  trouver le mot de dÃ©part
    ### Marquer la distance entre le mot de dÃ©part et tous les autres mots
    ### Obtenir une sÃ©rie de mots dÃ©butant avec le mot de dÃ©part.  La sÃ©rie doit comprendre le nombre de mots demandÃ©s
    ### Les mots ne doivent pas apparaÃ®tre plus d'une fois dans la liste
    ### Imprimer la liste de mots Ã  l'Ã©cran

    vertex = p1.depart(args.m)

    global listeMot
    listeMot = [vertex]


    p1.parcourir(vertex, 0, int(args.d))
    listeMot = list(dict.fromkeys(listeMot))

    for x in range(0, int(args.d)):
        print(listeMot[x].get_key())