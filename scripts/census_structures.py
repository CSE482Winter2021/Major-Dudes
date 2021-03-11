import json
class CensusFileParser:
    @staticmethod
    def tract_population_dict(file):
        with open(file) as f:
            pop_data = json.load(f)
        pop_data = pop_data[1:]
        pop_dict = {}
        for i in range(len(pop_data)):
            tr = pop_data[i]
            pop_dict[tr[len(tr) - 1]] = [int(tr[0])]

        return pop_dict

    # TRACT FUNCTIONS
    # { tract_no : [ Total, Male, Female ] }
    @staticmethod
    def tract_gender_dict(file):
        with open(file) as f:
            gender_data = json.load(f)
        gender_data = gender_data[1:]
        gender_dict = {}
        for i in range(len(gender_data)):
            tr = gender_data[i]
            gender_dict[tr[len(tr) - 1]] = [int(tr[0]) + int(tr[24]), int(tr[0]), int(tr[24])]

        return gender_dict

    # { tract_no : [ Total, 0-4, 5-9, 10-14, 15-17, 18-19, 20, 21, 22-24, 25-29, 30-34, 35-39, 40-44, 45-29, 
    #                   50-54, 55-59, 60-61, 62-64, 65-66, 67-69, 70-74, 75-79, 80-84, 85+ ] }
    @staticmethod
    def tract_age_dict(file):
        with open(file) as f:
            gender_data = json.load(f)
        gender_data = gender_data[1:]
        age_dict = {}
        for i in range(len(gender_data)):
            tr = gender_data[i]
            tr_age_data = []
            for i in range(0, 23):
                tr_age_data.append(int(tr[i + 1]) + int(tr[i + 25]))
            tr_age_data.insert(0, sum(tr_age_data))
            age_dict[tr[len(tr) - 1]] = tr_age_data

        return age_dict

    # { tract_no : [ Total, White, Black, Native, Asian, Pacific Islander, Other ] }
    @staticmethod
    def tract_race_dict(file):
        with open(file) as f:
            race_data = json.load(f)
        race_data = race_data[1:]
        race_dict = {}
        for i in range(len(race_data)):
            tr = race_data[i]
            tr_race_data = []
            for i in range(8):
                tr_race_data.append(int(tr[i]))
            race_dict[tr[len(tr) - 1]] = tr_race_data
        return race_dict

    # { tract_no : [ Total, <10k, 10k-14999, 15k-19999, 20k-24999, 25k-29999, 30k-34999, 35k-39999, 40k-44999, 
    #                   45k-49999, 50k-59999, 60k-74999, 75k-99999, 100k-124999, 125k-149999, 150k-199999, >200k] }
    @staticmethod
    def tract_income_dict(file):
        with open(file) as f:
            income_data = json.load(f)
        income_data = income_data[1:]
        # Map from tract num to list:
        tract_income = {}
        for i in range(len(income_data)):
            tr = income_data[i]
            
            tr_income_data = []
            for i in range(len(tr) - 3):
                tr_income_data.append(int(tr[i]))
            tract_income[tr[len(tr) - 1]] = tr_income_data
        return tract_income

    # { tract_no : [ Total, num_disabled, num_not_disabled ] }
    @staticmethod
    def tract_disability_dict(file):
        with open(file) as f:
            disability_data = json.load(f)
        disability_data = disability_data[1:]

        disability_dict = {}
        for i in range(len(disability_data)):
            tr = disability_data[i]

            total_disabled = 0
            for i in range(1,13):
                total_disabled += int(tr[i])
            tr_disability_data = [int(tr[0]), total_disabled, int(tr[0]) - total_disabled]
            disability_dict[tr[len(tr) - 1]] = tr_disability_data
        return disability_dict

    # BLOCK FUNCTIONS
    @staticmethod
    def block_population_dict(file):
        with open(file) as f:
            pop_data = json.load(f)
        pop_data = pop_data[1:]
        pop_dict = {}
        for i in range(len(pop_data)):
            block_data = pop_data[i]
            if block_data[0] == '0':
                continue
            block_no = block_data[len(block_data) - 1]
            tract_no = block_data[len(block_data) - 2]
            if tract_no not in pop_dict:
                pop_dict[tract_no] = {}
            pop_dict[tract_no][block_no] = [int(block_data[0])]

        return pop_dict

    # { tract_no : { block_no : [ Total, Male, Female ] } }
    @staticmethod
    def block_gender_dict(file):
        with open(file) as f:
            gender_data = json.load(f)
        gender_data = gender_data[1:]
        gender_dict = {}
        for i in range(len(gender_data)):
            block_data = gender_data[i]
            if block_data[0] == '0':
                continue
            block_no = block_data[len(block_data) - 1]
            tract_no = block_data[len(block_data) - 2]
            if tract_no not in gender_dict:
                gender_dict[tract_no] = {}
            gender_dict[tract_no][block_no] = [int(block_data[0]) + int(block_data[24]), int(block_data[0]), int(block_data[24])]

        return gender_dict


    # { tract_no : { block_no : [ Total, 0-4, 5-9, 10-14, 15-17, 18-19, 20, 21, 22-24, 25-29, 30-34, 
    #                               35-39, 40-44, 45-29, 50-54, 55-59, 60-61, 62-64, 65-66, 67-69, 
    #                               70-74, 75-79, 80-84, 85+ ] } }
    @staticmethod
    def block_age_dict(file):
        with open(file) as f:
            age_data = json.load(f)
        age_data = age_data[1:]
        age_dict = {}
        for i in range(len(age_data)):
            block_data = age_data[i]
            if block_data[0] == '0':
                continue
            block_no = block_data[len(block_data) - 1]
            tract_no = block_data[len(block_data) - 2]
            block_age_data = []
            block_age_data.append(int(block_data[0]))
            for i in range(1, 24):
                block_age_data.append(int(block_data[i + 1]) + int(block_data[i + 25]))
            
            if tract_no not in age_dict:
                age_dict[tract_no] = {}
            age_dict[tract_no][block_no] = block_age_data

        return age_dict

    # { tract_no : { block_no : [ Total, White, Black, Native, Asian, Pacific Islander, Other ] } }
    @staticmethod
    def block_race_dict(file):
        with open(file) as f:
            race_data = json.load(f)
        race_data = race_data[1:]
        race_dict = {}
        for i in range(len(race_data)):
            block_data = race_data[i]
            if block_data[0] == '0':
                continue
            block_no = block_data[len(block_data) - 1]
            tract_no = block_data[len(block_data) - 2]

            block_race_data = []
            for i in range(7):
                block_race_data.append(int(block_data[i]))
            if tract_no not in race_dict:
                race_dict[tract_no] = {}
            race_dict[tract_no][block_no] = block_race_data
        return race_dict


    # { tract_no : { block_group_no : [ Total, <10k, 10k-14999, 15k-19999, 20k-24999, 25k-29999, 30k-34999, 35k-39999, 
    #                               40k-44999, 45k-49999, 50k-59999, 60k-74999, 75k-99999, 100k-124999, 125k-149999, 
    #                               150k-199999, >200k] } }
    @staticmethod
    def block_income_dict(file):
        with open(file) as f:
            income_data = json.load(f)
        income_data = income_data[1:]
        income_dict = {}
        for i in range(len(income_data)):
            block_data = income_data[i]
            if block_data[0] == '0':
                continue
            block_no = block_data[len(block_data) - 1]
            tract_no = block_data[len(block_data) - 2]

            block_income_data = []
            for i in range(len(block_data) - 4):
                block_income_data.append(int(block_data[i]))

            if tract_no not in income_dict:
                income_dict[tract_no] = {}
            income_dict[tract_no][block_no] = block_income_data
        return income_dict

# cp = CensusFileParser()
# raw_dir = '/Users/kristoferwong/Major-Dudes/data/census_data/raw_data'
# b_dir = '/Users/kristoferwong/Major-Dudes/data/census_data/raw_block_data'
# print(cp.block_income_dict(b_dir + '/income_bg_data.json'))
