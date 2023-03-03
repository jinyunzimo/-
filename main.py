import os
from PIL import Image
def crop(image, crop_w, crop_h, offset_w, offset_h):
    x_max = image.size[0]
    y_max = image.size[1]
    mid_point_x = int(x_max / 2)
    mid_point_y = int(y_max / 2)
    right = mid_point_x + int(crop_w / 2) + offset_w
    left = mid_point_x - int(crop_w / 2) + offset_w
    down = mid_point_y + int(crop_h / 2) + offset_h
    up = mid_point_y - int(crop_h / 2) + offset_h
    BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN = left, up, right, down
    box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
    crop_img = image.crop(box)
    return crop_img

def reName(dirname,digit=3):
    count = 0
    for cur_file in os.listdir(dirname):
        count += 1
        oldDir = os.path.join(dirname, cur_file)
        filetype = os.path.splitext(cur_file)[1]  # 文件类型
        para="{:0>"+str(digit)+"d}"
        newDir = os.path.join(dirname, para.format(count) + filetype)  # 新文件
        os.rename(oldDir, newDir)
        #print(oldDir, newDir)

def divide(image, axis, ratio): #axis 0竖/1横
    x_max = image.size[0]
    y_max = image.size[1]
    if axis==0:
        BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN = 0, 0, x_max*ratio, y_max
        box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
        crop_img1 = image.crop(box).copy()
        BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN = x_max*ratio, 0, x_max, y_max
        box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
        crop_img2 = image.crop(box)
        return crop_img1,crop_img2
    if axis==1:
        BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN = 0, 0, x_max, y_max*ratio
        box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
        crop_img1 = image.crop(box).copy()
        BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN = 0, y_max*ratio, x_max, y_max
        box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
        crop_img2 = image.crop(box)
        return crop_img1, crop_img2


if __name__ == '__main__':
    dataset_dir = "E:\墨的文件\地政学boys\单行本第二卷"  # 图片路径
    output_dir = 'E:\墨的文件\地政学boys\结果'  # 输出路径
    size_w = 1330  # 裁剪图片宽
    size_h = 940  # 裁剪图片高
    offset_w = 0  # 向右偏移
    offset_h = 10  # 向下偏移

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    reName(dataset_dir) #批处理重命名
    # 获得需要转化的图片路径并生成目标路径
    image_filenames = [(os.path.join(dataset_dir, x),
                        os.path.join(output_dir, x.split('.')[0] + "_0." + x.split('.')[1]),
                        os.path.join(output_dir, x.split('.')[0] + "_1." + x.split('.')[1]))
                       for x in os.listdir(dataset_dir)]

    # 转化所有图片
    for path in image_filenames:
        image = Image.open(path[0])

        pic=crop(image, size_w, size_h, offset_w, offset_h)
        p1,p2=divide(pic,0,0.5)
        p1.save(path[1])
        p2.save(path[2])

    reName(output_dir)
