import os
import stat

# define a type called file_representation


class FileRepresentation:
    stats: os.stat_result
    name: str
    path: str

    def __init__(self, stats: os.stat_result, name: str, path: str):
        self.stats = stats
        self.name = name
        self.path = path


# file name, owner, size, and permissions (read/write/execute - standard octal representation is acceptable)
class Result:
    def __init__(self, entry: os.DirEntry[str] = None, path: str = None):
        representation = None
        if path and not entry:
            representation = self.inspect_file(path)

        if entry and not path:
            representation = self.inspect_file(entry.path)

        if entry and path:
            raise ValueError("Cannot pass both entry and path")

        if not representation:
            raise FileNotFoundError

        self.name = representation.name
        self.path = representation.path
        self.set_type(representation)
        self.set_stats(representation)

    def __repr__(self):
        return f"<Result {self.path} {self.name} {self.type}>"
    
    # We don't need to optimize this (e.g. read as a stream) more as files are 'reasonable size' per the prompt.
    def file_contents(self):
        fd = os.open(self.path, os.O_RDONLY)
        contents = os.read(fd, self.size)
        os.close(fd)
        return contents

    def inspect_file(self, path) -> FileRepresentation:
        try:
            fd = os.open(path, os.O_RDONLY)
            stats = os.fstat(fd)
            os.close(fd)
            return FileRepresentation(
                stats=stats,
                name=os.path.basename(path),
                path=path,
            )
        except FileNotFoundError:
            return None

    def set_type(self, representation: FileRepresentation):
        stats = representation.stats
        if stat.S_ISDIR(stats.st_mode):
            self.type = "directory"
        else:
            self.type = "file" # obviously there are other types of files, but we'll ignore them per the prompt.

    def set_stats(self, representation: FileRepresentation):
        stats = representation.stats
        self.owner = stats.st_uid
        self.size = stats.st_size
        self.mode = stats.st_mode
