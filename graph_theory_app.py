import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#Qt
#QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
class Background(QGraphicsEllipseItem, QWidget):
    myDots = []
    mylines = []
    vid = 1
    totalVertices = 0
    totalDegree = 0
    def __init__(self):
        super().__init__(-150, -300, 1500, 1500)
        self.setBrush(Qt.black)
        self.setAcceptHoverEvents(True) 

        self.lable = QLabel("n = " + str(self.totalVertices), alignment = Qt.AlignCenter)
        
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.lable)
        self.proxy.setPos(10, 10)

        self.lable2 = QLabel("total deg = " + str(2*len(self.mylines)), alignment = Qt.AlignCenter)
        self.proxy2 = QGraphicsProxyWidget(self)
        self.proxy2.setWidget(self.lable2)
        self.proxy2.setPos(10, 30)

        view.add(self)
        view.add(self.proxy)
        view.add(self.proxy2)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            dot = Vertex(event.scenePos().x()-25 , event.scenePos().y()-25 , 50, self.vid)
            self.setVertexLabel(1)
            self.vid = self.vid + 1
            self.myDots.append(dot)
            view.add(dot)
            
            
            view.show()
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_P:
            for dots in myDots:
                for connectedDots in dots.get:
                    pass

    def checkForLine(self, currentDot):
        if currentDot.getDoubleClicked() == 2:
            line = SelfGraphicsLineItem(currentDot)
            currentDot.setDoubleClicked(0)
            currentDot.addConnectedVertex(currentDot)
            currentDot.addLine(line)
            self.mylines.append(line)
            view.add(line)
            view.show()
            return
        for dots in self.myDots:
            if dots.getDoubleClicked() and dots != currentDot:
                if dots.checkParallel(currentDot) == 1:
                    line = GraphicsLineItem(dots, currentDot, 1)
                elif dots.checkParallel(currentDot) == 2:
                    line = GraphicsLineItem(dots, currentDot, 2)
                elif dots.checkParallel(currentDot) > 2:
                    print("max parallel edges sorry\n")
                    return 0
                else:
                    line = GraphicsLineItem(dots, currentDot, 0)

                currentDot.setDoubleClicked(0)
                dots.setDoubleClicked(0)
                
                currentDot.addConnectedVertex(dots)
                dots.addConnectedVertex(currentDot)

                currentDot.addLine(line)
                dots.addLine(line)

                self.mylines.append(line)
                view.add(line)
                view.show()
                backdrop.setDegreeLabel()

    def removeLine(self, nLine):
        print('removed line')
        self.mylines.remove(nLine)  

    def removeDot(self, nDot):
        print('removed vertex ' + str(nDot.getVid()))
        self.myDots.remove(nDot)
    def setVertexLabel(self, addorRemove):
        if(addorRemove):
            self.totalVertices += 1
            self.lable = QLabel("n = " + str(self.totalVertices))
            self.proxy.setWidget(self.lable)
            self.proxy.setPos(10,10)
        else:
            self.totalVertices -= 1
            self.lable = QLabel("n = " + str(self.totalVertices))
            self.proxy.setWidget(self.lable)
            self.proxy.setPos(10,10)
    def setDegreeLabel(self):
        self.lable2 = QLabel("total deg = " + str(2*len(self.mylines)), alignment = Qt.AlignCenter)
        self.proxy2.setWidget(self.lable2)
        self.proxy2.setPos(10,30)
        
    def getMyDots(self):
        return self.myDots
    def getMyLines(self):
        return self.mylines
    def getDot(self):
        return self.myDots[0]
    def getLine(self):
        return self.mylines[0]
    def reduceDots(self):
        self.myDots.pop(0)
    def reduceLines(self):
        self.mylines.pop(0)
    def setVid(self, nVid):
        self.vid = nVid


class MyWidget(QWidget):
    pos1 = [0,0]
    pos2 = [0,0]

    def __init__(self, source, destination):
        super().__init__()
        self.pos1 = source
        self.pos2 = destination
        self.setGeometry(source.getx(), source.gety(), destination.getx(), destination.gety())
        view.add(self)
        view.show()

class SelfGraphicsLineItem(QGraphicsLineItem):
    def __init__(self, source, parent=None):
        super().__init__(parent)
        self.source = source
        self.setPen(Qt.white)
        self.setLine(QLineF(self.source.getx() + 25, self.source.gety() + 5, self.source.getx() - 5, self.source.gety() + 25))
        self.setLine(QLineF(self.source.getx() + 25, self.source.gety() + 45, self.source.getx() - 5, self.source.gety() + 25))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()


