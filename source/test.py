from Polyhedron import Polyhedron
from Scene import Scene
from RaySource import RaySource
from Point import Point
from Vector import Vector
from RectangularPlanarPolygon import RectangularPlanarPolygon

cup = Polyhedron("../Examples/cup/cup.obj", "materials/blood.csv")

source = RaySource(Point(0,20,0), Vector(0, -1, 1), 0, rectangle = RectangularPlanarPolygon([Point(-20,20,0), Point(-20,40,20), Point(0,40,20), Point(0,20,0)]))

scene = Scene()
scene.add_object(cup)
scene.add_object(source)
scene.show()