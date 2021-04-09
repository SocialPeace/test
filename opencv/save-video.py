import cv2

cap = cv2.VideoCapture(0)
img_last = None  # 이전 프레임을 저장해둘 변수 --- (*1)
green = (0, 255, 0)

while True:
    # 이미지 추출하기
    _, frame = cap.read()
    frame = cv2.resize(frame, (700, 500))
    # 흑백 이미지로 변환하기 --- (*2)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 0)
    img_b = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
    # 차이 확인하기
    if img_last is None:
        img_last = img_b
        continue
    frame_diff = cv2.absdiff(img_last, img_b)  # --- (*3)
    cnts = cv2.findContours(frame_diff,
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[0]  # opencv 4부터 변경사항 이전 버전에서는 [1]

    # 차이가 있는 부분 출력하기 --- (*4)
    for pt in cnts:
        x, y, w, h = cv2.boundingRect(pt)
        if w < 30:
            continue  # 작은 변경은 무시하기
        cv2.rectangle(frame, (x, y), (x+w, y+h), green, 2)
        # 프레임을 변수에 저장해두기
        img_last = img_b
        # 화면에 출력하기
        cv2.imshow("Diff Camera", frame)
        cv2.imshow("diff data", frame_diff)
    if cv2.waitKey(1) == 13 or cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()


'''
(*1) img_last 초기화 
여기에 바로 앞 이미지가 기록됨 

(*2) 
비교하기 쉽게 하기 위해서 흑백 이미지로 변환
그레이스케일로 변환하고 블러 처리를 한 후 이진화

(*3)
cvs.absdiff()
두 이미지의 차이를 확인 

(*4)
cvs.findContours()
윤곽을 추출한 결과에 녹색 사각형을 렌더링 

(*5)
img_last에 이미지 기록 
'''