class GraphicsLineItem(QGraphicsLineItem):

    def __init__(self, source, destination, parallel, parent=None):
        super().__init__(parent)
        self.endpoints = [0,0]
        self.source = source
        self.destination = destination
        self.parallel = parallel
        self.endpoints[0] = source
        self.endpoints[1] = destination 
        self.setPen(Qt.white)
        if parallel == 1:
             self.setLine(QLineF(self.source.getx() + 45, self.source.gety() + 25, self.destination.getx() + 45, self.destination.gety() + 25))
        elif parallel == 2:
             self.setLine(QLineF(self.source.getx() + 5, self.source.gety() + 25, self.destination.getx() + 5, self.destination.gety() + 25))       
        else:
            self.setLine(QLineF(self.source.getx() + 25, self.source.gety() + 25, self.destination.getx() + 25, self.destination.gety() + 25))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setAcceptHoverEvents(True)
        

        print("line added between vertex " + str(self.endpoints[0].getVid()) + " and vertex " + str(self.endpoints[1].getVid()))
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()
        
    def mousePressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            app.instance().restoreOverrideCursor()
            self.source.removeConnectedVertex(self.destination)
            self.destination.removeConnectedVertex(self.source)
            self.source.removeLine(self)
            self.destination.removeLine(self)
            backdrop.removeLine(self)

            view.scene.removeItem(self)
            backdrop.setDegreeLabel()

    def mouseReleaseEvent(self, event):
        app.instance().restoreOverrideCursor()   
    
    def moveLine(self, dot):
        if dot.getVid() == self.endpoints[0].getVid():        #change source x y
            if(self.parallel == 1):
                self.setLine(dot.getx() + 45, dot.gety() + 25, self.destination.getx() + 45, self.destination.gety() + 25)
            elif(self.parallel == 2):
                self.setLine(dot.getx() + 5, dot.gety() + 25, self.destination.getx() + 5, self.destination.gety() + 25)
            else:
                self.setLine(dot.getx() + 25, dot.gety() + 25, self.destination.getx() + 25, self.destination.gety() + 25)

        else:
            if(self.parallel == 1):
                self.setLine(self.source.getx() + 45, self.source.gety() + 25, dot.getx() + 45, dot.gety() + 25)   
            elif(self.parallel == 2):
                self.setLine(self.source.getx() + 5, self.source.gety() + 25, dot.getx() + 5, dot.gety() + 25)   
            else:
                self.setLine(self.source.getx() + 25, self.source.gety() + 25, dot.getx() + 25, dot.gety() + 25)   
                         #change destination x y
        #self.move()

        #self.source.moved.connect(self.move)
        #self.destination.moved.connect(self.move) 
class clrButton(QGraphicsEllipseItem):
    def __init__(self, text, x, y, r, type):
        super().__init__(0, 0, r, r)
        self.r = r
        self.setPos(x, y)
        self.lable = QLabel(text, alignment = Qt.AlignCenter)
        

        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.lable)
        self.proxy.setPos(15, y + r/4)
        self.setBrush(Qt.red)
        self.setAcceptHoverEvents(True)

        view.add(self)
        view.add(self.proxy)

    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)
        explain_str = "Push This button to delete all Vertices"
        self.explain = QLabel(explain_str, alignment = Qt.AlignCenter)
        self.ex_proxy = QGraphicsProxyWidget(self)
        self.ex_proxy.setWidget(self.explain)
        self.ex_proxy.setPos(100, 10)
        view.add(self.ex_proxy)


    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()
        view.scene.removeItem(self.ex_proxy)
    #mouse click event
    def mousePressEvent(self, event):
        while(len(backdrop.getMyDots())):
            dots = backdrop.getDot()
            view.scene.removeItem(dots.proxy)
            view.scene.removeItem(dots)
            backdrop.setVertexLabel(0)
            backdrop.reduceDots()
        while(len(backdrop.getMyLines())):
            lines = backdrop.getLine()

            view.scene.removeItem(lines)
            #backdrop.setVertexLabel(0)
            backdrop.reduceLines()
        backdrop.setVid(1)
        backdrop.setDegreeLabel()
class button(QGraphicsEllipseItem):
    def __init__(self, text, x, y, r, type):
        super().__init__(0, 0, r, r)
        self.r = r
        self.setPos(x, y)
        self.lable = QLabel(text, alignment = Qt.AlignCenter)
        

        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.lable)
        self.proxy.setPos(x - (r-r/4), y + r/4)
        self.setBrush(Qt.red)
        self.setAcceptHoverEvents(True)

        view.add(self)
        view.add(self.proxy)

    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)
        explain_str = "Push This button to perform a\n2 color transformation of the graph\nand check terminal to see\nif the graph is bipartite"
        self.explain = QLabel(explain_str, alignment = Qt.AlignCenter)
        self.ex_proxy = QGraphicsProxyWidget(self)
        self.ex_proxy.setWidget(self.explain)
        self.ex_proxy.setPos(100, 10)
        view.add(self.ex_proxy)


    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()
        view.scene.removeItem(self.ex_proxy)
    #mouse click event
    def mousePressEvent(self, event):
        self.bipartite()

    def getx(self):
        return self.x
    def gety(self):
        return self.y

    def bipartite(self):
        vertexArray = []
        bipartite1 = []
        bipartite2 = []

        for dots in backdrop.getMyDots():
            vertexArray.append(dots)
        
        for dots in vertexArray:
            dots.setBipartiteColor(0)

        for dots in vertexArray:
            if not dots.getBipartiteColor(): #dot is blue
                for connectedDots in dots.getConnectedVertices():
                    connectedDots.setBrush(Qt.red)
                    connectedDots.setBipartiteColor(1)
            else:
                for connectedDots in dots.getConnectedVertices():
                    connectedDots.setBrush(Qt.blue)
                    connectedDots.setBipartiteColor(0)
        for vertex in vertexArray:
            if vertex.getBipartiteColor():
                bipartite1.append(vertex)
            else:
                bipartite2.append(vertex)
        for vertex in bipartite1:
            for connectedVertex in vertex.getConnectedVertices():
                if connectedVertex not in bipartite2:
                    print('The graph is not bipartite')
                    vertexArray.clear()
                    bipartite1.clear()
                    bipartite2.clear()
                    return 
        print('The graph is indeed bipartite, Yay')
        for vertex in bipartite1:
            vertex.setBrush(Qt.red)
        for vertex in bipartite2:
            vertex.setBrush(Qt.blue)
        vertexArray.clear()
        bipartite1.clear()
        bipartite2.clear()      
