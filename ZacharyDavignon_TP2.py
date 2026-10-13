from PySide6.QtWidgets import QLineEdit,QCheckBox, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
import maya.cmds as cmds
import sys
import json
 
class MessageBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Message board")
        self.create_ui()
        self.json_reading()

    def json_reading(self):
        self.data = json.load(open("C:\\Code\\tp2\\rules.json"))
        print(self.data)

        self.outline_names = list(self.data.keys())
        self.outline_color = list(self.data.values())

    def create_ui(self):
        layout = QVBoxLayout(self)
        jsonLabel = QLabel("Enter JSON path")
        self.jsonPathEdit = QLineEdit()
        self.checkboxSelect = QCheckBox("Selected only")
        self.checkboxColor = QCheckBox("Outliner color enabled?")
        self.checkboxSort = QCheckBox("Sort A -> Z")
        label = QLabel("Outliner settings")
        self.bouton = QPushButton("Organise Outliner")        
        self.bouton.clicked.connect(self.onStateChanged)
        layout.addWidget(jsonLabel)
        layout.addWidget(self.jsonPathEdit)
        layout.addWidget(label)
        layout.addWidget(self.checkboxSelect)
        layout.addWidget(self.checkboxColor)
        layout.addWidget(self.checkboxSort)
        layout.addWidget(self.bouton)

    

    def onStateChanged(self):
        if self.checkboxSelect.isChecked():
            liste_objet = cmds.ls(selection=True)
            print("Selected")
            print(liste_objet)
        else:
            print("tout")
            liste_objet = []
            for names in self.data:
                liste_objet  += cmds.ls(f"{names}*")
            print(liste_objet)

        for obj in liste_objet:
                    for names,color in self.data.items():
                        if self.checkboxColor.isChecked():
                            cmds.setAttr(f"{obj}.useOutlinerColor", True)
                            cmds.setAttr(f"{obj}.outlinerColor", color[0], color[1], color[2])
                            
                        else:
                            for names,k in self.data.items():
                                for obj in cmds.ls(f"{names}*"):
                                    cmds.setAttr(f"{obj}.useOutlinerColor", False)
        
        
        
        if self.checkboxSort.isChecked():
            outliners = cmds.getPanel(type='outlinerPanel')
            for i in outliners:
                editor = cmds.outlinerPanel(i, query=True,outlinerEditor=True)
                cmds.outlinerEditor(editor, edit=True, sortOrder='dagName')

        else:
            outliners = cmds.getPanel(type='outlinerPanel')
            for i in outliners:
                editor = cmds.outlinerPanel(i, query=True,outlinerEditor=True)
                cmds.outlinerEditor(editor, edit=True, sortOrder='none')
           


    def on_click(self):
        message = QMessageBox(self)
        message.setWindowTitle("Affichage réponse")



 
def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()