import threading


class Thread:
    @staticmethod
    def make_thread(function, *args, **kwargs):
        child_thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        child_thread.daemon = True
        child_thread.start()
