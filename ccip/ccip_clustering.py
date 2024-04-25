from PIL import Image
import os
from imgutils.metrics import ccip_clustering
import shutil
import cv2
# 设置原始图片文件夹路径
source_folder = r"E:\data\角色\ALL\zzz_all\1_all"
# 设置输出文件夹路径
output_folder = source_folder + r"\CCIPClassification"

# 确保原始文件夹和输出文件夹存在
if not os.path.exists(source_folder):
    os.makedirs(source_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

image_formats = ['.jpg', '.png', '.webp']
images = [os.path.join(source_folder, file) for file in os.listdir(source_folder) if any(file.endswith(format) for format in image_formats)]
# 使用完整路径执行聚类，并获取聚类结果
clusters = ccip_clustering(images,eps=4,min_samples=6) #修改min_samples，eps，CCIPClusterMethodTyping（可选'dbscan', 'dbscan_2', 'dbscan_free', 'optics', 'optics_best'，默认optics）可更改聚类灵敏度
print(clusters)
clustered_images = {image: cluster for image, cluster in zip(images, clusters)}

# 遍历字典，为每个类别在输出文件夹中创建文件夹并复制图片及其同名的txt文件
for image_path, cluster in clustered_images.items():
    # 为每个类别创建一个文件夹在输出路径
    cluster_folder = os.path.join(output_folder, str(cluster))
    if not os.path.exists(cluster_folder):
        os.makedirs(cluster_folder)

    # 设置图片的目标路径
    image_target_path = os.path.join(cluster_folder, os.path.basename(image_path))
    # 获取同名的txt文件路径
    txt_file_path = os.path.splitext(image_path)[0] + '.txt'
    # 设置txt文件的目标路径
    txt_target_path = os.path.join(cluster_folder, os.path.basename(txt_file_path))

    # 检查目标文件夹中是否已存在同名文件
    if not os.path.exists(image_target_path):
        # 复制图片到相应的类别文件夹
        shutil.copy(image_path, image_target_path)
    else:
        print(f'文件 {image_target_path} 已存在，无法复制 {image_path}')

    # 如果txt文件存在，则复制
    if os.path.exists(txt_file_path):
        if not os.path.exists(txt_target_path):
            shutil.copy(txt_file_path, txt_target_path)
        else:
            print(f'文件 {txt_target_path} 已存在，无法复制 {txt_file_path}')
