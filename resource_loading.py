import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy


class Activity:
    def __init__(self, name, duration, resources, predecessor=[], successor=[], dividable=False, delay=0):
        self.name = name
        self.duration = duration  # In weeks
        self.resources = resources  # Resources per week
        self.predecessor = predecessor
        self.successor = successor
        self.start_time = 0
        self.activity_resources_list = []
        self.delay = delay
        self.dividable = dividable

        if self.dividable:
            self.divided_variations = self.get_divided_variations()

    def get_divided_variations(self):
        if self.dividable and self.duration > 1:
            activity_divided_variations = []
            for i in range(self.duration):
                sub_activity = deepcopy(self)
                sub_activity.name = self.name + str(i + 1)
                sub_activity.duration = 1
                sub_activity.successor = [self.name + str(i + 2)]
                if i != 0:
                    sub_activity.predecessor = [self.name + str(i)]

                if i == self.duration - 1:
                    sub_activity.successor = self.successor

                activity_divided_variations.append(sub_activity)

        return activity_divided_variations


class Project:
    def __init__(self, activities):
        self.activities = activities
        self.activities_delays = self.get_activities_delays()
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
                        if level[-1] == item:
                            level.append(activity.name)

        return levels

    def lengths(self, x):
        if isinstance(x, list):
            yield len(x)
            for y in x:
                yield from self.lengths(y)

    def get_activities_delays(self):
        activities_delays = dict()
        for activity in self.activities:
            activities_delays.update({activity.name: activity.delay})

        return activities_delays

    def get_activities_start_times(self):
        activities_start_times = dict()

        for activity in self.activities:
            for level in self.network:
                if activity.name in level:
                    sub_level = level[0:level.index(activity.name)]
                    level_start_time = 0
                    for s in sub_level:
                        level_start_time += self.activities_durations[s]
                        level_start_time += self.activities_delays[s]

                    if level_start_time > activity.start_time:
                        activity.start_time = level_start_time
                    activity.start_time += activity.delay
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

    def activities_dataframe(self):

        data = []
        for item, value in self.activities_start_times.items():
            end = self.activities_end_times[item]
            data.append([item, value, end])

        df = pd.DataFrame(data, columns=["activity", "start_time", "end_time"])

        return df

    def visualize_activities_schedule(self):
        df = self.activities_dataframe()
        db = df[['start_time', 'end_time', 'activity']]
        # create start and end based on activity
        max_time = db.groupby(['activity'])['end_time'].max().reset_index()
        min_time = db.groupby(['activity'])['start_time'].min().reset_index()
        var_price = pd.DataFrame()
        var_price['range'] = max_time.end_time - min_time.start_time
        var_price['activity'] = min_time['activity']

        plt.figure(figsize=(8, 6))
        plt.hlines(y=min_time['activity'], xmin=min_time['start_time'], xmax=max_time['end_time'],
                   color='grey', alpha=0.4)
        plt.scatter(min_time['start_time'], min_time['activity'], color='black', alpha=1,
                    label='start time')
        plt.scatter(max_time['end_time'], max_time['activity'], color='black', alpha=1,
                    label='end time')

        plt.title("Activities Schedule")
        plt.xlabel('Weeks')
        plt.ylabel('Activities')

        plt.show()

    def visualize_resources_loading(self):
        x = np.arange(15)
        plt.bar(x, height=self.week_resource_loading)

        plt.xticks(x, [str(i + 1) for i in range(len(self.week_resource_loading))])

        plt.ylabel('Number of Resources')
        plt.xlabel('Weeks')
        plt.title("Resource Loading")
        plt.show()


