"""VTK Helper Methods
"""
#Author: Miguel Molero <miguel.molero@gmail.com>

import numpy as np
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
from vtk.util.numpy_support import get_numpy_array_type, create_vtk_array, get_vtk_array_type, numpy_to_vtkIdTypeArray
from vtk.util.numpy_support import get_vtk_to_numpy_typemap
from vtk import vtkPoints, vtkCellArray, vtkIdTypeArray, vtkUnsignedCharArray, vtkPolyData, vtkPolyDataMapper, vtkActor
from vtk import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor
from vtk import VTK_POINTS, VTK_FLOAT, VTK_CHAR, VTK_UNSIGNED_CHAR

def polydata_from_numpy(coords, color):
    """
    :param coords:
    :param color:
    :return:
    """

    Npts, Ndim = np.shape(coords)

    Points = vtkPoints()
    ntype = get_numpy_array_type(Points.GetDataType())
    coords_vtk = numpy_to_vtk(np.asarray(coords, order='C',dtype=ntype), deep=1)
    Points.SetNumberOfPoints(Npts)
    Points.SetData(coords_vtk)

    Cells = vtkCellArray()
    ids = np.arange(0,Npts, dtype=np.int64).reshape(-1,1)
    IDS = np.concatenate([np.ones(Npts, dtype=np.int64).reshape(-1,1), ids],axis=1)
    ids_vtk = numpy_to_vtkIdTypeArray(IDS, deep=True)

    Cells.SetNumberOfCells(Npts)
    Cells.SetCells(Npts,ids_vtk)

    if color is None:
        [[128, 128, 128]]*len(coords)

    size = np.shape(color)
    if len(size)==1:
        color = [128]*len(coords)
        color = np.c_[color, color, color]

    color_vtk = numpy_to_vtk(
            np.ascontiguousarray(color, dtype=get_vtk_to_numpy_typemap()[VTK_UNSIGNED_CHAR]),
            deep=True
        )

    color_vtk.SetName("colors")

    PolyData = vtkPolyData()
    PolyData.SetPoints(Points)
    PolyData.SetVerts(Cells)
    PolyData.GetPointData().SetScalars(color_vtk)

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


def display_from_actor(actor):
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    renderer.AddActor(actor)
    # enable user interface interactor
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)
    iren.Initialize()
    renderWindow.Render()
    iren.Start()
