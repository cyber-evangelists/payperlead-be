import importlib
import os.path

from fastapi import FastAPI


def dynamic_entities_loader(app, root_dir):
    def wrapper(*args, **kwargs):
        file_path = root_dir.replace("\\", "/")

        entity_files_path = os.listdir(file_path)

        entities_list = []
        """collecting all entity files"""
        for file in entity_files_path:
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]

                module_path = f"lib.models.entities.{module_name}"
                module = importlib.import_module(module_path)

                """making list of modules defined"""
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and obj.__module__ == module_path:
                        entities_list.append(obj)
        app.state.document_models = entities_list

    return wrapper


app = FastAPI()
