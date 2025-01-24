It's just some exercises for practice.

First homework is:

1) Write a function calculate_circle_area(radius) that:

Takes the radius of a circle.
Returns the area of a circle.
Use this function in a program that asks the user for a radius and prints out the area.
2) Create a Rectangle class that represents a rectangle.

Class requirements:

Class attributes:
width — the width of the rectangle.
height — the height of the rectangle.
Class methods:
__init__(self, width, height) — a constructor that accepts the width and height of the rectangle.
area(self) — a method that returns the area of the rectangle.
perimeter(self) — a method that returns the perimeter of the rectangle.
is_square(self) — a method that returns True if the rectangle is a square (the width is equal to the height), otherwise False.
resize(self, new_width, new_height) — a method that changes the width and height of the rectangle.
Create an object of the Rectangle class and test all the methods.

Submit a file with the code or a link to a repository (GitHub, GitLab, etc.).

Complete each task number in a separate file.

Second homework is:

Task 1: Checking object types and attributes

1) Write a function analyze_object(obj) that takes any object and outputs: 

The type of the object.
A list of all methods and attributes of the object.
The type of each attribute.

2) Implement a call_function(obj, method_name, *args) function that takes an object, a method name as a string, 
and any arguments for this method. The function must call the corresponding object method and return the result.