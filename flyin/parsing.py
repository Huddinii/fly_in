import os


class ParsingError(Exception):
    errors = []

    def __call__(self, line_nr: int, line: str, msg: str):
        self.errors.append((line_nr, line, msg))

    def __str__(self):
        out = ""
        for e in self.errors:
            out += f"Error in line {e[0]}: {e[1]}"
            out += f"{e[2]}\n"
        return out


class Parser:
    parsing_error = ParsingError()

    def parse_path(self):
        ...
        # for files in os.walk(self.path, topdown=True):
        #     self.files.append(files)

    def parse_file(self, file: str):
        lines = []
        with open(file) as f:
            line = f.readline()
            index = 0
            start = False
            end = False
            while line:
                if line.startswith("start_hub:"):
                    if not start:
                        start = True
                        lines.append(self.parse_line(line, index))
                    else:
                        self.parsing_error(index, line, "Multiple"
                                           " start_hubs not allowed")
                elif line.startswith("end_hub:"):
                    if not end:
                        end = True
                        lines.append(self.parse_line(line, index))
                    else:
                        self.parsing_error(index, line, "Multiple"
                                           " end_hubs not allowed")
                elif line.startswith(("nb_drones:", "hub:", "connection:")):
                    lines.append(self.parse_line(line, index))

                elif line.startswith(("#", "\n")):
                    ...
                else:
                    self.parsing_error(index, line, "No valid input")
                line = f.readline()
                index += 1
        if len(self.parsing_error.errors) > 0:
            raise self.parsing_error

    def parse_line(self, line: str, index: int):
        elements = line.split(' ')
        ele_type = elements[0].replace(':', '')
        match ele_type:
            case 'nb_drones':
                if len(elements) > 2:
                    self.parsing_error(index, line, "Incorrect format:"
                                       " nb_drones: <x>")
            case 'connection':
                if (len(elements) > 3 and elements[2].startswith('[')
                        and elements[-1].endswith(']')):
                    self.parsing_error(index, line, "Incorrect metadata:"
                                       " Duplicate or incorrect Data")
                elif ((not elements[2].startswith('[') and
                        not elements[2].endswith(']'))
                        or elements[1].find('-') == -1):
                    self.parsing_error(index, line, "Incorrect format:"
                                       " connection: <n1>-<n2> [metadata]")
                elif len(elements) == 3:
                    meta = elements[2].strip('[]')
                    if not meta.startswith("max_link_capacity"):
                        self.parsing_error(index, line, "Incorrect metadata:"
                                           " Only max_link_capacity is valid")
            case _:
                if (len(elements) > 4 and
                    (not elements[4].startswith('[')
                        or not elements[-1].endswith(']'))
                        or len(elements) < 4):
                    self.parsing_error(index, line, "Incorrect format:"
                                       f" {elements[0]}: <name> <x> <y>"
                                       " [metadata]")
        return elements


if __name__ == "__main__":
    pars = Parser()
    pars.parse_path()
    # print(pars.files)
    try:
        pars.parse_file("test.txt")
    except ParsingError as e:
        print(e)
