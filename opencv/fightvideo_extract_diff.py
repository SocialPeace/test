import cv2
import os

from xml.etree.ElementTree import parse

################# xml parsing #################
labels = parse('fight.xml')  # xml 넣는 곳
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

end_point = (dur_minu + (dur_sec//100))*standard_frame


objs = root.findall('object')
positions = [x.findall('position') for x in objs]


actions = []
for obj in objs:
    actions += obj.findall('action')


# 각 액션 시작, 끝 프레임 추출
starts = []
ends = []
abnoraml_frame_total = 0
action_frames = [x.findall('frame') for x in actions]


print("=============== actions frames ============")
print("start end")
print("===========================================")
for frames in action_frames:
    for frame in frames:
        start = int(frame.findtext('start'))
        end = int(frame.findtext('end'))
        abnoraml_frame_total += end-start
        print(start, end)
        starts.append(start)
        ends.append(end)


print(abnoraml_frame_total)


print('start_frame : %d , end_frame:  %d ' % (start_point, end_point))

##################### video parsing ######################

# 비디오에서 프레임 추출
img_last = None  # 이전 프레임을 저장할 변수
no = 0  # 이미지 장 수
save_dir = "./fight"  # 저장 디렉토리 이름
os.mkdir(save_dir)  # 디렉토리

frame_cnt = 0
cap = cv2.VideoCapture("fight.mp4")  # mp4 파일 넣는 곳


for start, end in zip(starts, ends):
    diff = end-start
    print(diff)
    frame_cnt = 0
    while True:
        cap.set(1, start)  # 이상행동 시작 구간으로 프레임 세팅
        # 이미지 추출하기
        is_ok, frame = cap.read()  # 프레임 읽기
        frame = cv2.resize(frame, (640, 800))  # 프레임 리사이징

        if not is_ok:
            break

        frame_cnt += 1
        print(start)

        # 이상행동 끝나는 지점
        if start >= end:
            print("frame_end")
            break

        # 프레임 이미지로 저장
        # 액션이 나오는 프레임만 자르기
        outfile = save_dir + "/" + str(no) + ".jpg"
        cv2.imwrite(outfile, frame)
        no += 1
        total = no
        start += diff // 2


print("===============================")
print('total : %d' % (no))
print('actions : %d' % (len(actions)))
print("===============================")
