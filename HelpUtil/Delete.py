from HelpUtil import os
import fnmatch


class Delete:

    @classmethod
    def all(cls, path):
        # List all items in the directory
        items = os.listdir(path)
        # Iterate through each item
        for item in items:
            # Get the full path of the item
            item_path = os.path.join(path, item)
            # If it's a directory, recursively call delete_directory
            if os.path.isdir(item_path):
                Delete.all(item_path)
            # If it's a file, remove it
            else:
                os.remove(item_path)

        # Remove the directory itself
        os.rmdir(path)

    @classmethod
    def empty(cls, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                # Check if directory is empty
                if not os.listdir(str(dir_path)):
                    # Remove the directory if it's empty
                    os.rmdir(dir_path)

    @classmethod
    def new_site_pattern(cls, path):
        for root, dirs, files in os.walk(path):
            # Iterate through each file
            for file in files:
                # Check if the file name matches the specified pattern
                if fnmatch.fnmatch(file, '*new site*') or fnmatch.fnmatch(file, '*새 도메인 주소*'):
                    # Construct the file path
                    file_path = os.path.join(root, file)
                    # Delete the file
                    os.remove(file_path)
