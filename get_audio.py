import youtube_dl
import os
import subprocess


TRESHOLD = 52428800


class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self,msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done. Converting...')


def cut_audio(path: str) -> list:
    '''
    Cuts audio file into pieces each with the size of
    TRESHOLD, except for last one which is combined with the
    rest of track. Then this chunk is cutted in two pieces:
    one with size of TRESHOLD/2 and one to the end of track
    If size of file is less than 2*TRESHOLD then

    in: path to the file to be cutted like 'track.mp3'
    out: list of files that represent input file if are
    combined like 'track_1.mp3, track_2.mp3'
    '''
    files_list = []
    path_list = path.split('.')
    name = ''.join(path_list[:-1])
    fileformat = '.' + path_list[-1]
    size = os.stat(path).st_size
    duration = float(subprocess.check_output([
        'ffprobe', '-loglevel', 'quiet', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', path
    ]).decode('utf-8'))
    whole_count = size // TRESHOLD
    time = int(duration / size * TRESHOLD)
    time_str = str(time)
    pause = 0
    for i in range(0, whole_count - 1):
        out = name + '_' + str(i + 1) + fileformat
        start = 0 + time * i
        start_str = str(start)
        subprocess.Popen([
            'ffmpeg', '-i', path, '-ss', start_str,
            '-t', time_str, out
        ]).wait()
        files_list.append(out)
        pause += time
    out = name + '_' + str(whole_count) + fileformat
    half_time = time // 2
    half_time_str = str(half_time)
    pause_str = str(pause)
    subprocess.Popen([
        'ffmpeg', '-i', path, '-ss', pause_str,
        '-t', half_time_str, out
    ]).wait()
    files_list.append(out)
    pause += half_time
    pause_str = str(pause)
    out = name + '_' + str(whole_count + 1) + fileformat
    subprocess.Popen([
        'ffmpeg', '-i', path, '-ss', pause_str, out
    ]).wait()
    files_list.append(out)
    return files_list


def get_audio (url: str) -> list:
    ydl_opts = {
            'format' : '251',
            'outtmpl' :  '/home/nick/Downloads/tg_dump/%(title)s_%(id)s.%(format)s',
            'postprocessors' : [{
                'key' : 'FFmpegExtractAudio',
                'preferredcodec' : 'opus',
                'preferredquality' : '192',
                }],
            'logger' : MyLogger(),
            'progress_hooks' : [my_hook],
            }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #ydl.cache.remove()
        meta = ydl.extract_info(url, download=False)
        ydl.download([url])

    filename = ''
    print("id    : " + meta['id'])
    for file in os.listdir("/home/nick/Downloads/tg_dump/"):
        if meta['id'] in file:
            filename = file

    file_path = "/home/nick/Downloads/tg_dump/" + filename
    print(os.stat(file_path).st_size)
    print(filename)
    if os.stat(file_path).st_size >= 52428800:
        file_path = cut_audio(file_path)
    else:
        file_path = [file_path]

    return file_path
