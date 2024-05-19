from HelpUtil import os, shutil
import zipfile
import tarfile
import rarfile


class Extract:

    def get_unique_dir_name(self, base_name):
        """Returns a unique directory name by appending numbers if necessary."""
        counter = 1
        new_name = base_name
        while os.path.exists(new_name):
            new_name = f"{base_name}_{counter}"
            counter += 1
        return new_name

    def extract(self, file_path):
        base_name = os.path.splitext(file_path)[0]
        extract_dir = self.get_unique_dir_name(base_name)
        os.makedirs(extract_dir, exist_ok=True)

        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        elif file_path.endswith('.tar.gz'):
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_dir)
        elif file_path.endswith('.rar'):
            with rarfile.RarFile(file_path, 'r') as rar_ref:
                rar_ref.extractall(extract_dir)
        elif file_path.endswith('.egg'):
            with zipfile.ZipFile(file_path, 'r') as egg_ref:
                egg_ref.extractall(extract_dir)
        else:
            return

        os.remove(file_path)
