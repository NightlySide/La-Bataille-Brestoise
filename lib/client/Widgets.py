from PyQt5 import QtWidgets, QtCore, QtGui


class Bar(QtWidgets.QWidget):

    def __init__(self, parent, geom, text, min_val, max_val, start_val):
        super().__init__(parent)
        self.setGeometry(geom)
        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setMinimum(min_val)
        self.progress.setMaximum(max_val)
        self.progress.setValue(start_val)
        self.progress.setTextVisible(False)
        self.text = QtWidgets.QLabel(self)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setText(text)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.stretch(1)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.progress)
        self.setLayout(self.layout)

    def update(self):
        super().update()
        self.progress.update()
        self.text.update()

    def setText(self, text):
        self.text.setText(text)
        self.update()

    def setValue(self, min_val, max_val, value):
        self.progress.setMinimum(min_val)
        self.progress.setMaximum(max_val)
        self.progress.setValue(value)
        self.update()