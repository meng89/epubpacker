

def relative_path(full_path, dirt):
    paths = full_path.split('/')
    dirs = dirt.split('/')
    l = len(paths) if len(paths) >= len(dirs) else len(dirs)
    for i in range(l):
        if len(paths) == i or len(dirs) == i or paths[i] != dirs[i]:
            return '/'.join(['..'] * len(dirs[i:]) + list(paths[i:]))
