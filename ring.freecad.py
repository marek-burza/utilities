# This script generates an STL file with an engraved ring.
# To use the script the following fonts are included:
#   http://www.dafont.com/pacifico.font
#   http://www.dafont.com/hearts-for-3d-fx.font
# Run the script as a parameter to the FreeCAD version 0.15
#
#
# This code is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for
# more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with code. If not, see <http://www.gnu.org/licenses/>.

import math
import os
import sys
import Draft
import Mesh

def sides(width, radius, thickness):
    cathetus_top = (thickness / 2.0) + radius
    cathetus_side = width / 2.0
    hypotenuse = math.sqrt(math.pow(cathetus_side, 2) + math.pow(cathetus_top, 2))
    return (cathetus_top, cathetus_side, hypotenuse)

def remove(thing):
    doc = App.activeDocument()
    doc.removeObject(thing.Label)

def clear():
    doc = App.activeDocument()
    for thing in doc.Objects:
        remove(thing)

def find(name):
    return App.activeDocument().getObject(name)

def rename(thing, name):
    thing.ObjectName = name
    thing.Label = name

def union(shapes):
    doc = App.activeDocument()
    thing = doc.addObject('Part::MultiFuse')
    thing.Shapes = shapes
    doc.recompute()
    return thing

def intersection(shapes):
    doc = App.activeDocument()
    thing = doc.addObject('Part::MultiCommon')
    thing.Shapes = shapes
    doc.recompute()
    return thing

def subtraction(thing1, thing2):
    doc = App.activeDocument()
    thing = doc.addObject('Part::Cut')
    thing.Base = thing1
    thing.Tool = thing2
    doc.recompute()
    return thing

def sphere(radius):
    doc = App.activeDocument()
    thing = doc.addObject('Part::Sphere')
    thing.Radius = radius
    doc.recompute()
    return thing

def cylinder(radius, height):
    doc = App.activeDocument()
    translation = App.Vector(0, height / 2.0, 0)
    rotation = App.Rotation(App.Vector(1, 0, 0), 90)
    center = App.Vector(0, 0, 0)
    thing = doc.addObject('Part::Cylinder')
    thing.Radius = radius
    thing.Height = height
    thing.Placement = App.Placement(translation, rotation, center)
    doc.recompute()
    return thing

def torus(radius, thickness, offset):
    doc = App.activeDocument()
    thickness = thickness / 2.0
    translation = App.Vector(0, offset, 0)
    rotation = App.Rotation(App.Vector(1, 0, 0), 90)
    center = App.Vector(0, 0, 0)
    thing = doc.addObject('Part::Torus')
    thing.Radius1 = radius
    thing.Radius2 = thickness
    thing.Placement = App.Placement(translation, rotation, center)
    doc.recompute()
    return thing

def hollowed(outer, inner):
    outer = sphere(outer)
    inner = sphere(inner)
    return subtraction(outer, inner)

def strutted(radius, thickness, clearance):
    radius = radius + (thickness / 2.0)
    hi = torus(radius, thickness,  clearance / 2.0)
    lo = torus(radius, thickness, -clearance / 2.0)
    return union([hi, lo])

def ringed(width, radius, thickness):
    (cathetus_top, cathetus_side, hypotenuse) = sides(width, radius, thickness)
    angle = math.acos(cathetus_side / hypotenuse)
    outer = hypotenuse + thickness / 2.0
    inner = hypotenuse - thickness / 2.0
    hollow = hollowed(outer, inner)
    trim = cylinder(2.0 * outer, width)
    return intersection([hollow, trim])

def texted(text, font, size, offset, scale, thickness):
    doc = App.activeDocument()
    translation = App.Vector(0, offset, -thickness / 2.0)
    rotation = App.Rotation(App.Vector(0, 0, 1), 0)
    center = App.Vector(0, 0, 0)
    flat = Draft.makeShapeString(String=text, FontFile=font, Size=size)
    flat.Placement = App.Placement(translation, rotation, center)
    extruded = doc.addObject('Part::Extrusion')
    extruded.Base = flat
    extruded.Dir = (0, 0, thickness)
    extruded.Solid = (True)
    scaled = Draft.clone(extruded)
    scaled.Scale = (scale, 1.00, 1.00)
    doc.recompute()
    remove(flat)
    remove(extruded)
    translation = App.Vector(-scaled.Shape.BoundBox.XLength / 2.0, 0, 0)
    scaled.Placement = App.Placement(translation, rotation, center)
    doc.recompute()
    return scaled

def wrapped(text, font, size, offset, scale, thickness, radius, angle):
    letters = []
    circumference = 2.0 * math.pi * radius
    factor = circumference / 360.0
    for letter in text:
        if ' ' == letter:
            delta = 2.0 * size
        else:
            letter = texted(letter, font, size, offset, scale, thickness)
            delta = 0.8 * letter.Shape.BoundBox.XLength / factor
            rotation = App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), angle))
            translation = App.Placement(App.Vector(0, 0, radius), App.Rotation())
            letter.Placement = rotation.multiply(translation.multiply(letter.Placement))
            letters.append(letter)
        angle += delta
    return letters

def export(thing, detail, stl):
    doc = App.activeDocument()
    mesh = doc.addObject('Mesh::Feature')
    mesh.Mesh = Mesh.Mesh(thing.Shape.tessellate(detail))
    Mesh.export([mesh], stl)

def go(engraving, radius, thickness, clearance, angle):
    path = os.path.dirname(sys.argv[1])
    pacifico = path + '/Pacifico.ttf'
    hearts = path + '/hearts.ttf'
    RING = 'Ring'
    App.newDocument(RING)
    App.setActiveDocument(RING)
    App.ActiveDocument = App.getDocument(RING)
    Gui.ActiveDocument = Gui.getDocument(RING)
    stamp = []
    stamp.extend(wrapped(engraving, pacifico, 6.2, -1.2, 1.7, 3 * thickness, radius, angle))
    stamp.extend(wrapped('&', pacifico, 3.9, -1.2, 1.7, 3 * thickness, radius, 180))
    stamp.extend(wrapped('l', hearts, 0.9, -1, 1.2, 3 * thickness, radius, +150))
    stamp.extend(wrapped('l', hearts, 0.9, -1, 1.2, 3 * thickness, radius, -150))
    stamp = union(stamp)
    blank = ringed(clearance, radius + 0.1, thickness - 0.2)
    engraving = intersection([blank, stamp])
    struts = strutted(radius, thickness, clearance)
    ring = union([struts, engraving])
    export(ring, 0.01, path + '/ring.stl')

go('love', 8.5, 1.0, 2.8, -35.0)
