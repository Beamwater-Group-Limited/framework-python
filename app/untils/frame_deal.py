# 获取frame的rgb数据
import cv2
import numpy as np

"""
将gstreamer获取的sample转化为rgb图像
"""
def get_rgb_frame(sample):

    # 将数据转换为 NumPy 数组
    buf = sample.get_buffer()
    data = buf.extract_dup(0, buf.get_size())
    height = sample.get_caps().get_structure(0).get_value("height")
    width = sample.get_caps().get_structure(0).get_value("width")
    format = sample.get_caps().get_structure(0).get_value("format")

    print("------------------------------------")
    print(f"图像格式为： {format}")
    print("------------------------------------")

    if format == "I420":  # YUV I420
        y_size = width * height
        u_size = (width // 2) * (height // 2)
        v_size = (width // 2) * (height // 2)

        y_plane = data[0:y_size]
        u_plane = data[y_size:y_size + u_size]
        v_plane = data[y_size + u_size:y_size + u_size + v_size]

        y = np.frombuffer(y_plane, np.uint8).reshape((height, width))
        u = np.frombuffer(u_plane, np.uint8).reshape((height // 2, width // 2))
        v = np.frombuffer(v_plane, np.uint8).reshape((height // 2, width // 2))

        # 上采样 U 和 V
        u_upsampled = cv2.resize(u, (width, height), interpolation=cv2.INTER_LINEAR)
        v_upsampled = cv2.resize(v, (width, height), interpolation=cv2.INTER_LINEAR)

        # 注意通道顺序：可能需要交换 U 和 V
        yuv = cv2.merge([y, v_upsampled, u_upsampled])  # 交换 U 和 V
        rgb_image = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB)

    elif format == "BGR":  # BGR 格式
        rgb_image = cv2.cvtColor(np.frombuffer(data, np.uint8).reshape((height, width, 3)),
                                 cv2.COLOR_BGR2RGB)

    elif format == "RGB":  # RGB 格式
        rgb_image = np.frombuffer(data, np.uint8).reshape((height, width, 3))

    elif format == "Y444":
        y_size = width * height
        u_size = width * height
        v_size = width * height

        # 提取 Y、U 和 V 分量
        y_plane = data[0:y_size]
        u_plane = data[y_size:y_size + u_size]
        v_plane = data[y_size + u_size:y_size + u_size + v_size]

        # 将 Y、U 和 V 数据转换为 NumPy 数组
        y = np.frombuffer(y_plane, np.uint8).reshape((height, width))
        u = np.frombuffer(u_plane, np.uint8).reshape((height, width))
        v = np.frombuffer(v_plane, np.uint8).reshape((height, width))

        # 将 YUV 转换为 RGB
        rgb_image = cv2.cvtColor(cv2.merge([y, u, v]), cv2.COLOR_YUV2RGB)

    else:
        rgb_image = None

    return rgb_image
