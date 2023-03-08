import vtk
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData
)

colors = vtk.vtkNamedColors()

input1 = vtkPolyData()
input2 = vtkPolyData()
input3 = vtkPolyData()

cylindeSource1 = vtk.vtkCylinderSource()
cylindeSource1.SetCenter(0,0,0)
cylindeSource1.SetRadius(3)
cylindeSource1.SetHeight(20)
cylindeSource1.SetResolution(20)
cylindeSource1.Update()
input1.ShallowCopy(cylindeSource1.GetOutput())

cylindeSource2 = vtk.vtkCylinderSource()
cylindeSource2.SetCenter(7,0,0)
cylindeSource2.SetRadius(3)
cylindeSource2.SetHeight(20)
cylindeSource2.SetResolution(20)
cylindeSource2.Update()
input2.ShallowCopy(cylindeSource2.GetOutput())

cylindeSource3 = vtk.vtkCylinderSource()
cylindeSource3.SetCenter(-13,0,0)
cylindeSource3.SetRadius(3)
cylindeSource3.SetHeight(20)
cylindeSource3.SetResolution(20)
cylindeSource3.Update()
input3.ShallowCopy(cylindeSource3.GetOutput())

appendFilter = vtkAppendPolyData()
appendFilter.AddInputData(input1)
appendFilter.AddInputData(input2)
appendFilter.AddInputData(input3)
appendFilter.Update()

###########
def limited_plane(centerPoint,normal,radius):
    #centerPoint:平面中心点
    #normal：平面法向量
    #radius：平面半径
    ####################
    sphere = vtk.vtkSphere()
    sphere.SetRadius(radius)
    sphere.SetCenter(centerPoint)
    plane = vtk.vtkPlane()
    plane.SetNormal(normal)
    plane.SetOrigin(centerPoint)
    myplane = vtk.vtkImplicitBoolean()
    #myplane.SetOperationType(0,1,2...)#0 union VTK_UNION 	VTK_INTERSECTION VTK_DIFFERENCE VTK_UNION_OF_MAGNITUDES
    myplane.AddFunction(plane)
    myplane.AddFunction(sphere)
    myplane.SetOperationTypeToIntersection()
    print(myplane)
    return myplane
#############

centerPoint=(0,0,0)
normal=(0,1,1)
radius=14
myplane1 = vtk.vtkImplicitBoolean()
myplane1 = limited_plane(centerPoint,normal,radius)

clip = vtk.vtkClipPolyData()
clip.SetInputConnection(appendFilter.GetOutputPort());
clip.SetClipFunction(myplane1);



clipMapper = vtk.vtkPolyDataMapper()
clipMapper.SetInputConnection(clip.GetOutputPort())
clipMapper.ScalarVisibilityOff()

backProp = vtk.vtkProperty()
backProp.SetColor(colors.GetColor3d("Tomato"))

clipActor = vtk.vtkActor()
clipActor.SetMapper(clipMapper);
clipActor.SetBackfaceProperty(backProp);
clipActor.GetProperty().SetColor(colors.GetColor3d("Banana"));
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow);

renderer.AddActor(clipActor);
renderer.SetBackground(colors.GetColor3d("SlateGray"));
renderWindow.SetSize(500, 500);
renderWindow.SetWindowName("vtkImplicitBoolean");
renderWindow.Render();
interactor.Start();
