# -*- coding: utf-8 -*-
'''
This module describes a class structure to represent physical objects in
3-dimensional space. The 3 foundational classes are Point, Vector, and Physical_Object

Point
---3D point in cartesian coordinates
Vector
---3D vector representing the difference between two points
Physical_Object
---represents any object with mass, position, velocity, and restitution

By leadbeltbuckle and burke-md
'''

from math import sqrt

class Point:
    # Represents a 3 dimensional point in cartesian coordinates
    def __init__(self, x, y, z, width = 1, height = 1, depth = 1):
        self.x = x
        self.y = y
        self.z = z
        self.xyz = (x, y, z)
        self.collision_zone_width = width
        self.collision_zone_height = height
        self.collision_zone_depth = depth

    def __str__(self):
        output = "({}, {}, {})".format(round(self.x, 3), round(self.y, 3), round(self.z,3))
        return output


    def calculateVectorFrom(self, point):
        # Takes a point, subtracts from itself, and produces a vector
        # For point P, given point O, finds vector OP
        outputVector = Vector(self.x - point.x,
                              self.y - point.y,
                              self.z - point.z)
        return outputVector

    def addVector(self, vector):
        # Expects a Vector object, returns a Point
        x = self.x + vector.i
        y = self.y + vector.j
        z = self.z + vector.k
        newPoint = Point(x, y, z)

        return newPoint

    def subtractVector(self, vector):
        # Expects a Vector object, returns a Point
        x = self.x - vector.i
        y = self.y - vector.j
        z = self.z - vector.k
        newPoint = Point(x, y, z)
        return newPoint

    def setPoint(self, x, y, z):
        # Expects 3 coordinates, resets the parameters of the Point object
        self.x = x
        self.y = y
        self.z = z
        self.xyz = (x, y, z)
        return True


class Vector:
    # Represents a 3 dimensional vector in cartesian space
    def __init__(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k
        self.ijk = (i, j, k)
        self.magnitude = sqrt(i**2 + j**2 + k**2)

    def __str__(self):
        output = "({}, {}, {})".format(round(self.i, 3), round(self.j, 3), round(self.k, 3))
        return output

    def subtractVector(self, vector):
        # Expects Vector object, returns Vector object
        outputVector = Vector(self.i - vector.i,
                              self.j - vector.j,
                              self.k - vector.k)
        return outputVector

    def addVector(self, vector):
        # Expects Vector object, returns Vector object
        outputVector = Vector(self.i + vector.i,
                              self.j + vector.j,
                              self.k + vector.k)
        return outputVector

    def linearTransform(self, matrix):
        # Expects a 3 x 3 matrix as a list vectors
        # Returns the resulting vector of a linear transformation
        #             defined by the transformation matrix
        value_list = []
        for x in range(3):
            i = matrix[x][0] * self.i
            j = matrix[x][1] * self.j
            k = matrix[x][2] * self.k
            value_list.append(i + j + k)

        outputVector = Vector(value_list[0],
                              value_list[1],
                              value_list[2])
        return outputVector

    def scale(self, vector):
        # Expects a Vector object, Returns a Vector object
        # Will also work with Int or Float --> applies equally to i, j, k
        try:
            i = self.i * vector.i
            j = self.j * vector.j
            k = self.k * vector.k
        except:
            i = self.i * vector
            j = self.j * vector
            k = self.k * vector

        outputVector = Vector(i, j, k)
        return outputVector

    def dotProduct(self, vector):
        # Expects Vector object, Returns Float
        product = (self.i * vector.i) + (self.j * vector.j) + (self.k * vector.k)
        return product

    def crossProduct(self, vector):
        # Expects Vector object, Returns Vector object
        i = (self.j * vector.k) - (self.k * vector.j)
        j = (self.k * vector.i) - (self.i * vector.k)
        k = (self.i * vector.j) - (self.j * vector.i)
        outputVector = Vector(i, j, k)
        return outputVector

    def scalarProjectionOnVector(self, vector):
        # Expects a Vector object, returns Float
        output_scalar = self.dotProduct(vector) / vector.magnitude
        return output_scalar

    def vectorProjectionOnVector(self, vector):
        # Expect a Vector object, and returns the resultant vector from the projection operation
        scalar = self.scalarProjectionOnVector(vector) / vector.magnitude
        scalar_vector = Vector(scalar, scalar, scalar)
        outputVector = vector.scale(scalar_vector)
        return outputVector

class Physical_Object:
    def __init__(self, mass, position, velocity, restitution = 1):
        # mass expects a single real number
        # position expects a Point object
        # velocity expects a Vector object
        # restitution expects a Float where 0 <= Float <= 1
        #          -- coefficient represents elasticity / bounciness
        #          -- useful in determining exit velocity after collisions
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.restitution = restitution

    def __str__(self):
        return("Mass: {}\nPosition: {}\nVelocity: {}".format(self.mass, self.position, self.velocity))

    def move(self):
        # Update the position based upon current velocity
        self.position = self.position.addVector(self.velocity)

    def updateVelocity(self, velocityChange):
        # Expects a 3 dimensional Vector
        # Updates Physical_Object to new velocity Vector
        self.velocity = self.velocity.addVector(velocityChange)

    def calculateAcceleration(self, forceVector):
        # Expects forceVector as a 3 dimensional Vector
        # Returns acceleration as a 3 dimensional Vector
        acceleration = forceVector.scale((1 / self.mass))
        return acceleration

'''A Basic Simulation of a moving ball'''
# TIMESTEP not correctly implemeted. Needs adjustment
TIMESTEP = 1
origin = Point(0, 0, 0)
gravity = Vector(0, -9.81 * TIMESTEP, 0)  # SI Units
ball_pos = Point(0, 50, 0)  # Ball starts at y = 50
ball_vel = Vector(30 * TIMESTEP, 10 * TIMESTEP, 0)  # Ball has initial forward/upward velocity

# Initialize the ball
ball = Physical_Object(5, ball_pos, ball_vel)

# Initialize the clock and throw the ball
counter = 0
while ball.position.y > 0:
    print(ball)
    ball.move()
    ball.updateVelocity(gravity)
    counter += 1
    print(counter)
