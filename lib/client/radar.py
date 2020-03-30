from random import randint

import numpy as np
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget
import time

from lib.client.global_client_registry import GCR
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur


class Radar(QWidget):

    def __init__(self, radius, speed=5, parent=None, refresh_rate=1/30):
        super().__init__(parent)
        self.setParent(parent)
        self.radius = radius
        self.angle = 0
        self.speed = speed
        self.time_counter = time.perf_counter()
        self.refresh_rate = refresh_rate
        self.enemies = [(randint(-int(radius*0.75), int(radius*0.75)) + 400//2,
                         randint(-int(radius*0.75), int(radius*0.75)) + 300//2) for _ in range(20)]
        self.points_to_draw = []
        self.to_remove = []
        self.temps_affichage = 300 / self.speed

        self.setFixedSize(400, 300)

    def update(self):
        if time.perf_counter() - self.time_counter > self.refresh_rate:
            self.time_counter = time.perf_counter()
            super().update()
            self.angle += self.refresh_rate * self.speed
            self.angle %= 360

            self.to_remove = []
            for pt in self.points_to_draw:
                pt[1] -= self.refresh_rate
                if pt[1] <= 0:
                    self.to_remove.append(pt)

            for element in self.to_remove:
                self.points_to_draw.remove(element)

    def paintEvent(self, event):
        qp = QPainter(self)
        y0 = self.height() // 2
        x0 = self.width() // 2
        x = np.cos(self.angle * np.pi / 180) * self.radius + x0
        y = np.sin(self.angle * np.pi / 180) * self.radius + y0
        origin = QPoint(x0, y0)
        dest = QPoint(x, y)

        for k in range(1, 5):
            qp.drawEllipse(origin, self.radius * k/4, self.radius * k/4)
        qp.drawLine(QPoint(x0 - self.radius, y0), QPoint(x0 + self.radius, y0))
        qp.drawLine(QPoint(x0, y0 - self.radius), QPoint(x0, y0 + self.radius))

        original_pen = qp.pen()
        new_pen = QPen()
        new_pen.setColor(Qt.green)
        new_pen.setWidth(2)
        qp.setPen(new_pen)
        qp.drawLine(origin, dest)
        qp.setPen(original_pen)

        for e in self.enemies:
            for pos, tps in self.points_to_draw:
                if pos == e:
                    break
            else:
                if Vecteur.est_entre(Vecteur(x0, y0), Vecteur(x, y), Vecteur(e[0], e[1]), epsilon=500):
                    self.points_to_draw.append([e, self.temps_affichage])

        for pt in self.points_to_draw:
            original_pen = qp.pen()
            new_pen = QPen()
            if pt[1] < 100 / self.speed:
                new_pen.setColor(Qt.darkGray)
            else:
                new_pen.setColor(Qt.red)
            new_pen.setWidth(5)
            qp.setPen(new_pen)
            qp.drawPoint(*pt[0])
            qp.setPen(original_pen)
