import requests
import time
import numpy
import sys
from matplotlib import pyplot as plt


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()


file = '512MB'
url = 'http://ipv4.download.thinkbroadband.com:8080/{}.zip'.format(file)
response = requests.head(url)
content_len = response.headers['content-length']
r = requests.get(url, stream=True)

file = open(url.split('/')[-1], 'wb')

i = 0
loopstart = 0
per_sec_avg = 0
should_be_one = 1
avg_speeds = []
window = 2048
for chunk in r.iter_content(chunk_size=1024):
    if loopstart is 0:
        loopstart = time.perf_counter()
    if i % window == 0 and i is not 0:
        kbtime = time.perf_counter() - loopstart
        kbtime /= window
        per_sec_avg = 1 * 1 / kbtime
        per_sec_avg = per_sec_avg / 1024
        avg_speeds.append(per_sec_avg)
        loopstart = time.perf_counter()
    per_sec_s = str(per_sec_avg)[:4]
    avg_s = 1 if len(avg_speeds) == 0 else numpy.average(avg_speeds)
    s = '{} MB/s current, avg. speed: {}'.format(per_sec_s, avg_s)
    progress(i, int(content_len)/1024, status=s)
    if chunk:
        file.write(chunk)

    i += 1

file_size = i / 1024
print('\nFile size:', file_size, 'MB')
plt.plot(avg_speeds)
plt.show()
