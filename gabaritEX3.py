#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Code pour explorer le troisiÃ¨me exercice du laboratoire - APP du cours GIF270

    Le traitement des arguments a Ã©tÃ© inclus:
        Tous les arguments requis sont prÃ©sents et accessibles dans args
        Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments

  Copyright 2018-2022, FrÃ©dÃ©ric Mailhot et UniversitÃ© de Sherbrooke
"""

import math
import argparse
import glob
import sys
import os

###  Vous devriez inclure vos classes et mÃ©thodes ici, qui seront appellÃ©es Ã  partir du main
###  Vous pouvez vous inspirer du code donnÃ© dans l'Ã©noncÃ© du problÃ¨me 3
###  Vous devriez imprimer le nombre de paires de mots:
###        dans le fichier de dÃ©part,
###        dans le fichier Ã  vÃ©rifier,
###  Vous devriez aussi imprimer combien de paires de mots sont communes


### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='S2-APP5i Labo1:Exercice1.py')
    parser.add_argument('-f', required=True, help='Fichier contenant la liste de paires de mots de dÃ©part')
    parser.add_argument('-t', required=True, help='Fichier contenant la liste de paires de mots Ã  vÃ©rifier')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    args = parser.parse_args()

    ### Si mode verbose, reflÃ©ter les valeurs des paramÃ¨tres passÃ©s sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Fichier de paires de mots de dÃ©part: " + args.f)
        print("Fichier de paires de mots Ã  vÃ©rifier: " + args.t)

### Ã€ partir d'ici, vous devriez inclure les appels Ã  votre code