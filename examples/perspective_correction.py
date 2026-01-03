#Perspective distortion Correction

#내가 클릭한 4개의 점(pts_src)-> 결과 이미지의 4개 모서리(pts_dst)가 되도록  비틀기(H)라고 컴퓨터에게 명령


import numpy as np
import cv2 as cv

#입력 받기
def mouse_event_handler(event, x, y, flags, param): 
    if event == cv.EVENT_LBUTTONDOWN:
        param.append((x, y))     #사용자가 이미지 위에서 마우스 왼쪽 버튼을 클릭할 때마다 클릭한 지점의 (x, y) 좌표를 리스트(param)에 저장
        #이 좌표들이 나중에 호모그래피를 계산할 때 원본 좌표인 pts_src가 

#목표 좌표 설정 (결과물 크기 결정)
if __name__ == '__main__':
    img_file = '../data/sunglok_card.jpg'
    card_size = (450, 250)  #우리가 결과물로 얻고 싶은 명함의 가로x세로 픽셀 크기
    offset = 10

    # Prepare the rectified points
    pts_dst = np.array([[0, 0], [card_size[0], 0], [0, card_size[1]], [card_size[0], card_size[1]]])
         #보정 후 이미지가 놓일 네 모서리의 좌표

    # Load an image
    img = cv.imread(img_file)
    assert img is not None, 'Cannot read the given image, ' + img_file

    # Get the matched points from mouse clicks
    pts_src = []
    wnd_name = 'Perspective Correction: Point Selection'
    cv.namedWindow(wnd_name)
    cv.setMouseCallback(wnd_name, mouse_event_handler, pts_src)
    
    #사용자 가이드
    while len(pts_src) < 4:   #사용자가 점을 4개 찍을 때까지 계속 화면 보여줌
        img_display = img.copy()
        cv.rectangle(img_display, (offset, offset), (offset + card_size[0], offset + card_size[1]), (0, 0, 255), 2)
        idx = min(len(pts_src), len(pts_dst))
        cv.circle(img_display, offset + pts_dst[idx], 5, (0, 255, 0), -1)   #사용자가 어디를 클릭해야 하는지 초록색 점으로 가이드를 표시
        cv.imshow(wnd_name, img_display)
        key = cv.waitKey(10)
        if key == 27: # ESC
            break

    #호모그래피 계산과 이미지 변환
    if len(pts_src) == 4:  # 1. 호모그래피 행렬 H 찾기
        # Calculate planar homography and rectify perspective distortion
        H, _ = cv.findHomography(np.array(pts_src), pts_dst)
        print(f'pts_src = {pts_src}')
        print(f'pts_dst = {pts_dst}')
        print(f'H = {H}')
        img_rectify = cv.warpPerspective(img, H, card_size)       # 2. 이미지 뒤틀기 (Warping)

        # Show the rectified image
        cv.imshow('Perspective Distortion Correction: Rectified Image', img_rectify)
        cv.waitKey(0)

    cv.destroyAllWindows()
