from PySide6.QtWidgets import QLineEdit,QCheckBox, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
import maya.cmds as cmds
import sys
import json
 
class MessageBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Message board")
        self.create_ui()

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

    def json_reading(self):
        self.data = json.load(open(self.jsonPathEdit.text()))
        print(self.data)


    def onStateChanged(self):
        try:
            self.json_reading()
            
        except:
            print("Impossible de lire le JSON")
            return

        cmds.undoInfo(openChunk=True)
        for names,color in self.data.items():
                
            if self.checkboxSelect.isChecked():
                liste_objet = cmds.ls(f"{names}*", selection=True)
                print(liste_objet)
            else:
                liste_objet  = cmds.ls(f"{names}*")

            for obj in liste_objet:
                if self.checkboxColor.isChecked():
                    cmds.setAttr(f"{obj}.useOutlinerColor", True)
                    cmds.setAttr(f"{obj}.outlinerColor", color[0], color[1], color[2])
                                    
                else:
                    cmds.setAttr(f"{obj}.useOutlinerColor", False)
            
            
            
                if self.checkboxSort.isChecked():
                    liste_objet.sort()
                    for i in liste_objet:
                        cmds.reorder(i,back=True)
        cmds.undoInfo(closeChunk=True)


            
           


 
def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()