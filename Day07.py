# This solution could have been much easier using the path library. However, the goal here was not to use that
# library and build a solution from scratch. Note, going forward, I will start using libraries as well.

# Get data from .txt file
def get_input() -> list[str]:
    with open('input/Day07.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
    return data


# Setup folders as a class structure
class Folder:
    # Initialize values
    def __init__(self, name):
        # Name of the folder
        self.name = name
        # Its children
        self.children = []
        # Its size
        self.size = None

    # Calculate the size of the folder
    def calc_size(self):
        # Initialize size at 0
        self.size = 0
        # Go through all its children
        for child in self.children:
            # If a child is a folder, we need to calculate the size of that folder
            if type(child[0]) == Folder:
                self.size += child[0].calc_size()
            # Else just add the size of the file
            else:
                self.size += child[1]
        return self.size

    # Method to add a child
    def add_child(self, child_name, size):
        self.children.append((child_name, size))


# This function builds the directory of objects
def build_directory(data: list) -> list:
    # Initialize variables
    current_folder = None
    root_folder = Folder('/')
    folder_list = [root_folder]
    folder_dict = {'/': root_folder}
    path = ''
    # For each instruction
    for line in data:
        # Split the instructions in its pieces
        instructions = line.split(' ')
        # We have a cd or ls instruction
        if instructions[0] == '$':
            # Move into a folder
            if instructions[1] == 'cd' and instructions[2] != '..':
                # Make sure we are not in the root directory (will throw an error because of //)
                if instructions[2] != '/':
                    # Update the path
                    path = path + instructions[2] + '/'
                # If we are in root, don't add an extra /
                else:
                    path = path + instructions[2]
                # Set the current folder to the object of the new path
                current_folder = folder_dict[path]
            # Move out of a folder
            elif instructions[1] == 'cd' and instructions[2] == '..':
                # Update the path
                path = path[:path[:-1].rfind('/') + 1]
                # Set the current folder to the object of the new path
                current_folder = folder_dict[path]
            # ls has no impact, just continue
            elif instructions[1] == 'ls':
                continue
        # We have a new folder
        elif instructions[0] == 'dir':
            # Create the new folder with the updated path
            new_folder = Folder(path + instructions[1] + '/')
            # Add this folder to the folder list
            folder_list.append(new_folder)
            # Update our folder dictionary with this folder
            folder_dict[path + instructions[1] + '/'] = new_folder
            # Add this folder as a child to the parent folder
            current_folder.add_child(new_folder, new_folder.size)
        # We have a new file
        else:
            # Add this file as a child to the parent folder
            current_folder.add_child(instructions[1], int(instructions[0]))

        # At this point we crawled through the entire instructions list and have all folders, in a second step we now
        # can calculate all folder sizes
        for folder in folder_list:
            folder.calc_size()

    return folder_list


# Solves part 1
def part_one(folder_list: list) -> int:
    # Initialize variable
    total_size = 0
    # Go through all folders in the list
    for folder in folder_list:
        # Check the size and add it if it's small enough
        if folder.size <= 100000:
            total_size += folder.size
    return total_size


# Solves part 2
def part_two(folder_list: list) -> int:
    # Initialize variables, we know that the top folder is the root and thus the biggest
    max_size = folder_list[0].size
    min_size = max_size
    # Go through all folders
    for folder in folder_list:
        # Check if each folder has the right size and is smaller than the currently smallest, available option
        if (30000000 - 70000000 + max_size) <= folder.size < min_size:
            min_size = folder.size
    return min_size


def main():
    folders = build_directory(get_input())
    print('The sum of the total sizes of those directories is:', part_one(folders))
    print('the total size of that directory is:', part_two(folders))


if __name__ == '__main__':
    main()
