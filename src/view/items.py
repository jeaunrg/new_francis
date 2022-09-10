import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from src.view.views import WidgetView


class WidgetItem(QtWidgets.QGraphicsRectItem):
    def __init__(
        self,
        view: WidgetView,
        position: QtCore.QPointF,
        width: int = 70,
        height: int = 10,
    ):
        super().__init__(0, -height, width, height)
        self.view = view
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setBrush(QtCore.Qt.lightGray)
        self.moveBy(position.x(), position.y())
        self.setCursor(QtCore.Qt.SizeAllCursor)
        proxy = QtWidgets.QGraphicsProxyWidget(self)
        proxy.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemIsSelectable
        )
        proxy.setWidget(view)
        self.proxy_rect = proxy.rect

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            self.view.position_changed.emit()
        return super().itemChange(change, value)


class GraphLinkItem(QtWidgets.QGraphicsPolygonItem):
    def __init__(self):
        super().__init__()
        border_color = (0, 150, 0)
        border_width = 2
        color = (0, 150, 0)
        self.setZValue(-1)
        self.setPen(QtGui.QPen(QtGui.QColor(*border_color), border_width))
        self.setBrush(QtGui.QColor(*color))
        self.width = 5
        self.arrow_width = 10
        self.arrow_len = 10
        self.space = [10, 20]

    def intersects(
        self, line: QtCore.QLineF, rect: QtCore.QRect, rect_position: QtCore.QPoint
    ) -> QtCore.QPointF:
        """
        This method find the intersection between widget rect and line
        by checking the intersection between line and each rect border line.
        As the line comes from inside the rect, only one intersection exists
        """
        points = [
            rect.bottomLeft(),
            rect.bottomRight(),
            rect.topRight(),
            rect.topLeft(),
        ]
        for i in range(4):
            border = QtCore.QLineF(
                rect_position + points[i - 1], rect_position + points[i]
            )
            try:
                intersection_type, intersection_point = line.intersects(border)
            except AttributeError:
                intersection_point = QtCore.QPointF()
                intersection_type = line.intersect(border, intersection_point)
            if intersection_type == QtCore.QLineF.BoundedIntersection:
                return intersection_point
        return QtCore.QPointF()

    def draw(self, parent: WidgetItem, child: WidgetItem):
        """
        This method create the arrow between child and parent
        
                               p23
                                 |\
           p11 ______________ p21| \
        p1    |                     \  p2
              |______________       /
           p12                p22| /
                                 |/
                               p24
        """
        # build direction line
        r1, r2 = parent.proxy_rect(), child.proxy_rect()
        line = QtCore.QLineF(parent.pos() + r1.center(), child.pos() + r2.center())

        # build unit vectors
        unit = line.unitVector().p2() - line.unitVector().p1()
        normal = (
            line.normalVector().unitVector().p2()
            - line.normalVector().unitVector().p1()
        )

        # set arrow points
        parent_intersection = self.intersects(line, r1, parent.pos())
        if parent_intersection is None:
            return self.setPolygon(QtGui.QPolygonF())
        child_intersection = self.intersects(line, r2, child.pos())
        if child_intersection is None:
            return self.setPolygon(QtGui.QPolygonF())
        p1 = parent_intersection + unit * self.space[0]
        p2 = child_intersection - unit * self.space[1]
        p12 = p1 - normal * self.width
        p22 = p2 - normal * self.width - unit * self.arrow_len
        if np.sign((p22 - p12).x()) != np.sign(unit.x()) or np.sign(
            (p22 - p12).y()
        ) != np.sign(unit.y()):
            return self.setPolygon(QtGui.QPolygonF())
        p11 = p1 + normal * self.width
        p21 = p2 + normal * self.width - unit * self.arrow_len
        p23 = p2 + normal * self.arrow_width - unit * self.arrow_len
        p24 = p2 - normal * self.arrow_width - unit * self.arrow_len
        self.setPolygon(QtGui.QPolygonF([p11, p21, p23, p2, p24, p22, p12, p11]))
