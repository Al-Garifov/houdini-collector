import os
from ctypes import create_unicode_buffer, windll
import hou
from cffi.backend_ctypes import unicode


def get_long_path(short_path):
    BUFFER_SIZE = 500
    buffer = create_unicode_buffer(BUFFER_SIZE)
    get_long_path_name = windll.kernel32.GetLongPathNameW
    get_long_path_name(unicode(short_path), buffer, BUFFER_SIZE)
    long_path_name = buffer.value
    return long_path_name


def get_env_lights():
    parms = set()
    for node in hou.objNodeTypeCategory().nodeType("envlight").instances():
        if node.parm("env_map"):
            parms.add(node.parm("env_map"))
    return parms


def parse(path=None):
    refs = set()
    refs.add(hou.hipFile.path())
    if path:
        hou.hipFile.load(path)

    parms = set()
    parms.update(get_env_lights())
    for parm, none in hou.fileReferences():
        parms.add(parm)

    for parm in parms:
        if not parm or not parm.eval():
            continue
        ref = os.path.abspath(hou.text.expandString(parm.eval()))
        if os.path.isfile(ref) and "~1" not in ref:
            refs.add(ref.replace("\\", "/"))
        else:
            try:
                ref = get_long_path(hou.text.expandString(parm.eval()))
                if os.path.isfile(ref):
                    refs.add(ref.replace("\\", "/"))
            except:
                # FIXME: raise an error?
                pass
    return refs
