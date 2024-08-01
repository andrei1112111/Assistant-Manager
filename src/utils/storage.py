class Storage:
    def __init__(self):
        self.date = {}

    def update(self, dt: dict):
        for i in dt.keys():
            if i in self.date.keys():
                self.date[i] = self.date[i] + ", " + dt[i].plane_tasks
                self.date[i] = ", ".join(list(set(self.date[i].split(", "))))
            else:
                self.date[i] = dt[i].plane_tasks

    def clear(self):
        self.date = {}

    def get(self, id):
        if id in self.date.keys():
            return self.date[id]
        return ""
