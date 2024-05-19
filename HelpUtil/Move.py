from HelpUtil.Delete import Delete
from HelpUtil import os, shutil
import fnmatch


class Move:

    def __init__(self, change_name):
        self.change_name = change_name

    def upper(self, current_path):
        for root, directories, files in os.walk(current_path):
            # 디렉터리를 상위 디렉터리로 옮김
            for directory in directories:
                source_path = os.path.join(root, directory)
                destination_path = self.naming_process(current_path, os.path.dirname(current_path), directory, self.change_name)
                shutil.move(str(source_path), str(destination_path))

            # 파일을 상위 디렉터리로 옮김
            for file_name in files:
                source_path = os.path.join(root, file_name)
                destination_path = self.naming_process(current_path, os.path.dirname(current_path), file_name, self.change_name)
                shutil.move(str(source_path), str(destination_path))

        Delete.empty(os.path.dirname(current_path))

    def no_directories(self, current_path):
        for root, dirs, files in os.walk(current_path):
            # Exclude the current directory itself to prevent moving files to it
            if root != current_path:
                # Move each file to the current directory
                for file in files:
                    # Get the source and destination paths
                    source_path = os.path.join(root, file)
                    destination_path = self.naming_process(root, current_path, file, self.change_name)
                    # Move the file
                    shutil.move(str(source_path), str(destination_path))

        # Remove each directory
        for directory in [d for d in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, d))]:
            directory_path = os.path.join(current_path, directory)
            Delete.all(directory_path)
        Delete.new_site_pattern(current_path)

    def mv(self, src, dest):
        Delete.new_site_pattern(src)
        if not os.path.exists(dest):
            # If it doesn't exist, create it
            os.makedirs(dest)
        for root, dirs, files in os.walk(src):
            for directory in dirs:
                source_path = os.path.join(root, directory)
                destination_path = self.naming_process(src, dest, directory, self.change_name)
                shutil.move(str(source_path), str(destination_path))
            # Exclude the current directory itself to prevent moving files to it
            for file in files:
                # Get the source and destination paths
                source_path = os.path.join(root, file)
                destination_path = self.naming_process(root, dest, file, self.change_name)
                # Move the file
                shutil.move(str(source_path), str(destination_path))

        # Remove each directory
        for directory in [d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d))]:
            directory_path = os.path.join(src, directory)
            Delete.all(directory_path)

    def similar_mv(self, src, dest, name):
        Delete.new_site_pattern(src)
        if not os.path.exists(dest):
            # If it doesn't exist, create it
            os.makedirs(dest)
        for file in os.listdir(src):
            if fnmatch.fnmatch(file, f'*{name}*'):
                if os.path.isdir(os.path.join(src, file)):
                    self.mv(os.path.join(src, file), dest)
                else:
                    # Construct the file path
                    source_path = os.path.join(src, file)
                    destination_path = self.naming_process(src, dest, file, self.change_name)
                    shutil.move(str(source_path), str(destination_path))

    @staticmethod
    def naming_process(src: str, dst: str, file_name: str, change_name: bool = False):
        base_name = os.path.basename(src)
        full_name = os.path.join(dst, f"{base_name} {file_name}" if change_name else file_name)

        counter = 0
        while os.path.exists(full_name):
            counter += 1
            full_name = os.path.join(dst, f"{base_name}{counter} {file_name}")
            if counter >= 1000:
                raise RuntimeError("Failed to generate a unique filename after 1000 attempts.")

        return full_name
