import os.path

from pxr import Usd, Vt


def get_asset_paths(stage):
    paths = set()
    for prim in stage.TraverseAll():
        for name in prim.GetPropertyNames():
            is_path = False
            attr = prim.GetAttribute(name)
            attr_type = attr.GetTypeName()
            if attr_type == "asset":
                is_path = True
            if is_path and attr.Get():
                specs = attr.GetPropertyStack(0)
                dir = None
                for spec in specs:
                    dir = os.path.dirname(str(spec.layer.resolvedPath))
                path = os.path.abspath(dir + "/" + attr.Get().path).replace("\\", "/")
                paths.add(path)
                # print(dir, attr.Get().path)
    return paths


def get_all_references(root_stage_abs_path):
    refs = set()
    get_references(root_stage_abs_path, refs)
    return refs


def get_references(stage_abs_path, refs):
    if os.path.isfile(stage_abs_path):
        stage = Usd.Stage.Open(stage_abs_path)
        refs.add(stage_abs_path.replace("\\", "/"))
        refs.update(get_asset_paths(stage))
        root = stage.GetRootLayer()
        for ref in root.GetExternalReferences():
            stage_path = os.path.abspath(os.path.dirname(stage_abs_path) + "/" + ref)
            get_references(stage_path, refs)
    else:
        print("Path does not exist: {}!".format(stage_abs_path))
