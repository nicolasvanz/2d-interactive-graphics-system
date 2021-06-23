# Instructions

## Interface manual

The main window interface is divided in two sections:
- the viewport, where the objects are displayed
- the commands frame, that is divided in:
  - The objects list box, in which are displayed all objects names in the scene
  - The "New Object" Button, where new objects can be added through the creation of the "New Object" window
  - The "in" and "out" buttons: responsable for zoom in and zoom out functionalities
  - The arrows: responsable for window navigation to right, left, up and down

The "New Object" window is responsable for the creation of a new object.
 - It must be specified a name and all the points coordinates that compose the object.
 - The coordinates must follow this format:
 (x1, y1), (x2, y2), ...
 - If the first coordinate is connected to the last coordinate, the "is a closed object" checkbox must be marked
 - "Ok" button confirms the object creation

## Development Environment
 - Operational System: Ubuntu 20.04
 - Python 3.8.5

## Running code
```
python main.py
```