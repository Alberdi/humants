from PySide import QtGui, QtCore
import sys
import time

import entity

class MainWindow(QtGui.QWidget):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.setGeometry(0, 0, 640, 480)
    self.setWindowTitle('Humants')
    self.timer = QtCore.QBasicTimer()
    self.x = 0

  def add_entity(self, entity):
    pixmap = QtGui.QPixmap("res/lumberjack.png")
    lbl = QtGui.QLabel(self)
    lbl.setPixmap(pixmap)
    entity.add_attribute("render_label", lbl)
    entity.add_handler("moved", self.moved_handler)
    self.entity = entity

  def moved_handler(self, e, p):
    new_x, new_y = p["new_position"][0]*72, p["new_position"][1]*72
    e.attribute("render_label").move(new_x, new_y)

  def timerEvent(self, event):
    if event.timerId() == self.timer.timerId():
      self.entity.message("moved", {"new_position": (self.x, 0)})
      self.x += 1

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  ex = MainWindow()
  e = entity.Entity()
  ex.add_entity(e)
  ex.show()
  ex.timer.start(2000, ex)
  sys.exit(app.exec_())

