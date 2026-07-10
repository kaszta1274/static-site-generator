import os
import shutil

def copy_contents(source: str, destination: str) -> None:
    if not os.path.exists(source):
        raise Exception("Source directory does not exist")
    if os.path.isfile(source):
        raise Exception("Source path can't be a file")
    if os.path.isfile(destination):
        raise Exception("Destination path can't be a file")
    
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)

    def recursive_copy(current_source: str, current_destination: str) -> None:
        nested_list = os.listdir(current_source)

        for nested in nested_list:
            source_item = os.path.join(current_source, nested)
            destination_item = os.path.join(current_destination, nested)

            if os.path.isfile(source_item):
                print(f"Copying {source_item} to {destination_item}")
                shutil.copy(source_item, destination_item)
                
            else:
                os.mkdir(destination_item)                    
                recursive_copy(source_item, destination_item)

    recursive_copy(source, destination)