class Projects:
    def __init__(self, activities, max_project_duration):
        self.activities = activities
        self.max_project_duration = max_project_duration
        self.project_variations_after_splitting = self.get_project_variations_after_splitting()
        self.all_possible_delay_combinations = self.get_all_possible_delay_combinations()
        self.all_possible_projects = self.get_all_possible_projects()

    def get_project_variations_after_splitting(self):
        project_activities = []
        for activity in self.activities:
            if activity.dividable:
                for item in activity.divided_variations:
                    project_activities.append(item)
            else:
                project_activities.append(activity)

        activity_new_ending_dict = {}
        for activity in self.activities:
            if activity.dividable:
                activity_new_ending_dict.update({activity.name: str(activity.name + str(activity.duration))})

        for activity in project_activities:
            for activity_predecessor in activity.predecessor:
                activity.predecessor = [activity_new_ending_dict[
                                            activity_predecessor] if activity_predecessor in activity_new_ending_dict else x
                                        for x in activity.predecessor]

        return project_activities

    def get_all_possible_delay_combinations(self):

        # get all combinations function
        def sums(length, total_sum):
            if length == 1:
                yield (total_sum,)
            else:
                for value in range(total_sum + 1):
                    for permutation in sums(length - 1, total_sum - value):
                        yield (value,) + permutation

        # initiate basic project to get levels data
        project = Project(self.project_variations_after_splitting)
        levels_times = project.levels_times
        network = project.network

        sorted_zipped_lists = sorted(zip(levels_times, network))
        sorted_network = [element for _, element in sorted_zipped_lists]
        sorted_network = sorted_network[::-1]
        sorted_levels_times = sorted(levels_times, reverse=True)

        # Remove duplicates from sorted network
        final_sorted_network = []
        for level in sorted_network:
            for item in level:
                if item not in final_sorted_network:
                    final_sorted_network.append(item)

        # Update number of activities in each list after removing duplicates
        new_network = []
        all_activities = []
        for level in network:
            new_level = []
            for item in level:
                if item not in all_activities:
                    new_level.append(item)
                all_activities.append(item)

            new_network.append(new_level)

        # Update number of activities in each list after removing suplicates
        new_network_wo_duplicates = []
        all_activities = []
        for level in new_network:
            new_level = []
            for item in level:
                if item not in all_activities:
                    new_level.append(item)
                all_activities.append(item)

            new_network_wo_duplicates.append(new_level)

        num_activities = [len(item) for item in new_network_wo_duplicates]

        # Create a list with all possible combinations
        items_lists = []
        for i, level_duration in enumerate(levels_times):
            allowed_total_delay_for_level = self.max_project_duration - level_duration

            item_list = []
            if allowed_total_delay_for_level == 0:
                item_list = list(sums(num_activities[i], allowed_total_delay_for_level))

            else:
                for w in range(allowed_total_delay_for_level + 1):
                    item_list += list(sums(num_activities[i], allowed_total_delay_for_level - w))
            # print('new_network', new_network_wo_duplicates, "len_of_level_list", len(item_list), "levels_times", levels_times, "allowed_delay_for_level", allowed_total_delay_for_level, "item_list", item_list)
            items_lists.append(item_list)

        def merge_two_lists_of_lists(lst1, lst2):
            if not lst1:
                return lst2

            final_lst = []
            for i in lst1:
                for j in lst2:
                    new_lst = i + j
                    final_lst.append(new_lst)
            return final_lst

        target_lst = []
        for i, item_lst in enumerate(items_lists):
            target_lst = merge_two_lists_of_lists(target_lst, item_lst)

        target_lst = list(set(target_lst))
        # print("target lst", len(target_lst), target_lst)

        return final_sorted_network, target_lst

    def get_all_possible_projects(self):
        final_sorted_network, target_lst = self.get_all_possible_delay_combinations()

        # get activity abjects ordered according to final_sorted_network
        ordered_activities = []
        for i in range(len(final_sorted_network)):
            for activity in self.project_variations_after_splitting:
                if activity.name == final_sorted_network[i]:
                    ordered_activities.append(activity)

        # generate all possible projects according to all delay combinations
        all_projects = []
        for delay_times in target_lst:
            new_activities = []
            for i, activity in enumerate(ordered_activities):
                activity_copy = deepcopy(activity)
                activity_copy.delay = delay_times[i]
                new_activities.append(activity_copy)

            # Exclude projects with durations more than allowed
            p = Project(new_activities)
            if p.project_duration <= self.max_project_duration:
                all_projects.append(p)

        return all_projects


class Conclusion:
    def __init__(self, projects):
        self.projects = projects
        self.df = self.get_projects_data_in_df()

    def get_projects_data_in_df(self):
        # df initiation
        columns = [
            "project",
            "duration",
            "Max no. resources in a week",
            "Sum of activities delays",
            "network",
            "activities start times",
            "activities end times",
            "activities durations",
            "resources allocation",
        ]
        df = pd.DataFrame(columns=columns)

        # Fill the dataframe with all projects' data
        for p in self.projects:
            # Calculate summation for activities delays
            sum_activities_delays = 0
            for activity in p.activities:
                sum_activities_delays += activity.delay

            project_data = {
                "project": p,
                "duration": p.project_duration,
                "Max no. resources in a week": p.max_resources_per_week,
                "Sum of activities delays": sum_activities_delays,
                "network": p.network,
                "activities start times": p.activities_start_times,
                "activities end times": p.activities_end_times,
                "activities durations": p.activities_durations,
                "resources allocation": p.week_resource_loading,
            }

            df = df.append(project_data, ignore_index=True)
        return df

    def print_df_csv(self):
        printed_df = deepcopy(self.df)
        printed_df = printed_df.drop('project', 1)
        printed_df.to_csv('conclusion.csv')


if __name__ == "__main__":
    # Define Maximum allowed project time
    max_project_duration = 17

    # Define activities
    activities = [
        Activity(name="A", duration=8, resources=6, successor=["B"]),
        Activity(name="B", duration=7, resources=4, predecessor=["A", "G"]),
        Activity(name="C", duration=6, resources=4, successor=["D"]),
        Activity(name="D", duration=2, resources=5, predecessor=["C"], successor=["E"]),
        Activity(name="E", duration=3, resources=6, predecessor=["D"]),
        Activity(name="F", duration=4, resources=2, successor=["G"]),
        Activity(name="G", duration=2, resources=6, predecessor=["F"], successor=["B"])
    ]

    # project_test = Project(activities=activities)
    # print(project_test.activities_start_times)
    # print(project_test.activities_end_times)
    # print(project_test.network)
    # print(project_test.project_duration)
    # print(project_test.week_resource_loading)

    # Get possible projects after considering possible splitting and delaying
    projects = Projects(activities=activities, max_project_duration=max_project_duration)

    # Get all possible projects
    all_projects = projects.all_possible_projects

    # All possible project number
    print('all_possible_project_plans', len(all_projects), '\n', '-----------------')

    # Get conclusion out of all possible projects
    conclusion = Conclusion(all_projects)
    conclusion.print_df_csv()
