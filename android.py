# coding=utf-8
from __future__ import print_function
import os
import time

from midi.midifiles.midifiles import MidiFile
from midi.helpers import tuner
from config import HIGH_1, LOW_7

letter = {'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73, 'j': 74, 'k': 75, 'l': 76, 'm': 77,
          'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82, 's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90}
mobile = {
    'qwertyu': 0,
    'asdfghj': 1,
    'zxcvbnm': 2,
}
mapping = {'48': 'z', '50': 'x', '52': 'c', '53': 'v', '55': 'b', '57': 'n', '59': 'm', '60': 'a', '62': 's', '64': 'd',
           '65': 'f', '67': 'g', '69': 'h', '71': 'j', '72': 'q', '74': 'w', '76': 'e', '77': 'r', '79': 't', '81': 'y', '83': 'u'}

SLEEP_TIME = 0
RESULT = ""
POINTS = []


def dinput():
    a = {}
    count = 36
    while count <= 84:
        a[str(count)] = int(input())
        count += 1
    return a


def find(arr, time):
    result = []
    for i in arr:
        if i["time"] == time:
            result.append(i["note"])
    return result


def press(note):  # 48 83
    global SLEEP_TIME, RESULT, POINTS
    if SLEEP_TIME > 0:
        if POINTS:
            RESULT += f"mclick([{', '.join(POINTS)}]);\n"
            POINTS = []
        RESULT += f"sleep({SLEEP_TIME*1000}*PLAY_SPEED);\n"
        SLEEP_TIME = 0
    if note in mapping.keys():
        l = mapping[note]
        x, y = 0, 0
        for k in mobile:
            if l in k:
                x = mobile[k]
                y = k.find(l)
                break
        POINTS.append(f"[{x}, {y}]")
        # RESULT += f"mclick({x}, {y});\n"
    return


def unpress(note):  # 48 83
    if note in mapping.keys():
        pass
        # print("UP")
    return


def make_map():
    s = "zxcvbnmasdfghjqwertyu"
    for i, k in enumerate(mapping.keys()):
        mapping[k] = s[i]
    print(mapping)


song_list = os.listdir("./songs/")
for song_count in range(0, len(song_list)):
    print(str(song_count) + "：" + song_list[song_count])

midi_file = song_list[int(input("输入您要弹奏的midi编号并按回车："))][:-4]
print("您将要弹奏的是：" + midi_file)

try:
    midi_object = MidiFile("./songs/" + midi_file + ".mid")
except:
    print("文件损坏或不存在。")
    quit()
tick_accuracy = 0
print("尝试计算播放速度......")
try:
    flag = False
    for i in midi_object.tracks:
        for j in i:
            if j.dict()["type"] == "set_tempo":
                flag = True
                tempo = j.tempo
                break
        if flag:
            break
    bpm = 60000000 / tempo
    tick_accuracy = bpm / 20
    print("计算成功。")
except:
    tick_accuracy = int(input("计算失败，请检查文件是否完整，或者手动输入播放速度：（7）"))
type = ['note_on', 'note_off']
tracks = []
end_track = []
print("开始读取音轨。")
for i, track in enumerate(midi_object.tracks):
    print(f'track{i}')
    last_time = 0
    last_on = 0
    for msg in track:
        info = msg.dict()
        info['pertime'] = info['time']
        info['time'] += last_time
        last_time = info['time']
        if (info['type'] in type):
            del info['channel']
            del info['velocity']
            info['time'] = round(info['time'] / tick_accuracy)
            if info['type'] == 'note_on':
                del info['type']
                del info['pertime']
                last_on = info['time']
                tracks.append(info)
            else:
                del info['type']
                del info['pertime']
                last_on = info['time']
                end_track.append(info)
mmax = 0
for i in tracks:
    mmax = max(mmax, i['time'] + 1)
start = {}
print("开始转换乐谱...")
for i in range(mmax):
    start[str(i)] = find(tracks, i)
shift = None
while shift is None:
    auto_tune = input("是否自动变调？([n]/y)")
    if auto_tune == "y":
        shift, score = tuner.get_shift_best_match(tracks)
        print("变调: ", shift, " 按键比例: ", score)
    elif auto_tune == "n" or auto_tune == "":
        shift = 0
close_on_switch = False
auto_open = False

for i in range(mmax):
    if i != 0:
        for note in start[str(i - 1)]:
            unpress(str(note+shift))
    for note in start[str(i)]:
        press(str(note+shift))
    SLEEP_TIME += 0.025

TEMPLATE = f"""HIGH_1 = [{HIGH_1[0]}, {HIGH_1[1]}]; // 高音Do位置
LOW_7 = [{LOW_7[0]}, {LOW_7[1]}]; // 低音Ti位置
PLAY_SPEED = 1.0; // 可调整演奏速度，值越小速度越快

// ==== 下方代码为自动生成，一般不需要修改 ====
""" + """
y_delta = (LOW_7[0] - HIGH_1[0]) / 6;
x_delta = (LOW_7[1] - HIGH_1[1]) / 2;

X_POS = [];
Y_POS = [];
for (var i = 0; i < 3; i++) {
  X_POS.push(parseInt(HIGH_1[1] + x_delta * i));
}
for (var i = 0; i < 7; i++) {
  Y_POS.push(parseInt(HIGH_1[0] + y_delta * i));
}

function mclick(points) {
  g = [];
  for (var i = 0; i < points.length; i += 1) {
    xx = X_POS[points[i][0]];
    yy = Y_POS[points[i][1]];
    g.push([0, 1, [yy, xx], [yy, xx]]);
  }
  gestures.apply(this, g);
}

"""
RESULT = TEMPLATE + RESULT

with open(f"{midi_file}.js", 'w') as f:
    f.write(RESULT)
print(f"生成Auto.js脚本文件成功，保存在“{midi_file}.js”中")