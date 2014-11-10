# -*- coding: utf-8 -*-
"""
@author: Callum Kift and Ralph Harti
"""

from eigenfaces import find_matching_image
from utils import merge_images


FACES     = None
THRESHOLD = 0.5


class PyFaces(object):
    """
    Detect if the face in `image` is similar to any face at `directory`,
    applies EigenFaces method with `threshold` as minum distance. Images
    on `directory` should be of the same size as `image`.
    """
    def __init__(self, image, directory, faces=FACES, threshold=THRESHOLD,
                 resize=True):
        self.image = image
        self.directory = directory
        self.faces = faces
        self.threshold = threshold
        self.resize = resize

    def match(self):
        """ Returns the match image and the distance between them, if any. """
        return find_matching_image(self.image, self.directory, self.threshold,
                                   self.faces, self.resize)

    def show(self):
        """ Shows the matching images joined """
        dist, match = self.match()
        if match is not None:
            merge_images([self.image, match]).show()
        return dist, match


def main(image, directory):


    pyfaces = PyFaces(image, directory, FACES, THRESHOLD, True)
    dist, match = pyfaces.match()


    return match, dist