
import time

def printExecutionTime(startTimeSec):
    startTimeMilli = startTimeSec * 1000
    endTimeMilli = time.time() * 1000

    diff = endTimeMilli - startTimeMilli

    hours = int(diff / 3600000)
    diff -= (hours * 3600000)

    minutes = int(diff / 60000)
    diff -= (minutes * 60000)

    seconds = int(diff / 1000)
    diff -= (seconds * 1000)

    milliseconds = round(diff, 4)

    result = []

    if hours > 0:
        result.append(str(hours) + 'h')
    if minutes > 0:
        result.append(str(minutes) + 'm')
    if seconds > 0:
        result.append(str(seconds) + 's')
    if milliseconds > 0:
        result.append(str(milliseconds) + 'ms')

    print('Total execution time: ' + ' '.join(result))
