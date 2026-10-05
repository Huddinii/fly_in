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
        for files in os.walk(self.path, topdown=True):
            self.files.append(files)

    def parse_file(self, file: str):
        lines = []
        with open(file) as f:
            line = f.readline()
            index = 0
            while line:
                if line.startswith(("nb_drones:", "hub:", "start_hub:",
                                    "end_hub:", "connection:")):
                    lines.append(self.parse_line(line))
                elif line.startswith(("#", "\n")):
                    ...
                else:
                    self.parsing_error(index, line, "No valid input")
                line = f.readline()
                index += 1
        if len(self.parsing_error.errors) > 0:
            raise self.parsing_error
        self.files.append((file, lines))

    def parse_line(self, line: str, index: int):
        elements = line.split(' ')
        ele_type = elements[0].replace(':', '')
        match ele_type:
            case 'nb_drones':
                if len(elements) > 2:
                    self.parsing_error(index, line, "Incorrect format:"
                                       " nb_drones: <x>")
            case 'connection':
                if len(elements) > 3 or elements[1].find('-') == -1:
                    self.parsing_error(index, line, "Incorrect format:"
                                       " connection: <n1>-<n2> [metadata]")
            case _:
                ...


if __name__ == "__main__":
    pars = Parser("../maps")
    pars.parse_path()
    print(pars.files)
    try:
        pars.parse_file("test.txt")
    except ParsingError as e:
        print(e)
