import logging
import cv2
import gradio as gr
from api import app_api
from script import get_points, blend_images, opencv_to_pillow, resize_image

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=20)


def ex(image, slider, checkbox):
    logging.info('-----------请求分割线-----------')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换一下图片格式
    if checkbox:
        image = resize_image(image, 1024)  # 限制图片宽高，超过1024压缩,否则在获取人脸关键点的时耗时
        logging.info('压缩图片')
    points = get_points(image)
    logging.info('获取国旗放置位置')
    output = blend_images(opencv_to_pillow(image), points, slider)
    logging.info('国旗人脸叠加')
    return output


ui = gr.Interface(fn=ex,
                  title='人脸自动贴国旗',
                  inputs=[gr.Image(label='图片'),
                          gr.Slider(minimum=0, maximum=1, value=0.7, label='国旗透明度'),
                          gr.Checkbox(value=True, label='是否压缩图片,若不勾选,如果图片过大,在获取人脸关键点时可能耗时'),
                          ],
                  outputs=gr.Image(label='结果'),
                  allow_flagging='never',
                  examples=[['images/face1.png'], ['images/face2.png'], ['images/face3.png']]
                  )

ui.queue()
ui.show_api = False
# interface.launch(inbrowser=True, server_name='0.0.0.0', server_port=7860)

# 将api与ui界面挂载,path为ui界面的访问路径
app = gr.mount_gradio_app(app_api, ui, path='/')
