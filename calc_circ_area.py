from math import pi

def calculate_circle_area(radius):
    # returns the circle area with a given radius
    area = pi * radius ** 2
    return area

def is_number(value):
    # returns true if the entered value is number
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == "__main__": # this is a protection against execution in case of import of functions
    # request radius from user
    r = input('Enter the radius of circle (positive number)): ')
    if is_number(r):
        r = float(r)
        if r > 0:
            print('The area of the circle is: ', calculate_circle_area(r))
        else:
            print('Radius of the circle must be a positive number')
    else:
        print('Radius of the circle must be a positive number')

