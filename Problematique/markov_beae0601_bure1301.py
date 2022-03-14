#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe markov, Ã  utiliser pour solutionner la problÃ©matique.
    C'est un gabarit pour l'application de traitement des frÃ©quences de mots dans les oeuvres d'auteurs divers.

    Les mÃ©thodes aparaissant dans ce fichier dÃ©finissent une API qui est utilisÃ©e par l'application
    de test testmarkov.py
    Les paramÃ¨tres d'entrÃ©e et de sortie (Application Programming Interface, API) sont dÃ©finis,
    mais le code est Ã  Ã©crire au complet.
    Vous pouvez ajouter toutes les mÃ©thodes et toutes les variables nÃ©cessaires au bon fonctionnement du systÃ¨me

    La classe markov est invoquÃ©e par la classe testmarkov (contenue dans testmarkov.py):

        - Tous les arguments requis sont prÃ©sents et accessibles dans args (dans le fichier testmarkov.py)
        - Note: vous pouvez tester votre code en utilisant les commandes:
            + "python testmarkov.py"
            + "python testmarkov.py -h" (donne la liste des arguments possibles)
            + "python testmarkov.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2022, F. Mailhot et UniversitÃ© de Sherbrooke
"""

import os
import glob
import ntpath
from math import sqrt
from random import random, randint

from pythonds3.graphs import Graph
from collections import OrderedDict

class markov():
    """Classe Ã  utiliser pour coder la solution Ã  la problÃ©matique:

        - Contient certaines fonctions de base pour faciliter le travail (recherche des auteurs).
        - Les interfaces du code Ã  dÃ©velopper sont prÃ©sentes, mais tout le code est Ã  Ã©crire
        - En particulier, il faut complÃ©ter les fonctions suivantes:
            - find_author(oeuvre)
            - gen_text(auteur, taille, textname)
            - get_nth_element(auteur, n)
            - analyze()

    Copyright 2018-2022, F. Mailhot et UniversitÃ© de Sherbrooke
    """

    # Le code qui suit est fourni pour vous faciliter la vie.  Il n'a pas Ã  Ãªtre modifiÃ©
    # Signes de ponctuation Ã  retirer (complÃ©ter la liste qui ne comprend que "!" et "," au dÃ©part)
    PONC = ["!","?",",",".",";",":","_","\"","«","»","(",")","\n","\'","—"]

    def set_ponc(self, value):
        """DÃ©termine si les signes de ponctuation sont conservÃ©s (True) ou Ã©liminÃ©s (False)

        Args:
            value (boolean) : Conserve la ponctuation (Vrai) ou Ã©limine la ponctuation (Faux)

        Returns:
            void : ne fait qu'assigner la valeur du champs keep_ponc
        """
        self.keep_ponc = value

    def print_ponc(self):
        print("Signes de ponctuation Ã  retirer: ", self.PONC)

    def set_auteurs(self):
        """Obtient la liste des auteurs, Ã  partir du rÃ©pertoire qui les contient tous

        Note: le champs self.rep_aut doit Ãªtre prÃ©dÃ©fini:
            - Par dÃ©faut, il contient le rÃ©pertoire d'exÃ©cution du script
            - Peut Ãªtre redÃ©fini par la mÃ©thode set_aut_dir

        Returns:
            void : ne fait qu'obtenir la liste des rÃ©pertoires d'auteurs et modifier la liste self.auteurs
        """
        files = self.rep_aut + "/*"
        full_path_auteurs = glob.glob(files)
        for auteur in full_path_auteurs:
            self.auteurs.append(ntpath.basename(auteur))
        return

    def get_aut_files(self, auteur):
        """Obtient la liste des fichiers (avec le chemin complet) des oeuvres d'un auteur

        Args:
            auteur (string): le nom de l'auteur dont on veut obtenir la liste des oeuvres

        Returns:
            oeuvres (Liste[string]): liste des oeuvres (avec le chemin complet pour y accÃ©der)
        """
        auteur_dir = self.rep_aut + "/" + auteur + "/*"
        oeuvres = glob.glob(auteur_dir)
        return oeuvres

    def set_aut_dir(self, aut_dir):
        """DÃ©finit le nom du rÃ©pertoire qui contient l'ensemble des rÃ©pertoires d'auteurs

        Note: L'appel Ã  cette mÃ©thode extrait la liste des rÃ©pertoires d'auteurs et les ajoute Ã  self.auteurs

        Args (string) : Nom du rÃ©pertoire en question (peut Ãªtre absolu ou bien relatif au rÃ©pertoire d'exÃ©cution)

        Returns:
            void : ne fait que dÃ©finir le nom du rÃ©pertoire qui contient les rÃ©pertoires d'auteurs
        """
        cwd = os.getcwd()
        if os.path.isabs(aut_dir):
            self.rep_aut = aut_dir
        else:
            self.rep_aut = os.path.join(cwd, aut_dir)

        self.rep_aut = os.path.normpath(self.rep_aut)
        self.set_auteurs()
        return


    def set_ngram(self, ngram):
        """Indique que l'analyse et la gÃ©nÃ©ration de texte se fera avec des n-grammes de taille ngram

        Args:
            ngram (int) : Indique la taille des n-grammes (1, 2, 3, ...)

        Returns:
            void : ne fait que mettre Ã  jour le champs ngram
        """
        self.ngram = ngram

    def __init__(self):
        """Initialize l'objet de type markov lorsqu'il est crÃ©Ã©

        Args:
            aucun: Utilise simplement les informations fournies dans l'objet Markov_config

        Returns:
            void : ne fait qu'initialiser l'objet de type markov
        """

        # Initialisation des champs nÃ©cessaires aux fonctions fournies
        self.keep_ponc = True
        self.rep_aut = os.getcwd()
        self.auteurs = []
        self.ngram = 1

        # Au besoin, ajouter votre code d'initialisation de l'objet de type markov lors de sa crÃ©ation
        self.vectors: {str, {tuple, int}} = dict()

        return

    # Ajouter les structures de donnÃ©es et les fonctions nÃ©cessaires Ã  l'analyse des textes,
    #   la production de textes alÃ©atoires, la dÃ©tection d'oeuvres inconnues,
    #   l'identification des n-iÃ¨mes mots les plus frÃ©quents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelÃ©e en premier par testmarkov.py
    # Ensuite, selon ce qui est demandÃ©, les fonctions find_author(), gen_text() ou get_nth_element() sont appelÃ©es

    def find_author(self, oeuvre):
        """AprÃ¨s analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximitÃ© (un nombre entre 0 et 1) de l'oeuvre inconnue avec les Ã©crits de chacun d'entre eux

        Args:
            oeuvre (string): Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns:
            resultats (Liste[(string,float)]) : Liste de tuples (auteurs, niveau de proximitÃ©), oÃ¹ la proximitÃ© est un nombre entre 0 et 1)
        """

        #resultats = [("balzac", 0.1234), ("voltaire", 0.1123)]   # Exemple du format des sorties


        # Ajouter votre code pour dÃ©terminer la proximitÃ© du fichier passÃ© en paramÃ¨tre avec chacun des auteurs
        # Retourner la liste des auteurs, chacun avec sa proximitÃ© au fichier inconnu
        # Plus la proximitÃ© est grande, plus proche l'oeuvre inconnue est des autres Ã©crits d'un auteur
        #   Le produit scalaire entre le vecteur reprÃ©sentant les oeuvres d'un auteur
        #       et celui associÃ© au texte inconnu pourrait s'avÃ©rer intÃ©ressant...
        #   Le produit scalaire devrait Ãªtre normalisÃ© avec la taille du vecteur associÃ© au texte inconnu:
        #   proximitÃ© = (A . B) / (|A| |B|)   oÃ¹ A est le vecteur du texte inconnu et B est celui d'un auteur,
        #           . est le produit scalaire, et |X| est la norme (longueur) du vecteur X

        resultats = list()

        vecteurOeuvre = self.analyzeOeuvre(oeuvre)


        for auteur in self.auteurs:
            resultats.append((auteur, self.proximite(vecteurOeuvre, self.vectors.get(auteur))))


        return resultats

    def proximite(self, texteInconnu: dict, texteConnu: dict):

        totalOccurenceConnu = 0
        totalOccurenceInconnu = 0


        for key, value in texteInconnu.items():
            totalOccurenceInconnu += value**2

        for key, value in texteConnu.items():
            totalOccurenceConnu += value**2




        totalOccurenceConnu = sqrt(totalOccurenceConnu)
        totalOccurenceInconnu = sqrt(totalOccurenceInconnu)
        val = 0
        for key in texteInconnu:
            if key in texteConnu:
                inconnu = texteConnu[key]/totalOccurenceInconnu
                connu = texteInconnu[key]/totalOccurenceConnu
                val += inconnu * connu


        return val


    def create_graph(self, dictionary : dict):
        g = Graph()
        values = list(dictionary.values())
        keys = list(dictionary.keys())
        for i in range(0, len(keys)):
            g.add_edge(keys[i][0], keys[i][1], values[i])
        return g

    def get_next_vertex(self, g : Graph, v: str) -> str:

        total = 0
        vertex = g.get_vertex(v)

        for voisin in vertex.get_neighbors():
            edge = (vertex.key, voisin.key)
            total += g._edges[edge]


        if total == 0:
            return list(g.get_vertices())[randint(0, len(g.get_vertices()))]

        rand = randint(0, total)
        for voisin in vertex.get_neighbors():
            rand -=vertex.get_neighbor(voisin)
            if rand <=0:
                return voisin.get_key()

    def gen_text(self, auteur, taille, textname):
        """AprÃ¨s analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args:
            auteur (string): Nom de l'auteur Ã  utiliser
            taille (int): Taille du texte Ã  gÃ©nÃ©rer
            textname (string): Nom du fichier texte Ã  gÃ©nÃ©rer.

        Returns:
            void : ne retourne rien, le texte produit doit Ãªtre Ã©crit dans le fichier "textname"
        """
        

        text = ""
        if auteur == "A":
            for auteur in self.auteurs:
                text += auteur + ":: Début:\n"
                text += self.generateText(auteur, taille)
                text += "\n" + auteur + "::Fin\n\n"
        else:
            text += self.generateText(auteur, taille)

        f = open(str(textname), "w+", encoding="utf8")
        f.write(text)
        f.close()

    def generateText(self, auteur, taille):
        text = ""
        if self.ngram == 1:
            words = dict()
            sortedList = (sorted(self.vectors.get(auteur), key=self.vectors.get(auteur).get))
            total = sum(self.vectors.get(auteur).values())
            for key, value in self.vectors.get(auteur).items():
               words[key] = value/total

            for i in range(0, taille):
                rand = random()
                for word in sortedList:
                    rand -= words[word]
                    if rand <= 0:
                        text += word[0] + " "
                        break
        else:
            graph = self.create_graph(self.vectors.get(auteur))
            vertex: str = list(graph.get_vertices())[randint(0, len(graph.get_vertices()))]
            text += vertex
            for i in range(0, taille):
                vertex = self.get_next_vertex(graph, vertex)
                text += " " + str(vertex)

        return text
    def get_nth_element(self, auteur, n):
        """AprÃ¨s analyse des textes d'auteurs connus, retourner le n-iÃ¨me plus frÃ©quent n-gramme de l'auteur indiquÃ©

        Args:
            auteur (string): Nom de l'auteur Ã  utiliser
            n (int): Indice du n-gramme Ã  retourner

        Returns:
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherchÃ© (il est possible qu'il y ait plus d'un n-gramme au mÃªme rang)
        """
        listeGram: {int, []} = dict()
        for gram in self.vectors.get(auteur):
            if listeGram.__contains__(self.vectors.get(auteur).get(gram)):
                listeGram.get(self.vectors.get(auteur).get(gram)).append(gram)
            else:
                listeGram[self.vectors.get(auteur).get(gram)] = [gram]


        listeGram = OrderedDict(sorted(((int(key), value) for key, value in listeGram.items()), reverse=True))
        classement = list(listeGram.values())


        #ngram = [['un', 'roman']]   # Exemple du format de sortie d'un bigramme
        return classement[n-1]

    def read_author(self, oeuvre, auteur):
        wordsList : list = []
        line = ""
        file = open(oeuvre, "r", encoding="utf8")
        for x in file.readlines():
            line += x.lower()
        if self.keep_ponc:
            wordline = line.split()
            for words in wordline:
                if len(words) > 2:
                    wordsList.append(words)
        else:
            for characters in self.PONC:
                line = line.replace(characters, " ")
            line = line.replace("-", " ")
            wordline = line.split()
            for words in wordline:
                if len(words) > 2:
                    wordsList.append(words)
        for i in range(0, len(wordsList) - self.ngram):
            words = tuple(wordsList[i:i + self.ngram])
            if words in self.vectors.get(auteur):
                self.vectors[auteur][words] += 1
            else:
                self.vectors[auteur][words] = 1
        file.close()


    def analyzeOeuvre(self, oeuvre) -> dict:
        wordsList: list = []
        vector = dict()
        line = ""
        file = open(oeuvre, "r", encoding="utf8")
        for x in file.readlines():
            line += x.lower()
        if self.keep_ponc:
            wordline = line.split()
            for words in wordline:
                if len(words) > 2:
                    wordsList.append(words)
        else:
            for characters in self.PONC:
                line = line.replace(characters, "")
            line = line.replace("-", "")
            wordline = line.split()
            for words in wordline:
                if len(words) > 2:
                    wordsList.append(words)
        for i in range(0, len(wordsList) - self.ngram):
            words = tuple(wordsList[i:i + self.ngram])
            if words in vector:
                vector[words] += 1
            else:
                vector[words] = 1
        file.close()

        return vector
    def analyze(self):
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args:
            void: toute l'information est contenue dans l'objet markov

        Returns:
            void : ne retourne rien, toute l'information extraite est conservÃ©e dans des strutures internes
        """
        for auteur in self.auteurs:
            self.vectors[auteur] = dict()
            list_oeuvre_auteur = self.get_aut_files(auteur)
            for oeuvre in list_oeuvre_auteur:
                self.read_author(oeuvre, auteur)

        # Ajouter votre code ici pour traiter l'ensemble des oeuvres de l'ensemble des auteurs
        # Pour l'analyse:  faire le calcul des frÃ©quences de n-gralmmes pour 'ensemble des oeuvres
        #   d'un certain auteur, sans distinction des oeuvres individuelles,
        #       et recommencer ce calcul pour chacun des auteurs
        #   En procÃ©dant ainsi, les oeuvres comprenant plus de mots auront un impact plus grand sur
        #   les statistiques globales d'un auteur
        # Il serait possible de considÃ©rer chacune des oeuvres d'un auteur comme ayant un poids identique.
        #   Pour ce faire, il faudrait faire les calculs de frÃ©quence pour chacune des oeuvres
        #       de faÃ§on indÃ©pendante, pour ensuite les normaliser (diviser chaque vecteur par sa norme),
        #       avant des les additionner pour obtenir le vecteur global d'un auteur
        #   De cette faÃ§on, les mots d'un court poÃ¨me auraient une importance beaucoup plus grande que
        #   les mots d'une trÃ¨s longue oeuvre du mÃªme auteur. Ce n'est PAS ce qui vous est demandÃ© ici.

        return


