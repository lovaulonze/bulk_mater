import ase.db
from ase.atoms import Atoms, string2symbols
from ase.io import read
from ase.data import atomic_numbers, covalent_radii
from ase.build import bulk
from ase.parallel import parprint, world, broadcast, rank
import json
import os, os.path


class StructureBuilder(object):
    """Build crystal structure based on the json file
    Lookup the crystal structures in the `structure_path`
    """
    def __init__(self,
                 json_file=os.path.join(os.path.dirname(__file__),
                                        "../config/prototype.json"),
                 structure_path=os.path.join(os.path.dirname(__file__),
                                       "../config/crystal_structures/")):
        self.register_json(json_file, structure_path)
        return

    def register_json(self, json_file, structure_path):
        """Register the json file and structure path
        The json file has key:value with "prototype":"formula:parameters"
        compile them into plain entries since not too many
        """
        with open(json_file, "r") as f:
            data = json.load(f)
        entries = []
        # flattern the entries
        for proto, candidates in data.items():      # first key with prototype
            for formula, param in candidates.items():
                entries.append(dict(formula=formula,
                                    prototype=proto,
                                    parameters=param))

        self.__entries = entries
        self.__count = len(self.entries)
        self.__strucutre_lookup_path = structure_path
        return

    @property
    def entries(self):
        return self.__entries

    @property
    def count(self):
        return self.__count
    
    def get_structure(self, formula, prototype=None):
        """Return candidates of structure provided the information
        """
        candidates = [entry for entry in self.__entries \
                      if entry["formula"] == formula]
        if len(candidates) == 0:
            return candidates   # always empty!
        else:
            # All candidates must be returned if not specified
            if prototype is None:
                return candidates
            # Original prototype can be single entry or multiple
            # alway convert them into tuple            
            prototypes = convert_name(prototype)
            final_candidates = [c for c in candidates \
                                if c["prototype"] in prototypes]
            return list(map(self._convert_struct, final_candidates))

    def from_index(self, index):
        if hasattr(index, "__iter__"):  # iterable?
            candidates = [self.__entries[i] for i in index]
        elif isinstance(index, int): # Single index
            candidates = [self.__entries[index]]
        else:
            raise TypeError("Index must be a list or single int!")
        return list(map(self._convert_struct, candidates))

    def _convert_struct(self, param_entry):
        formula = param_entry["formula"]
        prototype = param_entry["prototype"]
        param = param_entry["parameters"]

        # Only single parameter
        if prototype in ("zincblende", "diamond",
                         "rocksalt", "cesiumchloride"):
            mater = bulk(name=formula,
                         crystalstructure=prototype,
                         a=param)
        elif prototype == "wurtzite":
            mater = bulk(name=formula,
                         crystalstructure=prototype,
                         a=param["a"],
                         c=param["c"])
        elif prototype == "other":
            if isinstance(param, str) is not True:
                raise TypeError("If the prototype is other, then it must be a string!")
            struct_file = os.path.join(self.__strucutre_lookup_path,
                                       param)
            mater = read(struct_file)  # If the structure can be guessed correctly
        else:
            mater = None        # Unknown prototype
        return mater


# May be bad formatting, need to change?
def convert_name(cs):
    """Convert the name of prototype to formal name
    """
    def convert_single(_cs):
        if isinstance(_cs, str):  # convert string name
            _cs = cs.lower()
            if _cs[0] == "z":
                return "zincblende"
            elif _cs[0] == "w":
                return "wurtzite"
            elif _cs[0] in ("n", "r"):
                return "rocksalt"
            elif _cs[0] == "c":
                return "cesiumchloride"
            elif _cs[0] == "d":
                return "diamond"
            else:
                return "other"
        else:
            return ""

    if isinstance(cs, str):
        return ([convert_single(cs)])
    elif isinstance(cs, list):
        return tuple([convert_single(c) for c in cs])
        
# Construct the bulk material using given crystalline geometry


    

if __name__ == "__main__":
    import os, sys
    if len(sys.argv) < 3:
        raise ValueError("not enough parameters")
    else:
        formula = sys.argv[1]
        cs = sys.argv[2]
        print(get_structure(formula, cs))