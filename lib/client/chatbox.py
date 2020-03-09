from PyQt5.QtWidgets import QTextBrowser


class ChatBox(QTextBrowser):

    def __init__(self, parent, size = 50):
        super().__init__(parent)
        self.max_size = size
        self.lines = []
        self.need_update = False

        self.setAcceptRichText(True)
        self.setReadOnly(True)
        self.setMinimumSize(400, 250)

    def add_line(self, line):
        if len(self.lines) >= self.max_size:
            self.lines.remove(self.lines[0])
        self.lines.append(line)
        self.need_update = True

    def add_lines(self, lines):
        for l in lines:
            self.addLine(l)

    def update(self):
        if self.need_update:
            self.need_update = False
            res = ""
            for l in self.lines:
                res += l + "\n"
            self.setText(res[:-1])
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
