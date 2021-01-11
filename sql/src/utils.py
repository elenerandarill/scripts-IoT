from datetime import datetime


def log(*args):
    # print("got log() ", args)
    now = datetime.now()
    now_formatted = now.strftime("%H:%M:%S")
    args2 = [now_formatted, " "]
    args2.extend(args)
    print "".join(map(str, args2))
