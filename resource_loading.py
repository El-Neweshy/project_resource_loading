import pandas as pd


class Activity:
    def __init__(self, name, duration, resources, predecessor=[], successor=[]):
        self.name = name
        self.duration = duration  # In weeks
        self.resources = resources  # Resources per week
        self.predecessor = predecessor
        self.successor = successor
        self.start_time = 0
        self.activity_resources_list = []


class Project:
    def __init__(self, activities):
        self.activities = activities
        self.network = self.get_levels()
        self.levels_times = self.get_levels_times()
        self.min_time = self.get_min_time()  # Min time without crashing In weeks
        self.activities_durations = self.get_activities_durations()  # Dictionary
        self.activities_start_times = self.get_activities_start_times()  # Dictionary
        self.activities_end_times = self.get_activities_end_times()  # Dictionary
        self.max_network_length = max(self.lengths(self.network))
        self.project_duration = self.activities_end_times[
            max(self.activities_end_times, key=self.activities_end_times.get)]
        self.project_acceptable_duration = self.project_duration
        self.activity_resources_lists = self.get_activity_resources_lists()
        self.resources_loading_dataframe = self.get_resources_loading_dataframe()[0]
        self.week_resource_loading = self.get_resources_loading_dataframe()[1]
        self.max_resources_per_week = max(self.week_resource_loading)

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

    def get_activity_resources_lists(self):
        activity_resources_lists = dict()
        for activity in self.activities:
            activity_resources_list = [0] * activity.start_time + [activity.resources] * activity.duration + [0] * (
                    self.project_duration - activity.duration - activity.start_time)

            activity.activity_resources_list = activity_resources_list
            activity_resources_lists.update({activity.name: activity_resources_list})

        return activity_resources_lists

    def get_resources_loading_dataframe(self):
        df = pd.DataFrame(self.activity_resources_lists)
        df.loc['Total'] = df.sum()
        df.loc[:, 'Week_total'] = df.sum(numeric_only=True, axis=1)
        week_total = df['Week_total'].tolist()
        week_total = week_total[:-1]
        return df, week_total



if __name__ == "__main__":
    # Define activities
    A = Activity(name="A", duration=8, resources=6, successor=["B"])
    B = Activity(name="B", duration=7, resources=4, predecessor=["A", "G"])
    C = Activity(name="C", duration=6, resources=4, successor=["D"])
    D = Activity(name="D", duration=2, resources=5, predecessor=["C"], successor=["E"])
    E = Activity(name="E", duration=3, resources=6, predecessor=["D"])
    F = Activity(name="F", duration=4, resources=2, successor=["G"])
    G = Activity(name="G", duration=2, resources=6, predecessor=["F"], successor=["B"])

    project = Project([A, B, C, D, E, F, G])

    print("network:", project.network)
    print("levels_times:", project.levels_times)
    print("min_time:", project.min_time)
    print("activities_durations:", project.activities_durations)
    print("activities_start_times:", project.activities_start_times)
    print("activities_end_times:", project.activities_end_times)
    print("max_network_length:", project.max_network_length)
    print("project_duration:", project.project_duration)
    # print("activity_resources_lists:", project.activity_resources_lists)
    # print("resources_loading_data:", "\n", project.resources_loading_dataframe)
    print("week_resource_loading:", project.week_resource_loading)
    print("max_resources_per_week:", project.max_resources_per_week)