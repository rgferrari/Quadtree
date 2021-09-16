import random
import matplotlib.pyplot as plt

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (point.x <= self.x + self.w and
                point.x >= self.x - self.w and
                point.y <= self.y + self.h and
                point.y >= self.y - self.h)

class QuadTree():
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.is_divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        nw = Rectangle(x - w/2, y - w/2, w/2, h/2)
        self.northwest = QuadTree(nw, self.capacity)
        ne = Rectangle(x + w/2, y - h/2, w/2, h/2)
        self.northeast = QuadTree(ne, self.capacity)
        sw = Rectangle(x - w/2, y + w/2, w/2, h/2)
        self.southwest = QuadTree(sw, self.capacity)
        se = Rectangle(x + w/2, y + w/2, w/2, h/2)
        self.southeast = QuadTree(se, self.capacity)

        self.is_divided = True


    def insert(self, point):
        if(not self.boundary.contains(point)):
            return False

        if(len(self.points) < self.capacity):
            self.points.append(point)
            return True

        else:
            if(not self.is_divided):
                self.subdivide()
                self.is_divided = True

            if (self.northwest.insert(point)):
                return True
            elif (self.northeast.insert(point)):
                return True
            elif (self.southwest.insert(point)):
                return True
            elif (self.southeast.insert(point)):
                return True

    def draw(self):
        x = [self.boundary.x - self.boundary.w, self.boundary.x + self.boundary.w] 
        y = [self.boundary.y - self.boundary.h, self.boundary.y + self.boundary.h]

        plt.plot(x, [0,0], 'k-') 
        plt.plot(x, [self.boundary.y + self.boundary.h, self.boundary.y + self.boundary.h], 'k-') 
        plt.plot([0,0], y, 'k-')
        plt.plot([self.boundary.x + self.boundary.w, self.boundary.x + self.boundary.w], y, 'k-')

        for p in self.points:
            plt.plot(p.x, p.y, 'k.')

        if(self.is_divided):
            self.northwest.draw()
            self.northeast.draw()
            self.southwest.draw()
            self.southeast.draw() 

def main():
    boundary = Rectangle(200,200,200,200)
    quadtree = QuadTree(boundary, 4)

    width = 400
    height = 400

    for _ in range(500):
        p = Point(random.randrange(width), random.randrange(height))
        quadtree.insert(p)

    quadtree.draw()

    plt.show()

main()   