class Activity:
    def __init__(self, name, duration, num_resources, predecessor=[], successor=[]):
        self.name = name
        self.duration = duration  # In weeks
        self.num_resources = num_resources  # Per week
        self.predecessor = predecessor
        self.successor = successor
        self.start_time = 0


class Project:
    def __init__(self, activities):
        self.activities = activities
        self.network = self.get_levels()
        self.levels_times = self.get_levels_times()
        self.min_time = self.get_min_time()  # Min time without crashing In weeks
        self.activities_durations = self.get_activities_durations()  # Dictionary
        self.activities_start_times = self.get_activities_start_times()     # Dictionary
        self.activities_end_times = self.get_activities_end_times()     # Dictionary
        self.max_network_length = max(self.lengths(self.network))
        self.project_duration = self.activities_end_times[max(self.activities_end_times, key=self.activities_end_times.get)]
        self.project_acceptable_duration = self.project_duration

    def get_activities_durations(self):
        activities_durations = dict()
        for activity in self.activities:
            activities_durations.update({activity.name: activity.duration})

        return activities_durations

    def get_levels_times(self):
        levels_times = []
        for level in self.network:
            level_time = 0
            for activity in self.activities:
                if activity.name in level:
                    level_time += activity.duration
            levels_times.append(level_time)
        return levels_times

    def get_min_time(self):
        return max(self.levels_times)

    def get_levels(self):
        levels = []

        for activity in self.activities:
            if len(activity.predecessor) == 0:
                level = [activity.name]
                levels.append(level)

        for i in self.activities:  # To iterate on all activities to check all successors
            for level in levels:
                for activity in self.activities:
                    for item in activity.predecessor:
                        if level[-1] == str(item):
                            level.append(activity.name)

        return levels

    # def get_activities_start_times(self):
    #     activities_start_times = dict()
    #     for activity in self.activities:
    #         predecessors_duration = 0
    #         for predecessor in activity.predecessor:
    #             if self.activities_durations[predecessor] > predecessors_duration:
    #                 predecessors_duration = self.activities_durations[predecessor]
    #
    #         activities_start_times.update({activity.name: predecessors_duration})
    #
    #     return activities_start_times

    def lengths(self, x):
        if isinstance(x, list):
            yield len(x)
            for y in x:
                yield from self.lengths(y)

    def get_activities_start_times(self):
        activities_start_times = dict()

        for activity in self.activities:
            for level in self.network:
                if activity.name in level:
                    sub_level = level[0:level.index(activity.name)]
                    level_start_time = 0
                    for s in sub_level:
                        level_start_time += self.activities_durations[s]

                    if level_start_time > activity.start_time:
                        activity.start_time = level_start_time
            activities_start_times.update({activity.name: activity.start_time})

        return activities_start_times

    def get_activities_end_times(self):
        activities_end_times = self.activities_start_times.copy()
        for item, value in activities_end_times.items():
            for activity in self.activities:
                if item == activity.name:
                    value += activity.duration
                    activities_end_times[item] = value

        return activities_end_times


if __name__ == "__main__":
    # Define activities
    A = Activity(name="A", duration=8, num_resources=6, successor=["B"])
    B = Activity(name="B", duration=7, num_resources=4, predecessor=["A", "G"])
    C = Activity(name="C", duration=6, num_resources=4, successor=["D"])
    D = Activity(name="D", duration=2, num_resources=5, predecessor=["C"], successor=["E"])
    E = Activity(name="E", duration=3, num_resources=6, predecessor=["D"])
    F = Activity(name="F", duration=4, num_resources=2, successor=["G"])
    G = Activity(name="G", duration=2, num_resources=6, predecessor=["F"], successor=["B"])

    project = Project([A, B, C, D, E, F, G])

    print("network:", project.network)
    print("levels_times:", project.levels_times)
    print("min_time:", project.min_time)
    print("activities_durations:", project.activities_durations)
    print("activities_start_times:", project.activities_start_times)
    print("activities_end_times:", project.activities_end_times)
    print("max_network_length:", project.max_network_length)
    print("project_duration:", project.project_duration)