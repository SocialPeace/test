from xml.etree.ElementTree import parse


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


for pos in positions:
    keyframe = [x.findtext('keyframe') for x in pos][0]
    keypoint = [x.findall('keypoint') for x in pos][0]

    x = [x.findtext('x') for x in keypoint][0]
    y = [x.findtext('y') for x in keypoint][0]
