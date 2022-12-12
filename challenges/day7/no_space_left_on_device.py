# Path hack
import itertools
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


class FilesystemFile:
    id_iter = itertools.count()

    def __init__(self, name: str, is_dir: bool, size: int = 0):
        self.__id = next(FilesystemFile.id_iter)
        self.__parent = None
        self.__name = name
        self.__is_dir = is_dir
        self.__size = size
        if is_dir:
            self.__children = []  # type: list[FilesystemFile]

    def __add_child(self, child: "FilesystemFile") -> None:
        if not self.__is_dir:
            raise ValueError("You can only add children to a directory")
        self.__children.append(child)
        self.inc_size(child.size)

    def inc_size(self, size: int) -> None:
        self.__size += size
        if self.__parent is not None:
            self.__parent.inc_size(size)

    def set_parent(self, parent: "FilesystemFile") -> None:
        self.__parent = parent
        self.__parent.__add_child(self)

    def get_subdirectory(self, subdir_name: str) -> "FilesystemFile":
        """
        Returns existing child directory matching given name, else creates a 
        new one and returns that
        """
        if not self.__is_dir:
            raise ValueError("You can only get a subdirectory of a directory")
        for child in self.__children:
            if child.is_dir and child.name == subdir_name:
                return child

        new_child = FilesystemFile(subdir_name, True)
        new_child.set_parent(self)
        return new_child

    @property
    def file_id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def is_dir(self) -> bool:
        return self.__is_dir

    @property
    def size(self) -> int:
        return self.__size

    @property
    def parent(self) -> "FilesystemFile":
        return self.__parent

    @property
    def children(self) -> list["FilesystemFile"]:
        return self.__children


class Filesystem:
    def __init__(self, command_list: list[str],
                 space_available: int = 70000000):
        self.__command_list = command_list
        self.__root = FilesystemFile("__root__", True)
        self.__space_available = space_available

    def build_filesystem_from_command_list(self) -> FilesystemFile:
        curr_dir = self.__root
        for output_ln in self.__command_list[1:]:
            output_ln = output_ln.split(" ")
            if output_ln[0] == "$":
                cmd = output_ln[1:]
                if cmd[0] == "ls":
                    continue

                if cmd[0] == "cd":
                    if cmd[1] == "..":
                        curr_dir = curr_dir.parent
                    else:
                        curr_dir = curr_dir.get_subdirectory(cmd[1])
                continue

            # is ls output
            filename = output_ln[1]
            if output_ln[0] == "dir":
                child_file = FilesystemFile(filename, True)
            else:
                filesize = int(output_ln[0])
                child_file = FilesystemFile(filename, False, size=filesize)
            child_file.set_parent(curr_dir)

    def get_all_directories(self, root_dir: FilesystemFile = None) -> dict[int, FilesystemFile]:
        id_2_directory = {}
        if root_dir is None:
            root_dir = self.__root

        for child in root_dir.children:
            if child.is_dir:
                id_2_directory[child.file_id] = child
                id_2_directory.update(self.get_all_directories(child))

        return id_2_directory

    @property
    def used_space(self):
        return self.__root.size

    @property
    def unused_space(self):
        return self.__space_available - self.used_space


def _no_space_left_on_device(inp: list[str]):
    """
    Part 1: 
        Find all of the directories with a total size of at most 100000. 
        What is the sum of the total sizes of those directories?
    Part 2:
        Find the smallest directory that, if deleted, would free up enough 
        space on the filesystem to run the update. What is the total size of 
        that directory?
    """
    fs = Filesystem(inp)
    fs.build_filesystem_from_command_list()
    all_directories = fs.get_all_directories()

    min_size_to_delete = 30000000 - fs.unused_space
    to_clean_size = 0
    dir_to_delete = None  # type: FilesystemFile
    for directory in all_directories.values():
        if directory.size <= 100000:
            to_clean_size += directory.size
        if directory.size >= min_size_to_delete:
            if dir_to_delete is None or dir_to_delete.size > directory.size:
                dir_to_delete = directory

    print(f"Part 1: {to_clean_size}")
    print(f"Part 2: {dir_to_delete.size}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _no_space_left_on_device(inp)
