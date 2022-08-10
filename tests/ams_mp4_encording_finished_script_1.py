import os
import datetime
from datetime import datetime, timedelta
import time


class FileManager:

    @staticmethod
    def mp4_profiling(mp4_path):
        mp4_path = mp4_path.split("/")
        app_name = mp4_path[5]
        file_name = mp4_path[-1]
        stream_dir = "/usr/local/antmedia/webapps/{}/streams".format(app_name)
        # print(f"App name: {app_name}")
        # print(f"File name: {file_name}")
        # print(f"stream dir: {stream_dir}")
        have_bit_rate = False
        if 'kbps' in file_name:
            have_bit_rate = True

        file_name = file_name.split(".")
        stream_id_create_on = file_name[0].split("-")
        stream_id = stream_id_create_on[0]
        created_on = "{}-{}-{}:{}:{}".format(stream_id_create_on[1], stream_id_create_on[2],
                                             stream_id_create_on[3],
                                             stream_id_create_on[4], stream_id_create_on[5])
        # print(f"stream id: {stream_id}")
        # print(f"created_on: {created_on}")
        #
        bit_rate = ''
        if have_bit_rate:
            bit_rate = file_name[1].split('_')[1]
        return stream_dir, stream_id, created_on, bit_rate

    @staticmethod
    def find_files_in_folder(stream_dir: str, stream_id: str, bit_rate: str):
        files = []
        _files = os.listdir(stream_dir)
        for file in _files:
            if '.ts' in file and stream_id in file:
                file_s = file.split('_')
                # file ts name like is: jTXNUFmxtfeW1655036890355_720p1500kbps0000.ts
                if len(file_s[1]) > 7 and len(bit_rate) > 0 and bit_rate in file:
                    print(file)
                    files.append(file)
                # file ts name like is: jTXNUFmxtfeW1655036890355_0000.ts
                if len(file_s[1]) == 7 and not len(bit_rate):
                    print(file)
                    files.append(file)
        return files


def mk_dir(folder):
    try:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    except Exception as e:
        print(e)
        return str(e)


def timestamp_to_str_time_format():
    """
    convert timestamp to time str: %Y-%m-%d_%H-%M-%S
    :return: str
    """
    ts = time.time()
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')


def main():
    paths = ["/usr/local/antmedia/webapps/testApp/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-41-40.834.mp4",
             "/usr/local/antmedia/webapps/testApp/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-41-41.723_720p1500kbps.mp4",
             "/usr/local/antmedia/webapps/testApp/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-41-41.724_1080p2000kbps.mp4"]
    for path in paths:
        stream_dir, stream_id, created_on, bit_rate = FileManager().mp4_profiling(path)
        session_dir = '/tmp/{}'.format(stream_id)
        error = mk_dir(session_dir)
        if error is None:
            files = FileManager().find_files_in_folder(stream_dir, stream_id, bit_rate)
            print(f'Bit rate: {bit_rate}')
            print(files)
            if len(files):
                for f in files:
                    try:
                        src = stream_dir + '/' + f
                        dst = session_dir + '/' + f
                        os.rename(src, dst)
                    except Exception as e:
                        print(e)
            try:

                dst = session_dir + '/' + path.split('/')[-1]
                print('mp4 moving: src {} -> dst: {}'.format(path, dst))
                os.rename(path, dst)
            except Exception as e:
                print(e)

            try:
                srcs = [stream_dir + '/' + stream_id + '_adaptive.m3u8', stream_dir + '/' + stream_id + '.m3u8']
                if bit_rate:
                    srcs = [stream_dir + '/' + stream_id + '_{}.m3u8'.format(bit_rate)]
                dst = session_dir
                for src in srcs:
                    os.rename(src, dst + '/' + src.split('/')[-1])
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()