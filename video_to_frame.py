import cv2
from utils import FolderUtils

result_path = "frames/"
video_path = "video/pupil01.avi"


def convert_video_into_frames():
    FolderUtils.create_if_not_exists(result_path)

    count = 1

    video = cv2.VideoCapture(video_path)
    success, image = video.read()
    while success:
        cv2.imwrite(result_path + "frame%d.jpg" % count, image)
        success, image = video.read()
        print("Read a new frame: ", count)
        count += 1


def main():
    convert_video_into_frames()


if __name__ == "__main__":
    main()
