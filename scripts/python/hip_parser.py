import os
import hou


def get_env_lights():
    parms = set()
    for node in hou.objNodeTypeCategory().nodeType("envlight").instances():
        if node.parm("env_map"):
            parms.add(node.parm("env_map"))
    return parms


def get_parms():
    parms = set()
    parms.update(get_env_lights())
    for parm, none in hou.fileReferences():
        parms.add(parm)
    return parms


def parse(parms, frame, path=None):
    refs = set()
    refs.add(hou.hipFile.path())
    if path:
        hou.hipFile.load(path)

    for parm in parms:
        if not parm or not parm.eval():
            continue
        ref = os.path.abspath(hou.text.expandString(parm.evalAtFrame(frame)))
        if os.path.isfile(ref) and "~1" not in ref:
            refs.add(ref.replace("\\", "/"))
        else:
            try:
                ref = os.path.abspath(hou.text.expandString(parm.evalAtFrame(frame)))
                if os.path.isfile(ref):
                    refs.add(ref.replace("\\", "/"))
            except:
                # FIXME: raise an error?
                pass
    return refs
