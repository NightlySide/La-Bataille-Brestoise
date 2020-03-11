from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtCore import Qt

class ChatBox(QTextBrowser):
    """
    Contrôle la chatbox du jeu. Classe nécessaire pour pouvoir
    utiliser PyQt5 dans un thread différent.

    Args:
        parent (QWidget): le parent auquel la chatbox est attachée
        size (int): le nombre maximal de lignes dans la chatbox

    Attributes:
        max_size (int): le nombre maximal de lignes dans la chatbox
        lines (list): les lignes de la chatbox
        need_update (bool): indique si la chatbox doit être mise à jour
    """
    def __init__(self, parent, size=50):
        super().__init__(parent)
        self.max_size = size
        self.lines = []
        self.need_update = False

        self.setAcceptRichText(True)
        self.setReadOnly(True)
        self.setMinimumSize(400, 250)
        self.setFocusPolicy(Qt.NoFocus)

    def add_line(self, line):
        """
        Ajoute la ligne 'line' aux lignes de la chatbox
        pour le prochain update.

        Args:
            line (str): la ligne à ajouter
        """
        if len(self.lines) >= self.max_size:
            self.lines.remove(self.lines[0])
        self.lines.append(line)
        self.need_update = True

    def add_lines(self, lines):
        """
        Ajoute la liste de lignes aux lignes de la chatbox
        pour le prochain update.

        Args:
            lines (list): liste des lignes à ajouter
        """
        for l in lines:
            self.addLine(l)

    def update(self):
        """
        Met à jour la chatbox. Fonction appelée par le Thread
        contenant PyQt5.
        La mise à jour ne s'effectue que si elle est nécessaire.
        """
        if self.need_update:
            self.need_update = False
            res = ""
            for l in self.lines:
                res += l + "\n"
            self.setText(res[:-1])
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
