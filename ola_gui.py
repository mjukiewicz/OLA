from tkinter import *
import ola, ola_dp, ola_display
from anytree import Node, RenderTree
from PIL import Image , ImageTk
from decimal import Decimal, ROUND_HALF_UP

class OlaGUI (Frame , object ):
    def __init__(self, master):
        super(OlaGUI , self).__init__(master)
        self.master.title("Ola GUI")
        mainWindow.geometry("1350x650")
        #mainWindow.state('zoomed')
        mainWindow.resizable(0,0)
        self.pack(fill =BOTH , expand =1)
        self.create_widgets()

    def create_widgets(self):
        button_width=17
        small_button_width=5
        shift=200
        x_positions=[700,840,850,910,625]
        y_positions=[70, 100,130,170,220,270, 325]
        check_button = Button(self, text = "Check formula",
                                     width=button_width, command=self.check_formula)
        check_button.place(x=x_positions[2]+shift, y=y_positions[3])
        self.generate_tree_button = Button(self, text = "Generate tree",
                                     width=button_width, state=DISABLED,
                                     command=self.generate_tree)
        self.generate_tree_button.place(x=x_positions[0]+shift, y=y_positions[3])
        self.generate_tree_button_with_dp = Button(self, text = "Generate tree with dp",
                                       width=button_width, state=DISABLED,
                                       command=self.generate_tree_with_dp)
        self.generate_tree_button_with_dp.place(x=x_positions[0]+shift, y=y_positions[4])
        self.compute_dp_button = Button(self, text = "Compute dp",
                                          width=button_width, state=DISABLED,
                                          command=self.comupte_dp)
        self.compute_dp_button.place(x=x_positions[2]+shift, y=y_positions[4])
        self.generate_png_button = Button(self, text = "Generate tree in PNG",
                                        width=button_width, state=DISABLED,
                                        command=self.generate_png)
        self.generate_png_button.place(x=x_positions[0]+shift, y=y_positions[5])
        self.image_preview_button = Button(self, text = "PNG preview",
                                         width=button_width, state=DISABLED,
                                         command=self.image_preview)
        self.image_preview_button.place(x=x_positions[2]+shift, y=y_positions[5])
        implication_button = Button(self, text = "→", width=small_button_width,
                                    command=self.insert_implication)
        implication_button.place(x=x_positions[0]+shift, y=y_positions[2])
        or_button = Button(self, text = "v", width=small_button_width,
                                     command=self.insert_OR)
        or_button.place(x=770+shift, y=y_positions[2])
        and_button = Button(self, text = "ʌ", width=small_button_width,
                                    command=self.insert_AND)
        and_button.place(x=x_positions[1]+shift, y=y_positions[2])
        negation_button = Button(self, text = "~", width=small_button_width,
                                 command=self.insert_NOT)
        negation_button.place(x=x_positions[3]+shift, y=y_positions[2])
        formula_label=Label(self,text="Formula:")
        formula_label.place(x=x_positions[0]+shift, y=y_positions[0])
        self.oldText=StringVar()
        self.oldText.trace("w", self.text_changed)
        self.oldText.set("(pvq)→r")
        self.formula_entry = Entry (self, width=50,textvariable=self.oldText)
        self.formula_entry.place(x=x_positions[0]+shift, y=y_positions[1])
        self.formula=Text(self, height=37, width=105)
        self.formula.place(x=0, y=0)
        #self.formula_entry.insert(END, "pvq→r")
        self.computed_dp=Text(self, height=10, width=35)
        self.computed_dp.place(x=x_positions[0]+shift, y=y_positions[6])
        scrollbar = Scrollbar(self.formula)
        scrollbar.place(x=x_positions[-1]+shift, height=595)
        scrollbar.config(command=self.formula.yview)
        self.formula.config(yscrollcommand=scrollbar.set)

    def text_changed(self,*args):
        self.generate_tree_button.config(state="disabled")
        self.generate_tree_button_with_dp.config(state="disabled")
        self.compute_dp_button.config(state="disabled")
        self.generate_png_button.config(state="disabled")
        self.image_preview_button.config(state="disabled")

    def check_formula(self):
        if True:
            self.generate_tree_button.config(state="normal")
            self.generate_tree_button_with_dp.config(state="normal")
            self.compute_dp_button.config(state="normal")
            self.generate_png_button.config(state="normal")
            self.image_preview_button.config(state="normal")

    def insert_implication(self):
        self.formula_entry.insert(self.formula_entry.index(INSERT),"→")

    def insert_OR(self):
        self.formula_entry.insert(self.formula_entry.index(INSERT),"v")

    def insert_AND(self):
        self.formula_entry.insert(self.formula_entry.index(INSERT),"ʌ")

    def insert_NOT(self):
        self.formula_entry.insert(self.formula_entry.index(INSERT),"~")

    def generate_tree(self):
        self.formula.delete('1.0', END)
        tree1=ola.FormulaToTree(self.formula_entry.get())
        for pre, _, node in RenderTree(tree1.node_list[0]):
            self.formula.insert(END, "%s%s\n" % (pre, node.name))
        self.formula.insert(END, "\n\n")
        tree2=ola.FormulaToTree("~("+self.formula_entry.get()+")")
        for pre, _, node in RenderTree(tree2.node_list[0]):
            self.formula.insert(END, "%s%s\n" % (pre, node.name))

    def generate_tree_with_dp(self):
        self.formula.delete('1.0', END)
        tree1=ola_dp.FormulaToTreeWithDp(self.formula_entry.get())
        dp_values_list=iter(tree1.compute_dp_points())
        for pre, _, node in RenderTree(tree1.node_list[0]):
            self.formula.insert(END, "%s%s dp=%g\n" % (pre, node.name, next(dp_values_list)))
        self.formula.insert(END, "\n\n")
        tree2=ola_dp.FormulaToTreeWithDp("~("+self.formula_entry.get()+")")
        dp_values_list=iter(tree2.compute_dp_points())
        for pre, _, node in RenderTree(tree2.node_list[0]):
            self.formula.insert(END, "%s%s dp=%g\n" % (pre, node.name, next(dp_values_list)))

    def generate_png(self):
        ola_display.generate_png(self.formula_entry.get())

    def image_preview(self):
        obrazekOkno1=Toplevel()
        obrazekOkno1.title("Base formula")
        obrazTk = ImageTk.PhotoImage(file='tree1.png')
        label = Label(obrazekOkno1, image=obrazTk)
        label.image = obrazTk
        label.pack()
        obrazekOkno2=Toplevel()
        obrazekOkno2.title("Formula with negation")
        obrazTk = ImageTk.PhotoImage(file='tree2.png')
        label = Label(obrazekOkno2, image=obrazTk)
        label.image = obrazTk
        label.pack()

    def comupte_dp(self):
        self.computed_dp.delete('1.0', END)
        measures=ola_dp.computeMeasures(self.formula_entry.get())
        for var_values in measures.measures_in_list():
            for j in var_values:
                self.computed_dp.insert(END, " %.2f" % Decimal(j).quantize(Decimal('0.01'), ROUND_HALF_UP))
            self.computed_dp.insert(END, '\n')

mainWindow = Tk()
app = OlaGUI(mainWindow)
app.text_changed()
mainWindow.mainloop()
