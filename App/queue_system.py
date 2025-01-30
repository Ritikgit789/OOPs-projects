class Patient:
    def __init__(self, name, status):
        self.name = name
        self.status = status  # 0: Normal, 1: Urgent, 2: Super-Urgent

    def __str__(self):
        return f"{self.name} ({'Normal' if self.status == 0 else 'Urgent' if self.status == 1 else 'Super-Urgent'})"


class Specialization:
    def __init__(self, name, capacity=5):
        self.name = name
        self.queue = []
        self.capacity = capacity

    def add_patient(self, patient):
        if len(self.queue) < self.capacity:
            self.queue.append(patient)
            return True
        return False

    def get_next_patient(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def remove_patient(self, name):
        for patient in self.queue:
            if patient.name == name:
                self.queue.remove(patient)
                return True
        return False

    def list_patients(self):
        return self.queue
