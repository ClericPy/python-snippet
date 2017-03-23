import sys

__doc__ = ''' Progress bar 
 进度条，暂时不打算show_time
- items: one iterator, used for loop and yield one by one.
- inline: while running in command line, all progress_bar show in one line without newline.
  Lose effect for print/sys.stderr/sys.stdout. 
- percent: show process by percent or counts/length.
- left: show number of not done.
- progress_bar_size: the length of progress_bar graph. Set less than screen width.

# examples:
import time
# run in command line, all progress_bar show in one line without newline.
for item in progress_bar(range(10),1,1,1,100):
    time.sleep(.5)
    do_sth = item # 
    '''


def progress_bar(items='', inline=False, percent=False, left=False,
                 progress_bar_size=30):
    '''Args:
- items: one iterator, used for loop and yield one by one.
- inline: while running in command line, all progress_bar show in one line without newline.
  Lose effect for print/sys.stderr/sys.stdout. 
- percent: show process by percent or counts/length.
- left: show number of not done.
- progress_bar_size: the length of progress_bar graph. Set less than screen width.

Read more from model __doc__.

   '''
    length = len(items)
    for x, item in enumerate(items, 1):
        process = ''
        if progress_bar_size:
            done = int(x*progress_bar_size/length)
            todo = progress_bar_size-done
            process = '%s%s' % ('■'*done, '□'*todo)
        msg = '%s %s%%' % (process, round(
            x*100/length, 2)) if percent else '%s %s / %s' % (process, x, length)
        left_msg = ' (-%s)' % (length-x) if left else ''
        msg = '%s%s%s' % (
            msg, left_msg, '\r') if inline else '%s\n' % msg
        sys.stderr.write(msg)
        yield item
    sys.stderr.write('\n\n')
