import ola_display
from ola import FormulaToTree
import statistics
from anytree import Node, RenderTree

class computeMeasures():
    def __init__(self,formula):
        self.formula=formula

    def extractVariables(self):
        set_of_Variables=set([i for i in self.formula if i.isalpha()])
        set_of_Variables.discard('ʌ')
        set_of_Variables.discard('v')
        return sorted(set_of_Variables)

    def measures_in_list(self):
        list_variables_and_dp=self.prepare_variables_dp_list(self.formula)
        list_variables_and_dp_neg=self.prepare_variables_dp_list("~("+self.formula+")")
        results=[]
        half_len_of_list=int(len(list_variables_and_dp)/2)
        for i in range(half_len_of_list):
            value=list_variables_and_dp[i] + list_variables_and_dp_neg[i] + \
                  list_variables_and_dp[i+half_len_of_list] + list_variables_and_dp_neg[i+half_len_of_list]
            half_len_of_value=int(len(value)/2)
            results.append([max(value),statistics.mean(value),statistics.median(value),(max(value[:half_len_of_value])+max(value[half_len_of_value:]))/2])
        return results

    def prepare_variables_dp_list(self,formula):
        tree=FormulaToTreeWithDp(formula)
        leaves_list=[i.name for i in tree.node_list]
        dp_list=tree.compute_dp_points()

        connected_list=[[leaves_list[i],dp_list[i]] for i in range(len(leaves_list)) if len(leaves_list[i])<=2]
        variables=self.extractVariables()

        for var in variables:
            if not var in leaves_list:
                connected_list.append([var,0])
            elif not "~"+var in leaves_list:
                connected_list.append(["~"+var,0])
        return self.sort_measures_list(connected_list)

    def sort_measures_list(self,connected_list):
        variables=self.extractVariables()
        variables_neg=["~"+i for i in variables]
        cutted_list=[]
        for var in variables+variables_neg:
            sublist=[]
            for element in connected_list:
                if element[0]==var:
                    sublist.append(element[1])
            cutted_list.append(sublist)
        return cutted_list

class FormulaToTreeWithDp(FormulaToTree):
    def __init__(self,formula):
        formula=formula.replace(" ","")
        formula=self.clean_mess_in_formula(formula)
        self.node_list= [Node(formula)]
        self.generate_tree(formula, self.node_list[0])

    def compute_dp_points(self):
        dpList=[1]
        for i in range(1,len(self.node_list)):
            negation=self.check_if_negation(self.node_list[i].parent.name)
            index, parent_conjunction=self.find_middle_conjunction(self.node_list[i].parent.name)
            parent_value=dpList[self.node_list.index(self.node_list[i].parent)]

            if parent_conjunction== 'ʌ' and negation:
                dpList.append(parent_value*1)
            elif parent_conjunction== 'v' and negation or parent_conjunction== '→' and negation:
                dpList.append(parent_value*0.5)
            elif parent_conjunction== '→' or parent_conjunction== 'v':
                dpList.append(parent_value*1)
            elif parent_conjunction== 'ʌ':
                dpList.append(parent_value*0.5)
        return dpList
