import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api


WIDTH = 800
HEIGHT = 360
HEIGHT_OFFSET = 270
WIDTH_SMALL = int(WIDTH/10)
HEIGHT_SMALL = int(HEIGHT/10)


def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def edit_img(image):
    image =  cv2.Canny(image, threshold1 = 200, threshold2=300)
    frameResize=np.array([[250,360],[330,120],[470,120],[550,360]], np.int32)
    cv2.fillPoly(image, [frameResize], 0)
    image = cv2.GaussianBlur(image,(5,5),0)
    lines = cv2.HoughLinesP(image, 0.9, np.pi/180, 80, 20, 10)
    if lines!=None:
        for line in lines:
            coords = line[0]
            cv2.line(image, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 5)

    image = cv2.resize(image, (WIDTH_SMALL, HEIGHT_SMALL))
    image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
    return image