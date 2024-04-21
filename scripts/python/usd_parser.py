import os.path

from pxr import Usd, Vt


def get_asset_paths(usd_abs_path):
    stage = Usd.Stage.Open(usd_abs_path)

    paths = set()
    for prim in stage.TraverseAll():
        for name in prim.GetPropertyNames():
            is_path = False
            attr = prim.GetAttribute(name)
            if attr.GetTypeName() == "asset":
                is_path = True
            elif attr.GetTypeName == "string":
                # TODO: check if it is a path
                pass
            if is_path and attr.Get():
                specs = attr.GetPropertyStack(0)
                dir = None
                for spec in specs:
                    dir = os.path.dirname(str(spec.layer.resolvedPath))
                paths.add(os.path.abspath(dir + "/" + attr.Get().path).replace("\\", "/"))
    return paths


def get_all_references(root_stage_abs_path):
    refs = set()
    get_references(root_stage_abs_path, refs)
    return refs


def get_references(stage_abs_path, refs):
    if os.path.isfile(stage_abs_path):
        refs.add(stage_abs_path.replace("\\", "/"))
        stage = Usd.Stage.Open(stage_abs_path)
        root = stage.GetRootLayer()
        for ref in root.GetExternalReferences():
            stage_path = os.path.abspath(os.path.dirname(stage_abs_path) + "/" + ref)
            get_references(stage_path, refs)
    else:
        print("Path does not exist: {}!".format(stage_abs_path))