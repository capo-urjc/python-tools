import imageio
import numpy as np
import os
import shutil
import sys
from tqdm import tqdm
import wget
import zipfile


def generate_dataset(path_to_save: str, dataset_path: str):

    folders: list = os.listdir(dataset_path)
    folders = sorted(folders)

    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

        os.makedirs(path_to_save + "/train")
        os.makedirs(path_to_save + "/valid")
        os.makedirs(path_to_save + "/test")

    train_idxs: list = [1, 2, 5, 6, 7, 8, 9, 10, 11, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 30, 31]
    valid_idxs: list = [3, 4, 14, 26, 27]
    test_idxs: list = [12, 18, 28, 29, 32]

    for j in tqdm(range(len(folders)), desc="Generating"):

        if j in train_idxs:
            subset: str = "train"
        elif j in valid_idxs:
            subset: str = "valid"
        else:
            subset = "test"

        folder_path: str = dataset_path + '/' + folders[j] + '/' + folders[j] + '/'
        files: list = os.listdir(folder_path)
        files = sorted(files)

        images: list = [png_file for png_file in files if png_file.endswith(".png")]

        hs_image: np.ndarray = np.zeros((512, 512, 31))

        for i in range(31):
            if folders[j] != "watercolors_ms":
                hs_image[..., i] = imageio.v3.imread(folder_path + images[i]).astype(np.float32)

            else:
                hs_image[..., i] = imageio.v3.imread(folder_path + images[i])[..., 0].astype(np.float32)

        np.save(path_to_save + '/' + subset + '/' + folders[j] + ".npy", hs_image)


def download_CAVE(path_to_save: str):

    if not os.path.exists("temp"):
        os.makedirs("temp")

    # Download dataset
    url: str = "https://www.cs.columbia.edu/CAVE/databases/multispectral/zip/complete_ms_data.zip"

    def bar_custom(current, total, width=80):
        progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    wget.download(url, "temp", bar=bar_custom)

    with zipfile.ZipFile("temp" + "/complete_ms_data.zip", 'r') as zip_ref:
        zip_ref.extractall("temp")

    os.remove("temp" + "/complete_ms_data.zip")

    generate_dataset(path_to_save, "temp")

    shutil.rmtree("temp")