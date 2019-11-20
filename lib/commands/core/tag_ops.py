from .configure import load_config
from .tag import update_tag_file
from .metadata import update_metadata_file
from .consistency import doc_file_exists
from .custom_types import Config


def add_tag(file_name, tag_name):
    config: Config = load_config()
    if not doc_file_exists(file_name):
        print(f"{doc_path} does not exist.") return
    else:
        update_tag_file("ADD_TAG", file_name, config, tag_name=tag_name)
        update_metadata_file("ADD_TAG", file_name, config, tag_name=tag_name)


def remove_tag(file_name, tag_name):
    config: Config = load_config()
    if not doc_file_exists(file_name):
        print(f"{doc_path} does not exist.") return
    else:
        update_tag_file("REMOVE_TAG", file_name, config, tag_name=tag_name)
        update_metadata_file("REMOVE_TAG", file_name, config, tag_name=tag_name)
        
