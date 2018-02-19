import numpy as np
import cv2

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import sys


# TODO when selecting points mode:
# only one image per time can be activated to receive mouse events, disable the other to avoid confussions!

# TODO resize QLabels to fixed size, then transform the pixels selected to the real coordinates of that images...



class MyMainWindow(QMainWindow):

    def getPos_1(self,event):
        x = event.pos().x()
        y = event.pos().y() 
        if self.label_activated == 1:
            pt = np.array([x,y])
            print(pt)
            self.pts_1 =  np.vstack((self.pts_1, pt)) if self.pts_1.size else pt
            self.label_activated = 2

            # TODO 
            # Paint

            # Disable 

            # Enable


    def getPos_2(self,event):
        x = event.pos().x()
        y = event.pos().y() 
        if self.label_activated == 2:
            pt = np.array([x,y])
            print(pt) 
            self.pts_2 =  np.vstack((self.pts_2, pt)) if self.pts_2.size else pt
            self.label_activated = 1


            # TODO 
            # Paint
            
            # Disable 

            # Enable


    def find_homography(self):
        print("Pts 1:")
        print(self.pts_1)

        print("Pts 2:")
        print(self.pts_2)

        # Compute homography

        # 0 - a regular method using all the points
        # CV_RANSAC - RANSAC-based robust method
        # CV_LMEDS - Least-Median robust method
        self.H = cv2.findHomography(self.pts_1, self.pts_2, cv2.RANSAC)

        print("Homography: ")
        print(self.H[0])
        # Save
        np.savetxt('pts_1.txt', self.pts_1) 
        np.savetxt('pts_2.txt', self.pts_2) 
        np.savetxt('H.txt', np.array(self.H[0]))

    def load_homography(self):

        self.pts_1 = np.loadtxt('pts_1.txt') 
        self.pts_2 = np.loadtxt('pts_2.txt') 
        self.H     = np.loadtxt('H.txt')

        self.cv_imwarp1 = cv2.warpPerspective(self.cv_im1, self.H, self.cv_im2.shape[:2])
        cv2.imwrite("data/imwarp_1.png", self.cv_imwarp1)

        print(self.pts_1)
        print(self.pts_2)
        print(self.H)

    def __init__(self, parent=None):
        # Private variables
        self.label_activated = 1

        self.H = []
        self.pts_1 = np.array([], dtype=float)
        self.pts_2 = np.array([], dtype=float)

        super(MyMainWindow, self).__init__(parent)
        self.win = QWidget(self)   
        self.hbox = QHBoxLayout()
        
        # Labels for images
        path_img1 = 'data/P003M.bmp'
        path_img2 = 'data/P003M.png'
        self.cv_im1 = cv2.imread(path_img1, 0)
        self.cv_im2 = cv2.imread(path_img2, 0)
        self.cv_imwarp1 = []

        self.l1 = QLabel()
        self.pix1 = QPixmap(path_img1)
        self.l1.setPixmap(self.pix1)
        self.l1.resize(self.pix1.size())
        self.l1.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.l1.mousePressEvent = self.getPos_1

        self.l2 = QLabel()
        self.pix2 = QPixmap(path_img2)
        self.l2.setPixmap(self.pix2)
        self.l2.resize(self.pix1.size())
        self.l2.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.l2.mousePressEvent = self.getPos_2

        # Disable Label





        self.but = QPushButton("Find Homography", self.win)
        self.but.clicked.connect(self.find_homography)


        self.but2 = QPushButton("Load Homography", self.win)
        self.but2.clicked.connect(self.load_homography)
        # Add GUI elements

        self.hbox.addWidget(self.l1)
        self.hbox.addWidget(self.l2)

        self.hbox.addWidget(self.but)
        self.hbox.addWidget(self.but2)

        """
        # Label to display the selected correspondences coords

        # QButton to run find_homography (and show the result)

        # QButton to save the correspondences and homography in .txt files

        """

        self.win.setLayout(self.hbox)

        self.win.setWindowTitle('Find homography')
        self.setCentralWidget(self.win)

        

if __name__ == "__main__":
    print("find_homography_manually img1_path img2_path  number_of_correspondences")
    print("\nCall example: find_homography_manually img1.png img2.png 5")
#    find_homography_manually()

    app = QApplication([])
    foo = MyMainWindow()
    foo.show()
    sys.exit(app.exec_())
