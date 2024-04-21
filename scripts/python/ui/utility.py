def get_human_readable(size):
    suffixes = ["bytes", "KB", "MB", "GB", "TB", "PB"]
    idx = 0
    while size >= 1024:
        size /= 1024
        idx += 1
    if idx == 0:
        return "{:.0f} {}".format(size, suffixes[idx])
    return "{:.2f} {}".format(size, suffixes[idx])
