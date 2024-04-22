import importlib
import usd_parser
import hip_parser

import hou


def run():
    if hou.hipFile.hasUnsavedChanges() or hou.hipFile.isNewFile():
        raise RuntimeError("Please save scene before running collector.")
    with hou.InterruptableOperation("Parsing scene...", open_interrupt_dialog=True) as oper:
        oper.updateProgress(0)
        start_frame = int(hou.playbar.frameRange()[0])
        end_frame = int(hou.playbar.frameRange()[1])
        importlib.reload(hip_parser)
        importlib.reload(usd_parser)
        refs = set()
        for frame in range(start_frame, end_frame + 1, 1):
            oper.updateProgress(frame/end_frame)
            hip_refs = hip_parser.parse(frame=frame)
            for ref in hip_refs:
                if ref in refs:
                    continue
                if ".usd" in ref:
                    refs.update(usd_parser.get_asset_paths(ref))
                    refs.update(usd_parser.get_all_references(ref))
            refs.update(hip_refs)

        # FIXME: fix case-sensitive scenarios
        fixed_refs = set()
        for ref in refs:
            fixed_refs.add(ref.lower())

    return fixed_refs
