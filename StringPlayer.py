from tkinter import Tk, filedialog
from PIL import Image
import cv2
import os
import sys

# 获取 ASCII 字符映射表
ASCII_CHARS = list(" .,-~:;=!*#$@")
# ASCII 字符映射表长度
CHAR_LENGTH = len(ASCII_CHARS)
UNIT = (256.0 + 1) / CHAR_LENGTH
GRAY_TO_CHAR = [ASCII_CHARS[int(gray / UNIT)] for gray in range(256)]


def get_char(r, g, b, alpha=256):
    """根据RGB值获取对应的ASCII字符"""
    if alpha == 0:
        return ' '
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    return GRAY_TO_CHAR[gray]


def image_to_ascii(frame):
    """将视频帧转换为ASCII字符"""
    # 获取视频帧的尺寸
    term_width, term_height = os.get_terminal_size()
    term_width = min(term_width, 200)  # 限制最大宽度
    term_height = min(term_height - 1, 60)  # 预留一行空间

    # 将视频帧缩放到终端的尺寸
    im = Image.fromarray(frame)
    im = im.resize((term_width, term_height), Image.NEAREST)

    txt = ""
    for i in range(term_height):
        for j in range(term_width):
            txt += get_char(*im.getpixel((j, i)))
        txt += '\n'
    return txt


def get_video_path():
    """弹出文件选择对话框获取视频路径"""
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="快点选择视频文件哈哈哈😁",
        filetypes=[("视频文件👉", "*.mp4;*.avi;*.mov;*.mkv")]
    )


def get_video_info(video_path):
    """使用OpenCV获取视频信息"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return fps, total_frames


def play_video_as_ascii(video_path):
    """从视频流中提取每一帧并显示为ASCII字符"""
    cap = cv2.VideoCapture(video_path)

    # 获取视频信息
    fps, total_frames = get_video_info(video_path)
    delay = 1 / fps if fps > 0 else 1 / 60  # 默认30fps

    frame_number = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # 视频播放结束

            ascii_art = image_to_ascii(frame)

            # 清除屏幕，移动光标到左上角
            sys.stdout.write("\033[H")
            sys.stdout.write(ascii_art)
            sys.stdout.flush()

            frame_number += 1
            # time.sleep(delay)  # 控制帧率

    except KeyboardInterrupt:
        print("\n用户中断播放。")
    finally:
        cap.release()
        print("\n视频播放结束。")


if __name__ == '__main__':
    video_path = get_video_path()
    if not video_path:
        print("未选择视频文件，程序退出。")
        exit()

    play_video_as_ascii(video_path)
