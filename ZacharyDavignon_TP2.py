from PySide6.QtWidgets import QLineEdit,QCheckBox, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
import maya.cmds as cmds
import sys
import json
 
class MessageBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Message board") # Fait apparaitre la fenêtre
        self.create_ui() # Initialise le UI 


    # S'occupe de gérer tout la création d'UI
    def create_ui(self):
        layout = QVBoxLayout(self) #Type de layout  
        jsonLabel = QLabel("Enter JSON path")
        self.jsonPathEdit = QLineEdit()
        #Type de checkbox
        self.checkboxSelect = QCheckBox("Selected only")
        self.checkboxColor = QCheckBox("Outliner color enabled?")
        self.checkboxSort = QCheckBox("Sort A -> Z")

        label = QLabel("Outliner settings")
        #Bouton
        self.bouton = QPushButton("Organise Outliner")        
        self.bouton.clicked.connect(self.onStateChanged) # fonction qui sert a envoyer du courant vers la fonction qui a tout la logique pour l'organisateur

        # On ajoute tout les widget au layout
        layout.addWidget(jsonLabel)
        layout.addWidget(self.jsonPathEdit)
        layout.addWidget(label)
        layout.addWidget(self.checkboxSelect)
        layout.addWidget(self.checkboxColor)
        layout.addWidget(self.checkboxSort)
        layout.addWidget(self.bouton)

    # On lit le json avec le texte inséré dans la QLineEdit
    def json_reading(self):
        self.data = json.load(open(self.jsonPathEdit.text()))

    #Logique derrière l'organisateur
    def onStateChanged(self):
        # Pour pas que ca crash on teste le json avant pour être sur que ca fonctionne sinon on fait juste dire qu'il n'est pas valide
        try:
            self.json_reading()
            
        except:
            print("Impossible de lire le JSON")
            return

        cmds.undoInfo(openChunk=True) # Permet de retenir l'information en un groupe pour tout ctrl z après
        for names,color in self.data.items(): # Pour tout les items dans le json, on retient les keys dans names et les values dans color

                # Logique pour la sélection
            if self.checkboxSelect.isChecked(): # Si le checkbox Select est checked 
                liste_objet = cmds.ls(f"{names}*", selection=True) # On met tout les objets qui ont les préfixes dans la règles et qui sont sélectionnés.
            else:
                liste_objet  = cmds.ls(f"{names}*") # Sinon on prend tout les objets avec les préfixed définis.

            for obj in liste_objet: # Pour tout les objets dans la liste d'objet
                
                # Logique pour la couleur
                if self.checkboxColor.isChecked(): # Si le checkbox couleur est checked
                    cmds.setAttr(f"{obj}.useOutlinerColor", True) # On active le droit de modifié la couleur dans l'outliner pour les objets
                    cmds.setAttr(f"{obj}.outlinerColor", color[0], color[1], color[2]) # On modifie la couleur avec les values qu'on a. Puisque dans la règles il ya R, G, B. J'ai prit la value séparé de chaque et modifié chaque valeur par rapport par rapport à ce qui est donné.
                                    
                else:
                    cmds.setAttr(f"{obj}.useOutlinerColor", False) # On enlève le droit de modifié la couleur, donc aucune couleur est appliqué, un genre de CTRL Z dans l'organisateur.
            
            
                # Logique pour ranger en ordre alphabétique
                if self.checkboxSort.isChecked(): # Si la checkbox Sort est checked
                    liste_objet.sort() # On appel la fonction sort déja implémenté
                    for i in liste_objet: # Pour chaque objet dans la liste
                        cmds.reorder(i,back=True) # On remet en ordre alphabétique
        cmds.undoInfo(closeChunk=True) # Ferme le groupe pour le CTRL Z


            
        
def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()