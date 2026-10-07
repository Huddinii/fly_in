import os


class ParsingError(Exception):
    errors = []

    def __call__(self, line_nr: int, line: str, msg: str):
        self.errors.append((line_nr, line, msg))

    def __str__(self):
        out = ""
        for e in self.errors:
            out += f"Error in line {e[0]}:\n{e[1]}{e[2]}\n"
        return out


class Parser:
    parsing_error = ParsingError()
    out = {}

    def parse_path(self):
        ...
        # for files in os.walk(self.path, topdown=True):
        #     self.files.append(files)

    def parse_file(self, file: str):
        with open(file) as f:
            line = f.readline()
            index = 0
            start = False
            end = False
            while line:
                index += 1
                if line.startswith("start_hub:"):
                    if not start:
                        start = True
                        self.parse_line(line, index)
                    else:
                        err = "Multiple start_hubs not allowed"
                        self.parsing_error(index, line, err)
                elif line.startswith("end_hub:"):
                    if not end:
                        end = True
                        self.parse_line(line, index)
                    else:
                        err = "Multiple end_hubs not allowed"
                        self.parsing_error(index, line, err)
                elif line.startswith(("nb_drones:", "hub:", "connection:")):
                    self.parse_line(line, index)
                elif line.startswith(("#", "\n")):
                    ...
                else:
                    self.parsing_error(index, line, "No valid input")
                line = f.readline()
        if len(self.parsing_error.errors) > 0:
            raise self.parsing_error

    def parse_line(self, line: str, index: int):
        elements = line.strip('\n').split(' ')
        ele_type = elements[0].strip(':')
        match ele_type:
            case "nb_drones":
                if len(elements) > 2 or len(elements) < 2:
                    err = "Incorrect format: nb_drones: <x>"
                    self.parsing_error(index, line, err)
                    {"nb_drones": elements[1]}
            case "connection":
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
                elif len(elements) == 3:
                    meta = elements[2].strip('[]')
                    if not meta.startswith("max_link_capacity"):
                        err = "Invalid metadata:" \
                            " Only max_link_capacity is allowed"
                        self.parsing_error(index, line, err)
            case "hub" | "starting_hub" | "end_hub":
                format_err = f"Incorrect format: {elements[0]} <name> <x>" \
                        " <y> [metadata]"
                if len(elements) > 4 and (not elements[4].startswith('[')
                                          or not elements[-1].endswith(']')):
                    self.parsing_error(index, line, format_err)
                elif len(elements) < 4:
                    self.parsing_error(index, line, format_err)
                elif len(elements) > 4:
                    self.parse_meta(elements[4:], line, index)
            case _:
                if len(elements) == 1 or elements[0].endswith("\n"):
                    err = "Incorrect format: Single word on line"
                    self.parsing_error(index, line, err)

    def parse_meta(self, metadata: list[str], line: str, index: int):
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


if __name__ == "__main__":
    pars = Parser()
    pars.parse_path()
    # print(pars.files)
    try:
        pars.parse_file("test.txt")
    except ParsingError as e:
        print(e)
