"""
Template for a MainWindow with a QVTKWidget as central Widget
"""
#Author: Miguel Molero <miguel.molero@gmail.com>

from PySide.QtCore import *
from PySide.QtGui import *
from vtk import vtkRenderer, vtkPLYReader, vtkPolyData,  vtkPolyDataMapper, vtkActor

from MainWindowBase import MainWindowBase
from graphics.QVTKWidget import QVTKWidget

class QVTKMainWindowBase(MainWindowBase):
    """
    Template Class for a MainWindow Instance with a QVTKWidget as central Widget
    It inherits from MainWindowBase
    """
    def __init__(self, parent=None):
        super(QVTKMainWindowBase, self).__init__(parent)


    def setupGraphicView(self):

        widget = QWidget(self)
        widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.renderer = vtkRenderer()
        self.renderer.GradientBackgroundOn()
        self.renderer.SetBackground2(0.0,0.0,0.0)
        self.renderer.SetBackground(192/255.0, 192/255.0,192/255.0)

        self.vtkWidget = QVTKWidget(widget)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)

        self.vtkWidget.Initialize()
        self.vtkWidget.Start()
        self.vtkWidget.addAxes()

        layout = QVBoxLayout()
        layout.addWidget(self.vtkWidget)
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def addActor(self, actor):
        self.renderer.AddActor(actor)

    def setActor(self, actor):
        self.renderer.RemoveAllViewProps()
        self.renderer.AddActor(actor)

    def updateView(self):

        self.vtkWidget.Render()
        self.vtkWidget.show()

    def removeViewProps(self):

        #Add Actions

        self.setTitle()
        self.renderer.RemoveAllViewProps()
        self.renderer.ResetCamera()
        self.vtkWidget.Render()
        self.vtkWidget.show()



if __name__=='__main__':
    import sys
    import pandas as pd
    import numpy as np
    from graphics.vtkHelper import polydata_from_numpy, actor_from_polydata

    app = QApplication(sys.argv)
    win = QVTKMainWindowBase()
    win.show()

    #Read XYZ File -> x,y,z, r,g, b
    filename = r"tests\data\tunnel_scan.xyz"
    df = pd.read_csv(filename, sep = ' ')
    #export to numpy array
    data = df.as_matrix()

    #Because the tunnel coordinates are very unbalanced between them, apply a rescale
    mx = data[:,0].mean()
    my = data[:,1].mean()
    mz = data[:,2].mean()
    coords = data[:,0:3] - np.array([mx, my, mz])
    color = data[:,3:]

    #Get a vtkPolyData Structure and vtkActor from the numpy array
    polydata = polydata_from_numpy(coords, color)
    actor = actor_from_polydata(polydata)

    #Add Actor to render
    win.addActor(actor)
    win.updateView()

    app.exec_()
