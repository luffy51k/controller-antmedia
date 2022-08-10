import os
import shutil
import datetime
from datetime import datetime, timedelta
import time


def timestamp_to_str_time_format():
    """
    convert timestamp to time str: %Y-%m-%d_%H-%M-%S
    :return: str
    """
    ts = time.time()
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')


def filter_params_from_mp4_path(mp4_path):
    mp4_path = mp4_path.split("/")
    app_name = mp4_path[5]
    file_name = mp4_path[-1]

    print(f"App name: {app_name}")
    print(f"File name: {file_name}")

    file_name = file_name.split(".")
    stream_id_create_on = file_name[0].split("-")
    stream_id = stream_id_create_on[0]
    created_on = "{}-{}-{}:{}:{}".format(stream_id_create_on[1], stream_id_create_on[2],
                                         stream_id_create_on[3].replace("_", " "),
                                         stream_id_create_on[4], stream_id_create_on[5])
    print(f"stream id: {stream_id}")
    print(f"created_on: {created_on}")

    stream_dir = "/usr/local/antmedia/webapps/{}/streams".format(app_name)
    print(f"stream dir: {stream_dir}")

    have_bit_rate = False
    if 'kbps' in file_name:
        have_bit_rate = True


mp4_path = "/usr/local/antmedia/webapps/testApp/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-41-41.724_1080p2000kbps.mp4"


mp4_path = mp4_path.split("/")
app_name = mp4_path[5]
file_name = mp4_path[-1]
session_dir = '/tmp/' + file_name.replace('.mp4', '')
try:
    os.mkdir(session_dir)
except Exception as e:
    print(e)

print(f"App name: {app_name}")
print(f"File name: {file_name}")
stream_dir = "/usr/local/antmedia/webapps/{}/streams".format(app_name)
print(f"stream dir: {stream_dir}")
have_bit_rate = False
if 'kbps' in file_name:
    have_bit_rate = True

file_name = file_name.split(".")
stream_id_create_on = file_name[0].split("-")
stream_id = stream_id_create_on[0]
created_on = "{}-{}-{}:{}:{}".format(stream_id_create_on[1], stream_id_create_on[2],
                                     stream_id_create_on[3],
                                     stream_id_create_on[4], stream_id_create_on[5])
print(f"stream id: {stream_id}")
print(f"created_on: {created_on}")

print('- Bit rate: ')
bit_rate = ''
if have_bit_rate:
    bit_rate = file_name[1].split('_')[1]
    print(f'bit rate: {bit_rate}')


def find_ts_prefix(stream_id, bit_rate):
    print('- Ts file prefix: ')
    ts_prefix = stream_id + '_'
    if len(bit_rate):
        ts_prefix = stream_id + '_' + bit_rate


def move_file(stream_dir, session_dir, ts_prefix):
    print('- Moving files:')
    files = os.listdir(stream_dir)
    for f in files:
        print(f)
        if ts_prefix in f:
            try:
                src = stream_dir + '/' + f
                dst = session_dir + '/' + f
                os.rename(src, dst)
            except Exception as e:
                print(e)


