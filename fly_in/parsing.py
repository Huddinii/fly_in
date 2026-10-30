import os
from typing import Any


class ParsingError(Exception):
    def __init__(self) -> None:
        self.errors: list[tuple[int, str, str]] = []

    def __call__(self, line_nr: int, line: str, msg: str) -> None:
        self.errors.append((line_nr, line, msg))

    def __str__(self) -> str:
        out = ""
        for e in self.errors:
            out += f"Error in line {e[0]}:\n{e[1]}{e[2]}\n"
        return out


class Parser:
    def __init__(self) -> None:
        self.parsing_error: Any = None

    def get_dificulty(self) -> tuple[str, list[str]]:
        out = [(s, d) for s, d, _ in os.walk("maps")][0]
        out[1].sort()
        return out

    def get_maps(self, dif: str) -> tuple[str, list[str]]:
        out = [(s, f) for s, _, f in os.walk(dif)][0]
        out[1].sort()
        return out

    def parse_file(self, file: str) -> dict[str, Any]:
        self.parsing_error = ParsingError()
        with open(file) as f:
            map: dict[str, Any] = {"hubs": [], "connections": []}
            line = f.readline()
            index = 0
            start = False
            end = False
            while line:
                index += 1
                if line.startswith("start_hub:"):
                    if not start:
                        start = True
                        map = self.parse_line(line, index, map)
                    else:
                        err = "Multiple start_hubs not allowed"
                        self.parsing_error(index, line, err)
                elif line.startswith("end_hub:"):
                    if not end:
                        end = True
                        map = self.parse_line(line, index, map)
                    else:
                        err = "Multiple end_hubs not allowed"
                        self.parsing_error(index, line, err)
                elif line.startswith(("nb_drones:", "hub:", "connection:")):
                    map = self.parse_line(line, index, map)
                elif line.startswith(("#", "\n")):
                    ...
                else:
                    self.parsing_error(index, line, "No valid input")
                line = f.readline()
        if len(self.parsing_error.errors) > 0:
            raise self.parsing_error
        else:
            return map

    def parse_line(self, line: str, index: int,
                   map: dict[str, Any]) -> dict[str, Any]:
        elements = line.strip('\n').split(' ')
        ele_type = elements[0].strip(':')
        match ele_type:
            case "nb_drones":
                if len(elements) > 2 or len(elements) < 2:
                    err = "Incorrect format: nb_drones: <x>"
                    self.parsing_error(index, line, err)
                else:
                    map.update({"drones": elements[1]})
            case "connection":
                con = {}
                meta_err = "Incorrect metadata: Duplicate or incorrect Data"
                format_err = "Incorrect format: connection: <name1>-<name2>" \
                    " [metadata]"
                if (len(elements) > 3 and elements[2].startswith('[')
                        and elements[-1].endswith(']')):
                    self.parsing_error(index, line, meta_err)
                elif len(elements) < 2 or elements[1].find('-') == -1:
                    self.parsing_error(index, line, format_err)
                elif len(elements) > 2 and (not elements[2].startswith('[')
                                            or not elements[-1].endswith(']')):
                    self.parsing_error(index, line, format_err)
                else:
                    if len(elements) == 3:
                        meta = elements[2].strip('[]')
                        if not meta.startswith("max_link_capacity"):
                            err = "Invalid metadata:" \
                                " Only max_link_capacity is allowed"
                            self.parsing_error(index, line, err)
                        elif meta.find("=") == -1:
                            err = "Invalid metadata: No Value assigned"
                            self.parsing_error(index, line, err)
                        else:
                            cap = meta.split("=")[1]
                            con.update({"capacity": cap})
                    loc = elements[1].split("-")
                    if len(loc) > 2:
                        err = "Incorrect connection: Too many dashes in line"
                        self.parsing_error(index, line, err)
                    else:
                        con.update({"hub_from": loc[0], "hub_to": loc[1]})
                        map["connections"].append(con)
            case "hub" | "start_hub" | "end_hub":
                hub: dict[str, Any] = {}
                format_err = f"Incorrect format: {elements[0]} <name> <x>" \
                             " <y> [metadata]"
                if len(elements) > 4 and (not elements[4].startswith('[')
                                          or not elements[-1].endswith(']')):
                    self.parsing_error(index, line, format_err)
                elif len(elements) < 4:
                    self.parsing_error(index, line, format_err)
                else:
                    hub.update({"name": elements[1], "x": elements[2],
                                "y": elements[3]})
                    if ele_type.startswith("start"):
                        hub.update({"start": True})
                    if ele_type.startswith("end"):
                        hub.update({"end": True})
                    if len(elements) > 4:
                        hub.update(self.parse_meta(elements[4:], line, index))
                    map["hubs"].append(hub)
            case _:
                if len(elements) == 1 or elements[0].endswith("\n"):
                    err = "Incorrect format: Single word on line"
                    self.parsing_error(index, line, err)
        return map

    def parse_meta(self, metadata: list[str], line: str,
                   index: int) -> dict[str, str]:
        allowed = ("zone", "color", "max_drones")
        out = {}
        metadata[0] = metadata[0].strip('[')
        metadata[-1] = metadata[-1].strip(']')
        for m in metadata:
            if not m.startswith((allowed)):
                err = f"Incorrect Metadata: {m}. Only zone," \
                    " color or max_drones allowed"
                self.parsing_error(index, line, err)
            elif m.find("=") == -1:
                err = "Incorrect Metadata: No Value assigned." \
                    " Write in format: <key>=<value>"
                self.parsing_error(index, line, err)
            elif (key := m.split("=")[0]) in out:
                err = f"Incorrect Metadata: Duplicate key {key}"
                self.parsing_error(index, line, err)
            else:
                k, v = m.split("=")
                out.update({k: v})
        return out


if __name__ == "__main__":
    pars = Parser()
    out = pars.get_dificulty()
    level = pars.get_maps(out[0] + "/" + out[1][0])
    print(level)
