"""Basic Widget used to render vtk objects inside PySide Widget
"""
#Author: Miguel Molero <miguel.molero@gmail.com>

from PySide import QtCore, QtGui

from vtk import vtkOrientationMarkerWidget, vtkAxesActor
from vtk import vtkInteractorStyleTrackballCamera

from QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class QVTKWidget(QVTKRenderWindowInteractor):
    """
    Widget used to render vtk objects inside PySide Widget
    """
    def __init__(self, parent=None):
        super(QVTKWidget, self).__init__(parent)
        self._Iren.SetInteractorStyle (vtkInteractorStyleTrackballCamera ())

    def keyPressEvent(self, ev):

        QVTKRenderWindowInteractor.keyPressEvent(self, ev)

        if ev.key() < 256:
            key = str(ev.text())
        else:
            # Has modifiers, but an ASCII key code.
            #key = chr(ev.key())
            key = chr(0)

        #####
        ##Add Actions related to the key events


    def addAxes(self):

        self.widget = vtkOrientationMarkerWidget()
        axes = vtkAxesActor()
        axes.SetShaftTypeToLine()
        axes.SetTotalLength(0.5, 0.5, 0.5)
        self.widget.SetOutlineColor(0.9300,0.5700,0.1300)
        self.widget.SetOrientationMarker(axes)
        self.widget.SetInteractor(self._Iren)
        self.widget.SetViewport(0.80, 0.0, 1.0,0.25)
        self._widgetState = True
        self.widget.SetEnabled(self._widgetState)
        self.widget.InteractiveOff()


    def viewMX(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(-1, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 0, 1)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()


    def viewMY(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(0, -1, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 0, 1)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()


    def viewMZ(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(0, 0, -1)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 1, 0)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()



    def viewPX(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(1, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 0, 1)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()


    def viewPY(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(0, 1, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 0, 1)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()


    def viewPZ(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(0, 0, 1)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 1, 0)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()



def vtkWidgetExample():
    """A simple example that uses the vtkBasicWidget class."""
    from vtk import vtkPolyDataMapper, vtkActor
    from vtk import vtkRenderer
    from vtk import vtkConeSource

    # every QT app needs an app
    app = QtGui.QApplication(['vtkWidget'])

    # create the widget
    widget = QVTKWidget()
    widget.Initialize()
    widget.Start()
    widget.addAxes()

    ###########

    # if you dont want the 'q' key to exit comment this.
    widget.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

    ren = vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)

    cone = vtkConeSource()
    cone.SetResolution(8)
    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)

    ren.AddActor(coneActor)

    # show the widget
    widget.show()
    # start event processing
    app.exec_()

if __name__ == "__main__":
    vtkWidgetExample()
