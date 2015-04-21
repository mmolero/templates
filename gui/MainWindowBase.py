"""
Template MainWindowBase.py
"""

import os

from PySide.QtCore import *
from PySide.QtGui import *


NAME = "Template"

class MainWindowBase(QMainWindow):
    """
    Base Class for the MainWindow Object. This class should inherit its attributes and methods to a MainWindow Class
    """
    def __init__(self, parent = None):
        super(MainWindowBase, self).__init__(parent)

        self.init()

        self.createMenus()
        self.createToolBar()
        self.setupGraphicView()
        self.setupStatusBar()
        self.setupConnections()
        self.initSettings()

        QTimer.singleShot(0,self.loadInitialFile)


    def init(self):

        self.dirty = False
        self.reset = False
        self.filename = None
        self.recent_files = []
        self.dir_path = os.getcwd()
        self.software_name = NAME

        self.setGeometry(100,100,900,600)
        self.setMinimumSize(400,400)
        self.setMaximumSize(2000,1500)
        self.setWindowFlags(self.windowFlags())
        self.setWindowTitle(self.software_name)

        #Put here your init code


    def setTitle(self, fname):
        title = os.path.basename(fname)
        self.setWindowTitle("%s:%s"%(self.softwareName,title))

    def loadInitialFile(self):
        settings = QSettings()
        fname = unicode(settings.value("LastFile"))
        if fname and QFile.exists(fname):
            self.loadFile(fname)

    def loadFile(self, fname=None):

        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = unicode(action.data())
                if not self.okToContinue():
                    return
            else:
                return

        if fname:
            self.filename = None
            self.addRecentFile(fname)
            self.filename = fname
            self.dirty = False
            self.setTitle(fname)

            #Add More actions
            #
            #

    def addRecentFile(self, fname):

        if fname is None:
            return
        if not self.recentFiles.count(fname):
            self.recentFiles.insert(0,fname)
            while len(self.recentFiles)>9:
                self.recentFiles.pop()


    def createMenus(self):
        pass

    def setupConnections(self):
        pass

    def createToolBar(self):
        pass

    def setupGraphicView(self):
        pass

    def setupStatusBar(self):
        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)

        #Add more actions


    def initSettings(self):

        settings = QSettings()
        self.recentFiles = settings.value("RecentFiles")
        size = settings.value("MainWindow/Size",QSize(900,600))
        position = settings.value("MainWindow/Position",QPoint(50,50))
        self.restoreState(settings.value("MainWindow/State"))
        self.dir_path = settings.value("DirPath")
        #Retrives more options
        #

        if self.recentFiles is None:
            self.recentFiles = []

        self.resize(size)
        self.move(position)


        #Add more actions


    def resetSettings(self):

        settings = QSettings()
        settings.clear()
        self.reset = True
        self.close()


    def okToContinue(self):

        if self.dirty:
            reply = QMessageBox.question(self,
                                        "%s - Unsaved Changes"%self.softwareName,
                                        "Save unsaved changes?",
                                        QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)

            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.fileSave()

        return True


    def fileNew(self):
        pass


    def fileOpen(self):
        pass


    def fileSaveAs(self):
        pass

    def fileSave(self):
        pass


    def helpAbout(self):

        QMessageBox.about(self, "About %s"%NAME,
                          """
                          """)

    def closeEvent(self, event):

        if self.reset:
            return

        if self.okToContinue():
            settings = QSettings()
            filename = self.filename if self.filename is not None else None
            settings.setValue("LastFile", filename)
            recentFiles = self.recentFiles if self.recentFiles else None
            settings.setValue("RecentFiles", recentFiles)
            settings.setValue("MainWindow/Size",	 self.size())
            settings.setValue("MainWindow/Position", self.pos())
            settings.setValue("MainWindow/State",	 self.saveState())
            #Set more options


        else:
            event.ignore()



if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindowBase()
    win.show()
    app.exec_()


