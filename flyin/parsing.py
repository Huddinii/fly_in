class Parser:
    files = []

    def __init__(self, path: str):
        self.path = path

    def parse_path(self):
        ...

    def parse_file(self, file: str):
        with open(file) as f:
            line = f.readline()
            while line:
                if line.startswith("nb_drones:"):
                    print("drones")
                elif line.startswith("hub:"):
                    print("hub")
                elif line.startswith("start_hub:"):
                    print("hub")
                elif line.startswith("end_hub:"):
                    print("hub")
                elif line.startswith("connection:"):
                    print("connection")
                elif line.startswith("#"):
                    ...
                elif line.startswith("\n"):
                    ...
                else:
                    raise RuntimeError("Error")
                line = f.readline()


if __name__ == "__main__":
    pars = Parser("../maps")
    try:
        pars.parse_file("test.txt")
    except RuntimeError:
        print("err")
