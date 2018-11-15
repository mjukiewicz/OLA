from anytree import Node, RenderTree

class FormulaToTree():
    def __init__(self,formula):
        formula=formula.replace(" ","")
        formula=self.clean_mess_in_formula(formula)
        self.node_list= [Node(formula)]
        self.generate_tree(formula, self.node_list[0])

    def generate_tree(self,formula, parent):
        #glowna funkcja tworzaca drzewo
        if not (len(formula)==1 or len(formula)==2 and formula[0]=="~"):
            subformula1, subformula2=self.extract_subformulas(formula)
            self.node_list.append(Node(subformula1, parent=parent))
            self.generate_tree(subformula1, self.node_list[-1])
            self.node_list.append(Node(subformula2, parent=parent))
            self.generate_tree(subformula2, self.node_list[-1])

    def check_if_negation(self, formula):
        #sprawdza, czy formula (cala a nie pierwszy czlon) rozpoczyna sie negacja
        middle_conjunction_index, middle_conjunction=self.find_middle_conjunction(formula)
        return formula[0]=="~" and \
        not self.count_nr_of_parentheses(formula[:middle_conjunction_index])==0 and \
        not self.count_nr_of_parentheses(formula[middle_conjunction_index:])==0

    def find_middle_conjunction(self, formula):
        #sprawdza gdzie się znajduje i jaki spojnik laczy obie podformuly
        conjunction=["ʌ","v","→"]
        add_to_index=0
        if self.count_nr_of_conjunctions(formula)==formula.count("(") and formula[0]=="~":
            formula=formula[2:-1]
            add_to_index=2
        for i in range(len(formula)):
            if formula[i] in conjunction and \
            self.count_nr_of_parentheses(formula[:i])==0 and \
            self.count_nr_of_parentheses(formula[i:])==0:
                return i+add_to_index, formula[i]

    def count_nr_of_parentheses(self,formula):
        #wyznacza liczbe poprawnie domknietych nawiasow
        return formula.count("(")-formula.count(")")

    def count_nr_of_conjunctions(self,formula):
        #wyznacza liczbe spojnikow w formule
        return formula.count("ʌ")+formula.count("v")+formula.count("→")

    def clean_mess_in_formula(self, formula):
        #sprzata formule po podziale. W pierwszej kolejnosci usuwa podwojne
        #negacje i wynikajace z tego nawiasy (lacznie dwie pary). Następnie
        #usuwa pozostale nadmiarowe nawiasy wg zasad. jesli formula jest
        #zanegowana nawiasow powinno byc tyle samo co spojnikow. jesli nie,
        #spojnikow powinno byc o jeden wiecej niz nawiasow.
        nr_of_conj=self.count_nr_of_conjunctions(formula)
        if nr_of_conj == 0 and formula[0:3]=="~(~":
            formula=formula[3:-1]
        if nr_of_conj<formula.count("(") and formula[0:3]=="~(~":
            formula=formula[4:-2]
        if formula.count("(") >= nr_of_conj:
            if self.count_nr_of_conjunctions(formula)==0:
                while not formula.count("(")==0:
                    formula=self.remove_excess_parentheses(formula)
            elif formula[0]=="~":
                while not self.count_nr_of_conjunctions(formula)==formula.count("("):
                    formula=self.remove_excess_parentheses(formula)
            elif not formula[0]=="~":
                while self.count_nr_of_conjunctions(formula)-formula.count("(")<1:
                    formula=self.remove_excess_parentheses(formula)
        return formula

    def remove_excess_parentheses(self,formula):
        #usuwa nadmiarowe nawiasy.
        formula_in_list=list(formula)
        formula_in_list[formula.find("(",0,len(formula))]=""
        formula_in_list[formula.rfind(")",0,len(formula))]=""
        formula="".join(formula_in_list)
        return formula

    def extract_subformulas(self, formula):
        #rozdziela formule na dwie podformuly oraz usuwa nadmiarowe nawiasy,
        #ktore powstaly podczas tej operacji
        middle_conjunction_index, middle_conjunction=self.find_middle_conjunction(formula)
        if self.check_if_negation(formula):
            if middle_conjunction=="ʌ" or middle_conjunction=="v":
                subformula1="~("+formula[2:middle_conjunction_index]+")"
                subformula2="~("+formula[middle_conjunction_index+1:-1]+")"
            elif middle_conjunction=="→":
                subformula1=formula[2:middle_conjunction_index]
                subformula2="~("+formula[middle_conjunction_index+1:-1]+")"
        else:
            if middle_conjunction=="ʌ" or middle_conjunction=="v":
                subformula1=formula[:middle_conjunction_index]
                subformula2=formula[middle_conjunction_index+1:]
            elif middle_conjunction=="→":
                subformula1="~("+formula[:middle_conjunction_index]+")"
                subformula2=formula[middle_conjunction_index+1:]

        subformula1=self.clean_mess_in_formula(subformula1)
        subformula2=self.clean_mess_in_formula(subformula2)
        return subformula1, subformula2
