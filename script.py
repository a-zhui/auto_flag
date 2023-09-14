import base64
from io import BytesIO
import dlib
import cv2
import numpy as np
from PIL import Image


def base64_to_opencv(base64_string):
    # 从Base64字符串解码图像数据
    decoded_data = base64.b64decode(base64_string)

    # 将字节数据转换为numpy数组
    np_data = np.frombuffer(decoded_data, np.uint8)

    # 从numpy数组中解码图像
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    return img


def pillow_to_base64(image):
    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_image = base64.b64encode(byte_data).decode()
    return base64_image


def resize_image(img, target_size):
    # 获取原始图像的宽高
    height, width = img.shape[:2]
    # 根据目标尺寸计算缩放比例,只缩不放
    if height > target_size or width > target_size:
        if height > width:
            scale = target_size / height
        else:
            scale = target_size / width
        # 根据缩放比例计算新的尺寸
        new_height = int(height * scale)
        new_width = int(width * scale)
        # 使用OpenCV的resize函数进行缩放
        img = cv2.resize(img, (new_width, new_height))
    return img


def get_points(image):
    # 读取输入数据，预处理
    # 图像灰度处理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 这里先识别人脸，然后下面在识别到人脸的基础上进行人脸关键点的分别展示
    rects = detector(gray, 2)  # 第一个参数是传入的图像，第二个参数 2 代表的是图片上采样倍数，值越大，最终识别得到的结果越好，但耗时会越长

    point_list = []
    # 遍历检测到的框
    for (i, rect) in enumerate(rects):
        result = predictor(gray, rect)
        result = result.parts()
        points = [[p.x, p.y] for p in result]  # 上面的result还需进行结果提取

        flag_x = points[17][0]
        flag_y = points[29][1]
        flag_w = points[39][0] - points[36][0]
        point_list.append((flag_x, flag_y, flag_w))

    return point_list


def blend_images(background, point_info, alpha):
    flag_img = Image.open('images/flag.png')
    # 打开背景图片和叠加图片
    for j in point_info:
        flag_img.thumbnail((j[2], j[2]))
        flag_img.putalpha(int(255 * alpha))
        # 将叠加图片与背景图片进行叠加混合
        background.paste(flag_img, (j[0], j[1]), flag_img)
    return background


def pillow_to_opencv(pillow_img):
    # 将Pillow对象转换为NumPy数组
    image_np = np.array(pillow_img)
    # 将RGB图像转换为BGR图像
    image_opencv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    return image_opencv


def opencv_to_pillow(opencv_img):
    # 将BGR图像转换为RGB图像
    image_rgb = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2RGB)
    # 将NumPy数组转换为Pillow对象
    image_pillow = Image.fromarray(image_rgb)
    return image_pillow


# 加载人脸检测与关键点定位
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# blend_images(background_path=face_path, overlay_path=flag_path, point_info=point_list, alpha=0.2)

if __name__ == '__main__':
    img = cv2.imread('images/face1.png')
    # 获取放置国旗的点位
    ret = get_points(img)
    # 将国旗贴上取
    blend_images(opencv_to_pillow(img), ret, 0.5).show()
