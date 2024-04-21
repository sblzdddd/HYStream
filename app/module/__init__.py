import hashlib


def format_bytes(size):
    # Define the units and their respective sizes
    units = ['bytes', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    return '{:.2f}{}'.format(size, units[unit_index])


def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()


def format_integer(n, length):
    return f"{n:0>{length}}"


def format_duration(seconds):
    minutes = seconds // 60
    seconds %= 60
    milliseconds = (seconds - int(seconds)) * 100
    return '{:02d}:{:02d}.{:02d}'.format(int(minutes), int(seconds), int(milliseconds))


def md5_hash(data):
    hash_obj = hashlib.md5()
    hash_obj.update(data.encode('utf-8'))
    md5_hash_hex = hash_obj.hexdigest()
    return md5_hash_hex


def file_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        md5_hash.update(f.read())
    return md5_hash.hexdigest()
