from anytree import Node, RenderTree
from os import system
import ola, ola_dp

def generate_png(formula):
    tree1=ola_dp.FormulaToTreeWithDp(formula)
    tree_png=displayTree(tree1.node_list)
    tree_png.tree_to_pic('tree1.png', tree1.compute_dp_points())
    tree2=ola_dp.FormulaToTreeWithDp("~("+formula+")")
    tree_png=displayTree(tree2.node_list)
    tree_png.tree_to_pic('tree2.png', tree2.compute_dp_points())

class displayTree():

    def __init__(self,node_list):
        self.node_list=node_list

    def tree_to_pic(self,pictureName, dp_values_list):
        text='digraph tree {'
        for i in range(len(self.node_list)):
            text+='    \"'+str(self.node_list[i])+'\" [label=\"'+  self.node_list[i].name+"\ndp="+str(dp_values_list[i])+"\"];"
        for i in range(1,len(self.node_list)):
            text+='    \"'+ str(self.node_list[i].parent)+'\" ->\"'+ str(self.node_list[i]) + "\";"
        text+="}"
        self.write_DOT_File(pictureName, text.replace("ʌ",'\u028C'))
        self.convert_DOT_to_PNG(pictureName)

    def write_DOT_File(self,filename, textToSave):
        textFile=open('graph.txt','wb')
        textFile.write(textToSave.encode('utf8'))
        textFile.close()

    def convert_DOT_to_PNG(self,pictureName):
        system("dot graph.txt -T png -o "+pictureName)
