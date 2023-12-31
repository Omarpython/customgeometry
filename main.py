#####################################################
## Name: None                                      ##
## Type: Graphic                                   ##
## Auther: Omar Mohammed                           ##
## Link GitHub: https://github.com/Omarpython      ##
## copyright (C) 2022                              ##
#####################################################

from PyQt5.QtCore import pyqtProperty, pyqtSignal, QPointF, QUrl
from PyQt5.QtGui import QColor, QGuiApplication
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import (QQuickItem, QQuickView, QSGFlatColorMaterial,
        QSGGeometry, QSGGeometryNode, QSGNode)

import icons_rc


class BezierCurve(QQuickItem):

    p1Changed = pyqtSignal(QPointF)

    @pyqtProperty(QPointF, notify=p1Changed)
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, p):
        if self._p1 != p:
            self._p1 = QPointF(p)
            self.p1Changed.emit(p)
            self.update()

    p2Changed = pyqtSignal(QPointF)

    @pyqtProperty(QPointF, notify=p2Changed)
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, p):
        if self._p2 != p:
            self._p2 = QPointF(p)
            self.p2Changed.emit(p)
            self.update()

    p3Changed = pyqtSignal(QPointF)

    @pyqtProperty(QPointF, notify=p3Changed)
    def p3(self):
        return self._p3

    @p3.setter
    def p3(self, p):
        if self._p3 != p:
            self._p3 = QPointF(p)
            self.p3Changed.emit(p)
            self.update()

    p4Changed = pyqtSignal(QPointF)

    @pyqtProperty(QPointF, notify=p4Changed)
    def p4(self):
        return self._p4

    @p4.setter
    def p4(self, p):
        if self._p4 != p:
            self._p4 = QPointF(p)
            self.p4Changed.emit(p)
            self.update()

    segmentCountChanged = pyqtSignal(int)

    @pyqtProperty(int, notify=segmentCountChanged)
    def segmentCount(self):
        return self._segmentCount

    @segmentCount.setter
    def segmentCount(self, count):
        if self._segmentCount != count:
            self._segmentCount = count
            self.segmentCountChanged.emit(count)
            self.update()

    def __init__(self, parent=None):
        super(BezierCurve, self).__init__(parent)

        self._p1 = QPointF(0, 0)
        self._p2 = QPointF(1, 0)
        self._p3 = QPointF(0, 1)
        self._p4 = QPointF(1, 1)

        self._segmentCount = 32

        self._root_node = None

        self.setFlag(QQuickItem.ItemHasContents, True)

    def updatePaintNode(self, oldNode, nodeData):
        if self._root_node is None:
            self._root_node = QSGGeometryNode()

            geometry = QSGGeometry(QSGGeometry.defaultAttributes_Point2D(),
                    self._segmentCount)
            geometry.setLineWidth(2)
            geometry.setDrawingMode(QSGGeometry.GL_LINE_STRIP)
            self._root_node.setGeometry(geometry)
            self._root_node.setFlag(QSGNode.OwnsGeometry)

            material = QSGFlatColorMaterial()
            material.setColor(QColor(255, 0, 0))
            self._root_node.setMaterial(material)
            self._root_node.setFlag(QSGNode.OwnsMaterial)
        else:
            geometry = self._root_node.geometry()
            geometry.allocate(self._segmentCount)

        w = self.width()
        h = self.height()
        vertices = geometry.vertexDataAsPoint2D()

        for i in range(self._segmentCount):
            t = i / float(self._segmentCount - 1)
            invt = 1 - t

            pos = invt * invt * invt * self._p1 \
                    + 3 * invt * invt * t * self._p2 \
                    + 3 * invt * t * t * self._p3 \
                    + t * t * t * self._p4

            vertices[i].set(pos.x() * w, pos.y() * h)

        self._root_node.markDirty(QSGNode.DirtyGeometry)

        return self._root_node


if __name__ == '__main__':
    import sys

    app = QGuiApplication(sys.argv)

    qmlRegisterType(BezierCurve, "CustomGeometry", 1, 0, "BezierCurve")

    view = QQuickView()
    format = view.format()
    format.setSamples(16)
    view.setFormat(format)

    view.setSource(QUrl('qrc:///scenegraph/customgeometry/main.qml'))
    view.show()

    sys.exit(app.exec_())
