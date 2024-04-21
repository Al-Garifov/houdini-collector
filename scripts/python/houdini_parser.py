import importlib

import usd_parser
import hip_parser


def run():
    importlib.reload(hip_parser)
    importlib.reload(usd_parser)
    refs = set()
    hip_refs = hip_parser.parse()
    for ref in hip_refs:
        if ".usd" in ref:
            refs.update(usd_parser.get_asset_paths(ref))
            refs.update(usd_parser.get_all_references(ref))
    refs.update(hip_refs)

    # FIXME: fix case-sensitive scenarios
    fixed_refs = set()
    for ref in refs:
        fixed_refs.add(ref.lower())

    return fixed_refs
