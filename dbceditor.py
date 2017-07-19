import sys
from PyQt4 import QtGui, QtCore
import wow.dbc


class DbcTableModel(QtCore.QAbstractTableModel):

    def __init__(self, dbc):
        super(DbcTableModel).__init__(self)
        self.dbc = dbc

    def rowCount(self):
        return len(self.dbc.records)

    def columnCount(self):
        return len(self.dbc.records[0])


def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    w.resize(480, 320)
    w.setWindowTitle('Editor')
    w.show()

    l = QtGui.QTableWidget(w)
    l.setModel(DbcTableModel(wow.dbc.DbcFile(None)))
    l.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