class Vertex(QGraphicsEllipseItem):
    lines = []
    connectedVertices = []
    bipartiteColor = 0

    def __init__(self, x, y, r, ID):
        super().__init__(0, 0, r, r)
        self.radius = 0
        self.doubleClicked = 0
        self.connectedVertices = []
        self.lines = []
        self.setPos(x, y)
        self.vid = ID
        self.lable = QLabel(str(ID), alignment = Qt.AlignCenter)
        self.color = 0
        
        self.lable.setAutoFillBackground(False)
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.lable)
        self.proxy.setPos(x + r, y)
        view.add(self.proxy)
        
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)
        self.radius = r

        
    #mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)
    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    #mouse click event
    def mousePressEvent(self, event):
        self.setBrush(Qt.yellow)
        if event.modifiers() == Qt.ControlModifier:
            backdrop.setVertexLabel(0)
            app.instance().restoreOverrideCursor()
            i = 0
            while(len(self.connectedVertices) > 0):
                self.connectedVertices[0].removeConnectedVertex(self)
                self.connectedVertices[0].removeLine(self.lines[i])
                self.connectedVertices.pop(0)
                i = i + 1

            while(len(self.lines) > 0):
                backdrop.removeLine(self.lines[0])
                view.scene.removeItem(self.lines[0])
                self.lines.pop(0)
            backdrop.removeDot(self)
            view.scene.removeItem(self.proxy)
            view.scene.removeItem(self)

        elif event.modifiers() == Qt.ShiftModifier:
            self.doubleClicked = 1
            backdrop.checkForLine(self)
        elif event.button() == Qt.RightButton:
            if self.color < 3:
                self.color += 1
            else:
                self.color = 0
        backdrop.setDegreeLabel()      
    #mouse drag event
    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()
        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(updated_cursor_x, updated_cursor_y)
        self.proxy.setPos(updated_cursor_x + self.getr(), updated_cursor_y)

        if(self.lines):
            for curLine in self.lines:
                curLine.moveLine(self)

    #mouse release event
    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))
        for dots in self.connectedVertices:
            print('connected to vertex ' + str(dots.getVid()))
        if self.color == 0:
            self.setBrush(Qt.blue)
        elif self.color == 1:
            self.setBrush(Qt.green)
        elif(self.color == 2):
            self.setBrush(Qt.red)
        elif(self.color == 3):
            self.setBrush(Qt.white)
    def checkParallel(self, newDot):
        count = 0
        for dots in self.connectedVertices:
            if dots == newDot:
                count += 1
        return count

    def getDoubleClicked(self):
        return self.doubleClicked

    def getx(self):
        return self.pos().x()
    
    def gety(self):
        return self.pos().y()

    def getr(self):
        return self.radius

    def getVid(self):
        return self.vid

    def getBipartiteColor(self):
        return self.bipartiteColor
    
    def getConnectedVertices(self):
        return self.connectedVertices
    
    def setBipartiteColor(self, colorInt):
        self.bipartiteColor = colorInt

    def setDoubleClicked(self, val):
        self.doubleClicked = val
    
    def addConnectedVertex(self, adjacentVertex):
        self.connectedVertices.append(adjacentVertex)
        
    def removeConnectedVertex(self, adjacentVertex):
        self.connectedVertices.remove(adjacentVertex)

    def addLine(self, nLine):
        self.lines.append(nLine)
        print("vertex " + str(self.vid) + " added a line")
    def removeLine(self, nLine):
        self.lines.remove(nLine)

class GraphicView(QGraphicsView):

    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 1200, 1000)
        self.setBackgroundBrush(Qt.black)
        self.setWindowTitle("Graph Theory App")

    def add(self, obj):
        self.scene.addItem(obj)

   

app = QApplication(sys.argv)
view = GraphicView()
backdrop = Background()
def main():
    
    
    #view.add(backdrop)
    b1 = button("Bipartite\nButton", 100, 10, 100, 1)
    view.add(b1)
    clrbutton = clrButton("Clear Button", 800, 10, 100, 1)
    view.add(clrbutton)
    view.show()

    sys.exit(app.exec_())


main()
