# 将图片裁剪出感兴趣区，以便之后给YOLO训练能得到32倍数的像素点
import cv2

CAM_INDEX = 1 # 摄像头索引，0表示默认摄像头

cap_width = 1920 # 摄像头分辨率宽度
cap_height = 1080 # 摄像头分辨率高度

roi_width = cap_height
roi_height = cap_height

def draw_table(img, pt1, pt2, rows, cols, color, thickness):
  """
  绘制带均匀表格的矩形
  :param img: 要绘制的图像
  :param pt1: 左上角 (x1, y1)
  :param pt2: 右下角 (x2, y2)
  :param rows: 表格行数
  :param cols: 表格列数
  :param color: BGR 颜色
  :param thickness: 线条粗细
  """
  cv2.rectangle(img, pt1, pt2, color, thickness) # 先画外框矩形
  x1, y1 = pt1 # 取出矩形的左上角坐标
  x2, y2 = pt2 # 取出矩形的右下角坐标

  cell_w = (x2 - x1) / cols # 计算每一格的宽度
  cell_h = (y2 - y1) / rows # 计算每一格的高度

  for i in range(1, cols): # 遍历每一列
    x = int(x1 + i*cell_w) # 计算当前列的x坐标
    cv2.line(img, (x,y1), (x,y2), color, thickness) # 画竖线

  for i in range(1, rows): # 遍历每一行
    y = int(y1 + i*cell_h) # 计算当前行的y坐标
    cv2.line(img, (x1,y), (x2,y), color, thickness) # 画横线



def main():
  cam = cv2.VideoCapture(CAM_INDEX) # 创建摄像头捕获对象，0表示默认摄像头
  if not cam.isOpened(): # 如果摄像头未成功打开
    print("无法打开摄像头") # 打印错误信息
    return # 退出程序

  cam.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width) # 设置摄像头分辨率宽度
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height) # 设置摄像头分辨率高度
  
#   cv2.namedWindow('cam_origin') # 创建名为"cam"的窗口，显示原始图像
  cv2.namedWindow('cam_roi') # 创建名为"cam_roi"的窗口，显示裁剪后的图像
  print("按ESC键退出程序")

  while True:
    ret, frame_origin = cam.read() # 读取摄像头帧
    if not ret: # 如果帧读取失败
      print("无法读取摄像头帧")  # 打印错误信息
      break # 退出循环
    
    frame_origin_height, frame_origin_width = frame_origin.shape[0:2] # 获取帧的宽度和高度
    x = (frame_origin_width - roi_width) // 2 # 计算裁剪区域的左上角x坐标
    y = (frame_origin_height - roi_height) // 2 # 计算裁剪区域的左上角y坐标
    frame_roi = frame_origin[y:y+roi_height, x:x+roi_width] # 裁剪图像
    draw_table(frame_roi, 
               pt1=(20,10),
               pt2=(1050,1070),
               rows=9, cols=8,
               color=(0,0,255),
               thickness=2 )

    # cv2.imshow('cam_origin', frame_origin) # 在窗口中显示帧
    cv2.imshow('cam_roi', frame_roi) # 在窗口中显示裁剪后的图像

    if cv2.waitKey(1) & 0xFF == 27: # 如果按下ESC键
      break # 退出循环
    
  cam.release() # 释放摄像头
  print("相机资源已释放")
  cv2.destroyAllWindows() # 关闭所有窗口
  print("所有窗口已关闭")



if __name__ == "__main__":
  main()
