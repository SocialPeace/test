import cv2
import os

from xml.etree.ElementTree import parse


# 트랙커 객체 생성자 함수


labels = parse('fight.xml')
root = labels.getroot()


labels = parse('fight.xml')
root = labels.getroot()


# 이상행동 나오는 부분 추출
event = root.findall('event')
starttimes = [x.findtext("starttime") for x in event]
durations = [x.findtext("duration") for x in event]


# fps 30 기준으로 프레임 개수가 1800개면 1분
standard_frame = 1800
start_minu = int(starttimes[0].split(':')[1])
start_sec = int(float(starttimes[0].split(':')[2]))

start_point = (start_minu + (start_sec//100))*standard_frame

dur_minu = int(durations[0].split(':')[1])
dur_sec = int(float(durations[0].split(':')[2]))

end_point = start_point + (dur_minu + (dur_sec//100))*standard_frame

objs = root.findall('object')
positions = [x.findall('position') for x in objs]
actions = [x.findall('action') for x in objs]


x1, x2, _y, w_, h = (9999, 0, 0, 0, 0)

for pos in positions:
    keyframe = [x.findtext('keyframe') for x in pos][0]
    keypoint = [x.findall('keypoint') for x in pos][0]

    x = int([x.findtext('x') for x in keypoint][0])
    y = int([x.findtext('y') for x in keypoint][0])
    x1 = min(x1, x)
    x2 = max(x2, x)

    _y = max(y, y)


w = x1 - x2
h = 100  # 일단 임의로

# 비디오에서 프레임 추출
img_last = None  # 이전 프레임을 저장할 변수
no = 0  # 이미지 장 수
save_dir = "./fight"  # 저장 디렉토리 이름
os.mkdir(save_dir)  # 디렉토리


print(start_point, end_point)
# # 동영상 파일로부터 입력받기 -- (*1)

frame_cnt = 0
cap = cv2.VideoCapture("fight.mp4")
cap.set(1, start_point)

while True:
    # 이미지 추출하기
    is_ok, frame = cap.read(start_point)
    frame = cv2.resize(frame, (640, 800))

    if not is_ok:
        break

    frame_cnt += 1

    print(frame_cnt)
    # 이상행동 끝나는 지점
    if frame_cnt > end_point-start_point:
        break

    # 이상행동 시작하는 지점
    # if frame_cnt >= start_point:
    roi = frame[0:_y, x:x+w]
    cv2.rectangle(roi, (0, 0), (h-1, w-1), (0, 255, 0))
    outfile = save_dir + "/" + str(no) + ".jpg"
    cv2.imwrite(outfile, frame)
    no += 1


cap.release()
print("ok")
