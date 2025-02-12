import os, shutil
import subprocess
from capo_tools.datasets.CAVE.tools import download_CAVE

def du(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du','-hs', path]).split()[0].decode('utf-8')

# TODO: review with Ivan
# def test_download_CAVE():
#     path_to_save = './DATA'
#     if os.path.exists(path_to_save):
#         shutil.rmtree(path_to_save)
#     if os.path.exists('temp'):
#         shutil.rmtree('temp')
#     download_CAVE(path_to_save=path_to_save)
#     size = du(path_to_save)
#     assert size == '2.0G'
#     shutil.rmtree(path_to_save)