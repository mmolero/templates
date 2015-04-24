"""VTK Helper Methods
"""
#Author: Miguel Molero <miguel.molero@gmail.com>

import numpy as np
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
from vtk import vtkPoints, vtkCellArray, vtkUnsignedCharArray, vtkPolyData, vtkPolyDataMapper, vtkActor


def polydata_from_numpy(coords, color):
    """

    :param coords:
    :param color:
    :return:
    """

    Points = vtkPoints()
    Vertices = vtkCellArray()
    Colors = vtkUnsignedCharArray()
    Colors.SetName("colors")
    Colors.SetNumberOfComponents(3)

    def append_coords(item):
        id = Points.InsertNextPoint(item[0], item[1], item[2])
        Vertices.InsertNextCell(1)
        Vertices.InsertCellPoint(id)

    def append_color(item):
        Colors.InsertNextTuple3(item[0], item[1], item[2])


    if color is None:

        map(append_coords, coords)
        map(append_color, [[128, 128, 128]]*len(coords))

    else:
        size = np.shape(color)
        if len(size)==1:
           map(append_coords, coords)
           map(append_color, np._c[color, color, color])
        else:
            map(append_coords, coords)
            map(append_color, color)


    PolyData = vtkPolyData()
    PolyData.SetPoints(Points)
    PolyData.SetVerts(Vertices)
    PolyData.GetPointData().SetScalars(Colors)
    PolyData.GetPointData().SetActiveScalars("colors")

    return PolyData


def actor_from_polydata(PolyData):
    """
    Returns the VTK Actor from vtkPolyData Structure
    """
    mapper = vtkPolyDataMapper()
    mapper.SetInput(PolyData)
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(2)
    return actor