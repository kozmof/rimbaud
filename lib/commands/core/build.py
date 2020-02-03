import json
from .configure import load_config
from .dir_ops import get_dir_path
from .custom_types import Config
from .metadata import load_metadata, METADATA_FILE
from .tag import load_tag_data, TAG_FILE

BUILD_CONFIG_FILE = "build.config.json"


def extract(file_names, tagged_files):
    return [tagged_file for tagged_file in tagged_files if tagged_file in file_names]


def make_build_config_file(file_names):
    config: Config = load_config()
    root_dir = config["root_path"]
    doc_dir = get_dir_path("DOCUMENT", config)
    history_dir = get_dir_path("HISTORY", config)

    metadata = load_metadata(config)
    tag_data = load_tag_data(config)

    build_config = {
        "pages": {
            file_name: {
                "doc": f"{doc_dir}/{file_name}",
                "history": f"{history_dir}/{file_name}",
                "tag": metadata[file_name].get("tag", []) if file_name in metadata else []
            } for file_name in file_names
        },

        "tags": {tag: extract(file_names, tagged_files) for tag, tagged_files in tag_data.items()}
    }

    save_path = "{root_dir}/viewer/{build_file}".format(root_dir=root_dir,
                                                        build_file=BUILD_CONFIG_FILE)

    with open(save_path, "w") as f:
        json.dump(build_config, f, indent=4, sort_keys=True)