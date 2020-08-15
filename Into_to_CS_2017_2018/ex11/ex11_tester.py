"""
create by yuval lahav
"""
from ex11_backtrack import general_backtracking
import ex11_sudoku
import ex11_map_coloring
import ex11_improve_backtrack
import time

COLORS = ex11_map_coloring.COLORS
long_map_check = False
long_sudoku_check = False


def check(num, expected, result, input, checker=None, time_took=0):
    b = expected == result
    if checker is not None:
        b = checker(expected, result)
    if b:
        to_print = "Test " + str(num) + " passed"
    else:
        to_print = "Test " + str(num) + " failed. for " + str(input) + " Should have printed " + str(
            expected) + ", printed: " + str(result)
    if time_took != 0:
        to_print = to_print + ". the time it took is " + str(time_took)
    print(to_print)


def list_check(lst1, lst2):
    for a in lst1:
        if a not in lst2:
            return False
    for a in lst2:
        if a not in lst1:
            return False
    return True


def dict_check(dict_1, dict_2):
    if not list_check(dict_1.keys(), dict_2.keys()):
        return False
    for key in dict_1.keys():
        if dict_1[key] != dict_2[key]:
            print(key)
            return False
    return True


def legal_assignment2(dic, i):
    if dic[i] == i + 2:
        return True
    return False


def legal_assignment3(dic, i):
    if dic[i] == i + 3:
        return True
    return False


def legal_assignment4(dic, i):
    if dic[i] == i + 4:
        return True
    return False


def legal_assignment_reduce(dic, i):
    if dic[i] < i:
        return False
    for key in dic.keys():
        if key == i:
            continue
        if dic[i] >= dic[key]:
            return False
    return True


def valid_map(map, neibhours):
    for item in map.keys():
        if item not in neibhours.keys():
            print("missing " + str(item))
            return False
        for neibhour in neibhours[item]:
            if neibhour not in map.keys():
                print("missing " + str(neibhour))
                return False
            if map[neibhour] == map[item]:
                print(str(item), str(neibhour), "have the same color")
                return False
    return True


if __name__ == "__main__":
    items = [1, 2, 3, 4]
    assignments = [1, 2, 3, 4, 5, 6, 7]

    # 0.1
    expected = True
    result = general_backtracking(items, {}, 0,
                                  assignments, legal_assignment2)
    check(0.1, expected, result, "")

    # 0.2
    expected = True
    result = general_backtracking(items, {}, 0,
                                  assignments, legal_assignment3)
    check(0.2, expected, result, "")

    # 0.3
    expected = False
    result = general_backtracking(items, {}, 0,
                                  assignments, legal_assignment4)
    check(0.3, expected, result, "")

    # 0.4
    expected = True
    result = general_backtracking(items, {}, 0,
                                  assignments, legal_assignment_reduce)
    check(0.4, expected, result, "")

    # 0.5
    assignments = [1, 2, 3, 4, 5, 6]
    expected = False
    result = general_backtracking(items, {}, 0,
                                  assignments, legal_assignment_reduce)
    check(0.5, expected, result, "")
    sudoku_board = {(0, 0): 0, (0, 1): 0, (0, 2): 8, (0, 3): 4, (0, 4): 3, (0, 5): 5, (0, 6): 2, (0, 7): 0, (0, 8): 1,
                    (1, 0): 2, (1, 1): 0, (1, 2): 0, (1, 3): 8, (1, 4): 0, (1, 5): 9, (1, 6): 3, (1, 7): 5, (1, 8): 4,
                    (2, 0): 0, (2, 1): 3, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (2, 6): 0, (2, 7): 6, (2, 8): 8,
                    (3, 0): 9, (3, 1): 0, (3, 2): 3, (3, 3): 6, (3, 4): 1, (3, 5): 2, (3, 6): 0, (3, 7): 4, (3, 8): 7,
                    (4, 0): 8, (4, 1): 7, (4, 2): 0, (4, 3): 0, (4, 4): 5, (4, 5): 4, (4, 6): 6, (4, 7): 1, (4, 8): 0,
                    (5, 0): 0, (5, 1): 6, (5, 2): 0, (5, 3): 9, (5, 4): 0, (5, 5): 8, (5, 6): 0, (5, 7): 0, (5, 8): 0,
                    (6, 0): 5, (6, 1): 8, (6, 2): 1, (6, 3): 2, (6, 4): 0, (6, 5): 3, (6, 6): 0, (6, 7): 0, (6, 8): 0,
                    (7, 0): 3, (7, 1): 2, (7, 2): 0, (7, 3): 0, (7, 4): 0, (7, 5): 0, (7, 6): 0, (7, 7): 0, (7, 8): 0,
                    (8, 0): 0, (8, 1): 0, (8, 2): 0, (8, 3): 5, (8, 4): 0, (8, 5): 6, (8, 6): 0, (8, 7): 0, (8, 8): 0}

    # 1.1
    sudoku_file2 = r".\sudoku_tables\sudoku_table2.txt"
    sudoku_file1 = r".\sudoku_tables\sudoku_table1.txt"
    sudoku_file3 = r".\sudoku_tables\sudoku_table3.txt"
    expected = sudoku_board
    result = ex11_sudoku.load_game(sudoku_file2)
    check(1.1, expected, result, "", dict_check)

    # 1.2.0
    expected = False
    sudoku_board[(0, 0)] = 5
    result = ex11_sudoku.check_board(sudoku_board, (0, 0))
    check("1.2.0", expected, result, "(0,0):5")
    sudoku_board[(0, 0)] = 0

    # 1.2.1
    expected = False
    sudoku_board[(7, 3)] = 2
    result = ex11_sudoku.check_board(sudoku_board, (7, 3))
    check("1.2.1", expected, result, "(7,3):2")

    # 1.2.2
    expected = True
    sudoku_board[(7, 3)] = 1
    result = ex11_sudoku.check_board(sudoku_board, (7, 3))
    check("1.2.2", expected, result, "(7,3):1")
    sudoku_board[(7, 3)] = 0

    # 1.3.0
    if long_sudoku_check:
        expected = True
        result = ex11_sudoku.run_game(sudoku_file2, True)
        check("1.3,0", expected, result, "file 2")

    # 1.3.1
    if long_sudoku_check:
        expected = True
        result = ex11_sudoku.run_game(sudoku_file1, True)
        check("1.3.1", expected, result, "file 1")

    # 1.3.2
    sudoku3 = {(0, 0): 0, (0, 1): 7, (0, 2): 0, (0, 3): 0, (0, 4): 0, (0, 5): 6, (0, 6): 0, (0, 7): 0, (0, 8): 0,
               (1, 0): 9, (1, 1): 0, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (1, 6): 0, (1, 7): 4, (1, 8): 1,
               (2, 0): 0, (2, 1): 0, (2, 2): 8, (2, 3): 0, (2, 4): 0, (2, 5): 9, (2, 6): 0, (2, 7): 5, (2, 8): 0,
               (3, 0): 0, (3, 1): 9, (3, 2): 0, (3, 3): 0, (3, 4): 0, (3, 5): 7, (3, 6): 0, (3, 7): 0, (3, 8): 2,
               (4, 0): 0, (4, 1): 0, (4, 2): 3, (4, 3): 0, (4, 4): 0, (4, 5): 0, (4, 6): 8, (4, 7): 0, (4, 8): 0,
               (5, 0): 4, (5, 1): 0, (5, 2): 0, (5, 3): 8, (5, 4): 0, (5, 5): 0, (5, 6): 0, (5, 7): 1, (5, 8): 0,
               (6, 0): 0, (6, 1): 8, (6, 2): 0, (6, 3): 3, (6, 4): 0, (6, 5): 0, (6, 6): 9, (6, 7): 0, (6, 8): 0,
               (7, 0): 1, (7, 1): 6, (7, 2): 0, (7, 3): 0, (7, 4): 0, (7, 5): 0, (7, 6): 0, (7, 7): 0, (7, 8): 7,
               (8, 0): 0, (8, 1): 0, (8, 2): 0, (8, 3): 5, (8, 4): 0, (8, 5): 0, (8, 6): 0, (8, 7): 8, (8, 8): 0}

    if long_sudoku_check:
        expected = False
        result = ex11_sudoku.run_game(sudoku_file3, True)
        check("1.3.2", expected, result, "file 3")

    # 2.1.0
    map_file1 = r".\adjacency_files\adj_usa_ex11.txt"
    usa_map = {'Alabama': ['Florida', 'Georgia', 'Mississippi', 'Tennessee'], 'Alaska': [],
               'Arizona': ['California', 'New Mexico', 'Nevada', 'Utah'],
               'Arkansas': ['Louisiana', 'Missouri', 'Mississippi', 'Oklahoma', 'Tennessee', 'Texas'],
               'California': ['Arizona', 'Nevada', 'Oregon'],
               'Colorado': ['Kansas', 'Nebraska', 'New Mexico', 'Oklahoma', 'Utah', 'Wyoming'],
               'Connecticut': ['Massachusetts', 'New York', 'Rhode Island'],
               'Delaware': ['Maryland', 'New Jersey', 'Pennsylvania'],
               'District of Columbia': ['Maryland', 'Virginia'], 'Florida': ['Alabama', 'Georgia'],
               'Georgia': ['Alabama', 'Florida', 'North Carolina', 'South Carolina', 'Tennessee'], 'Hawaii': [],
               'Idaho': ['Montana', 'Nevada', 'Oregon', 'Utah', 'Washington', 'Wyoming'],
               'Illinois': ['Iowa', 'Indiana', 'Kentucky', 'Missouri', 'Wisconsin'],
               'Indiana': ['Illinois', 'Kentucky', 'Michigan', 'Ohio'],
               'Iowa': ['Illinois', 'Minnesota', 'Missouri', 'Nebraska', 'South Dakota', 'Wisconsin'],
               'Kansas': ['Colorado', 'Missouri', 'Nebraska', 'Oklahoma'],
               'Kentucky': ['Illinois', 'Indiana', 'Missouri', 'Ohio', 'Tennessee', 'Virginia', 'West Virginia'],
               'Louisiana': ['Arkansas', 'Mississippi', 'Texas'], 'Maine': ['New Hampshire'],
               'Maryland': ['District of Columbia', 'Delaware', 'Pennsylvania', 'Virginia', 'West Virginia'],
               'Massachusetts': ['Connecticut', 'New Hampshire', 'New York', 'Rhode Island', 'Vermont'],
               'Michigan': ['Indiana', 'Ohio', 'Wisconsin'],
               'Minnesota': ['Iowa', 'North Dakota', 'South Dakota', 'Wisconsin'],
               'Mississippi': ['Alabama', 'Arkansas', 'Louisiana', 'Tennessee'],
               'Missouri': ['Arkansas', 'Iowa', 'Illinois', 'Kansas', 'Kentucky', 'Nebraska', 'Oklahoma', 'Tennessee'],
               'Montana': ['Idaho', 'North Dakota', 'South Dakota', 'Wyoming'],
               'Nebraska': ['Colorado', 'Iowa', 'Kansas', 'Missouri', 'South Dakota', 'Wyoming'],
               'Nevada': ['Arizona', 'California', 'Idaho', 'Oregon', 'Utah'],
               'New Hampshire': ['Massachusetts', 'Maine', 'Vermont'],
               'New Jersey': ['Delaware', 'New York', 'Pennsylvania'],
               'New Mexico': ['Arizona', 'Colorado', 'Oklahoma', 'Texas'],
               'New York': ['Connecticut', 'Massachusetts', 'New Jersey', 'Pennsylvania', 'Vermont'],
               'North Carolina': ['Georgia', 'South Carolina', 'Tennessee', 'Virginia'],
               'North Dakota': ['Minnesota', 'Montana', 'South Dakota'],
               'Ohio': ['Indiana', 'Kentucky', 'Michigan', 'Pennsylvania', 'West Virginia'],
               'Oklahoma': ['Arkansas', 'Colorado', 'Kansas', 'Missouri', 'New Mexico', 'Texas'],
               'Oregon': ['California', 'Idaho', 'Nevada', 'Washington'],
               'Pennsylvania': ['Delaware', 'Maryland', 'New Jersey', 'New York', 'Ohio', 'West Virginia'],
               'Rhode Island': ['Connecticut', 'Massachusetts'], 'South Carolina': ['Georgia', 'North Carolina'],
               'South Dakota': ['Iowa', 'Minnesota', 'Montana', 'North Dakota', 'Nebraska', 'Wyoming'],
               'Tennessee': ['Alabama', 'Arkansas', 'Georgia', 'Kentucky', 'Missouri', 'Mississippi', 'North Carolina',
                             'Virginia'], 'Texas': ['Arkansas', 'Louisiana', 'New Mexico', 'Oklahoma'],
               'Utah': ['Arizona', 'Colorado', 'Idaho', 'Nevada', 'Wyoming'],
               'Vermont': ['Massachusetts', 'New Hampshire', 'New York'],
               'Virginia': ['District of Columbia', 'Kentucky', 'Maryland', 'North Carolina', 'Tennessee',
                            'West Virginia'], 'Washington': ['Idaho', 'Oregon'],
               'West Virginia': ['Kentucky', 'Maryland', 'Ohio', 'Pennsylvania', 'Virginia'],
               'Wisconsin': ['Iowa', 'Illinois', 'Michigan', 'Minnesota'],
               'Wyoming': ['Colorado', 'Idaho', 'Montana', 'Nebraska', 'South Dakota', 'Utah']}
    expected = usa_map
    result = ex11_map_coloring.read_adj_file(map_file1)
    check("2.1.0", expected, result, map_file1, dict_check)

    # 2.1.1
    map_file2 = r".\adjacency_files\adj_world_ex11.txt"
    world_map = {'Afghanistan': ['China', 'Iran', 'Pakistan', 'Tajikistan', 'Turkmenistan', 'Uzbekistan'],
                 'Aland': [], 'Albania': ['Greece', 'Kosovo', 'Macedonia', 'Montenegro', 'Serbia'],
                 'Algeria': ['Libya', 'Mali', 'Mauritania', 'Morocco', 'Niger', 'Tunisia', 'W. Sahara'],
                 'American Samoa': [], 'Andorra': ['France', 'Spain'],
                 'Angola': ['Dem. Rep. Congo', 'Namibia', 'Congo', 'Zambia'], 'Anguilla': [], 'Antarctica': [],
                 'Antigua and Barb.': [], 'Argentina': ['Bolivia', 'Brazil', 'Chile', 'Paraguay', 'Uruguay'],
                 'Armenia': ['Azerbaijan', 'Georgia', 'Iran', 'Turkey'], 'Aruba': [], 'Australia': [],
                 'Austria': ['Czech Rep.', 'Germany', 'Hungary', 'Italy', 'Liechtenstein', 'Slovakia', 'Slovenia',
                             'Switzerland'], 'Azerbaijan': ['Armenia', 'Georgia', 'Iran', 'Russia', 'Turkey'],
                 'Bahamas': [], 'Bahrain': [], 'Bangladesh': ['India', 'Myanmar'], 'Barbados': [],
                 'Belarus': ['Latvia', 'Lithuania', 'Poland', 'Russia', 'Ukraine'],
                 'Belgium': ['France', 'Germany', 'Luxembourg', 'Netherlands'], 'Belize': ['Guatemala', 'Mexico'],
                 'Benin': ['Burkina Faso', 'Niger', 'Nigeria', 'Togo'], 'Bermuda': [], 'Bhutan': ['China', 'India'],
                 'Bolivia': ['Argentina', 'Brazil', 'Chile', 'Paraguay', 'Peru'],
                 'Bosnia and Herz.': ['Croatia', 'Montenegro', 'Serbia'],
                 'Botswana': ['Namibia', 'South Africa', 'Zimbabwe'], 'Br. Indian Ocean Ter.': [],
                 'Brazil': ['Argentina', 'Bolivia', 'Colombia', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay',
                            'Venezuela'], 'British Virgin Is.': [], 'Brunei': ['Malaysia'],
                 'Bulgaria': ['Greece', 'Macedonia', 'Romania', 'Serbia', 'Turkey'],
                 'Burkina Faso': ['Benin', 'Ghana', "CÃ´te d'Ivoire", 'Mali', 'Niger', 'Togo'],
                 'Burundi': ['Dem. Rep. Congo', 'Rwanda', 'Tanzania'], 'Cambodia': ['Lao PDR', 'Thailand', 'Vietnam'],
                 'Cameroon': ['Central African Rep.', 'Chad', 'Eq. Guinea', 'Gabon', 'Nigeria', 'Congo'],
                 'Canada': ['United States'], 'Cape Verde': [], 'Cayman Is.': [],
                 'Central African Rep.': ['Cameroon', 'Chad', 'Dem. Rep. Congo', 'Congo', 'S. Sudan', 'Sudan'],
                 'Chad': ['Cameroon', 'Central African Rep.', 'Libya', 'Niger', 'Nigeria', 'Sudan'],
                 'Chile': ['Argentina', 'Bolivia', 'Peru'],
                 'China': ['Afghanistan', 'Bhutan', 'India', 'Kazakhstan', 'Kyrgyzstan', 'Lao PDR', 'Mongolia',
                           'Myanmar', 'Nepal', 'Dem. Rep. Korea', 'Pakistan', 'Russia', 'Tajikistan', 'Vietnam'],
                 'Colombia': ['Brazil', 'Ecuador', 'Panama', 'Peru', 'Venezuela'], 'Comoros': [],
                 'Congo': ['Angola', 'Cameroon', 'Central African Rep.', 'Dem. Rep. Congo', 'Gabon'], 'Cook Is.': [],
                 'Costa Rica': ['Nicaragua', 'Panama'],
                 'Croatia': ['Bosnia and Herz.', 'Hungary', 'Montenegro', 'Serbia', 'Slovenia'],
                 'Cuba': ['United States'], 'CuraÃ§ao': [], 'Cyprus': [],
                 'Czech Rep.': ['Austria', 'Germany', 'Poland', 'Slovakia'],
                 "CÃ´te d'Ivoire": ['Burkina Faso', 'Ghana', 'Guinea', 'Liberia', 'Mali'],
                 'Dem. Rep. Congo': ['Angola', 'Burundi', 'Central African Rep.', 'Congo', 'Rwanda', 'S. Sudan',
                                     'Tanzania', 'Uganda', 'Zambia'], 'Dem. Rep. Korea': ['China', 'Russia', 'Korea'],
                 'Denmark': ['Germany'], 'Djibouti': ['Eritrea', 'Ethiopia', 'Somalia'], 'Dominica': [],
                 'Dominican Rep.': ['Haiti'], 'Ecuador': ['Colombia', 'Peru'], 'Egypt': ['Israel', 'Libya', 'Sudan'],
                 'El Salvador': ['Guatemala', 'Honduras'], 'Eq. Guinea': ['Cameroon', 'Gabon'],
                 'Eritrea': ['Djibouti', 'Ethiopia', 'Sudan'], 'Estonia': ['Latvia', 'Russia'],
                 'Ethiopia': ['Djibouti', 'Eritrea', 'Kenya', 'Somalia', 'S. Sudan', 'Sudan'], 'Faeroe Is.': [],
                 'Falkland Is.': [], 'Fiji': [], 'Finland': ['Norway', 'Russia', 'Sweden'], 'Fr. Polynesia': [],
                 'Fr. S. Antarctic Lands': [],
                 'France': ['Andorra', 'Belgium', 'Germany', 'Italy', 'Luxembourg', 'Monaco', 'Spain', 'Switzerland'],
                 'Gabon': ['Cameroon', 'Eq. Guinea', 'Congo'], 'Gambia': ['Senegal'],
                 'Georgia': ['Armenia', 'Azerbaijan', 'Russia', 'Turkey'],
                 'Germany': ['Austria', 'Belgium', 'Czech Rep.', 'Denmark', 'France', 'Luxembourg', 'Netherlands',
                             'Poland', 'Switzerland'], 'Ghana': ['Burkina Faso', "CÃ´te d'Ivoire", 'Togo'],
                 'Gibraltar': ['Spain'], 'Greece': ['Albania', 'Bulgaria', 'Macedonia', 'Turkey'], 'Greenland': [],
                 'Grenada': [], 'Guam': [], 'Guatemala': ['Belize', 'El Salvador', 'Honduras', 'Mexico'],
                 'Guernsey': [],
                 'Guinea': ['Guinea-Bissau', "CÃ´te d'Ivoire", 'Liberia', 'Mali', 'Senegal', 'Sierra Leone'],
                 'Guinea-Bissau': ['Guinea', 'Senegal'], 'Guyana': ['Brazil', 'Suriname', 'Venezuela'],
                 'Haiti': ['Dominican Rep.'], 'Heard I. and McDonald Is.': [],
                 'Honduras': ['El Salvador', 'Guatemala', 'Nicaragua'], 'Hong Kong': [],
                 'Hungary': ['Austria', 'Croatia', 'Romania', 'Serbia', 'Slovakia', 'Slovenia', 'Ukraine'],
                 'Iceland': [], 'India': ['Bangladesh', 'Bhutan', 'China', 'Myanmar', 'Nepal', 'Pakistan'],
                 'Indonesia': ['Timor-Leste', 'Malaysia', 'Papua New Guinea'],
                 'Iran': ['Afghanistan', 'Armenia', 'Azerbaijan', 'Iraq', 'Pakistan', 'Turkey', 'Turkmenistan'],
                 'Iraq': ['Iran', 'Jordan', 'Kuwait', 'Saudi Arabia', 'Syria', 'Turkey'], 'Ireland': ['United Kingdom'],
                 'Isle of Man': [], 'Israel': ['Egypt', 'Jordan', 'Lebanon', 'Palestine', 'Syria'],
                 'Italy': ['Austria', 'France', 'San Marino', 'Slovenia', 'Switzerland', 'Vatican'], 'Jamaica': [],
                 'Japan': [], 'Jersey': [], 'Jordan': ['Iraq', 'Israel', 'Palestine', 'Saudi Arabia', 'Syria'],
                 'Kazakhstan': ['China', 'Kyrgyzstan', 'Russia', 'Turkmenistan', 'Uzbekistan'],
                 'Kenya': ['Ethiopia', 'Somalia', 'S. Sudan', 'Tanzania', 'Uganda'], 'Kiribati': [],
                 'Korea': ['Dem. Rep. Korea'], 'Kosovo': ['Albania', 'Macedonia', 'Montenegro', 'Serbia'],
                 'Kuwait': ['Iraq', 'Saudi Arabia'], 'Kyrgyzstan': ['China', 'Kazakhstan', 'Tajikistan', 'Uzbekistan'],
                 'Lao PDR': ['Cambodia', 'China', 'Myanmar', 'Thailand', 'Vietnam'],
                 'Latvia': ['Belarus', 'Estonia', 'Lithuania', 'Russia'], 'Lebanon': ['Israel', 'Syria'],
                 'Lesotho': ['South Africa'], 'Liberia': ['Guinea', "CÃ´te d'Ivoire", 'Sierra Leone'],
                 'Libya': ['Algeria', 'Chad', 'Egypt', 'Niger', 'Sudan', 'Tunisia'],
                 'Liechtenstein': ['Austria', 'Switzerland'], 'Lithuania': ['Belarus', 'Latvia', 'Poland', 'Russia'],
                 'Luxembourg': ['Belgium', 'France', 'Germany'], 'Macao': [],
                 'Macedonia': ['Albania', 'Bulgaria', 'Greece', 'Kosovo', 'Serbia'], 'Madagascar': [],
                 'Malawi': ['Mozambique', 'Tanzania', 'Zambia'], 'Malaysia': ['Brunei', 'Indonesia', 'Thailand'],
                 'Maldives': [],
                 'Mali': ['Algeria', 'Burkina Faso', 'Guinea', "CÃ´te d'Ivoire", 'Mauritania', 'Niger', 'Senegal'],
                 'Malta': [], 'Marshall Is.': [], 'Mauritania': ['Algeria', 'Mali', 'Senegal', 'W. Sahara'],
                 'Mauritius': [], 'Mexico': ['Belize', 'Guatemala', 'United States'], 'Micronesia': [],
                 'Moldova': ['Romania', 'Ukraine'], 'Monaco': ['France'], 'Mongolia': ['China', 'Russia'],
                 'Montenegro': ['Albania', 'Bosnia and Herz.', 'Croatia', 'Kosovo', 'Serbia'], 'Montserrat': [],
                 'Morocco': ['Algeria', 'W. Sahara'],
                 'Mozambique': ['Malawi', 'South Africa', 'Swaziland', 'Tanzania', 'Zambia', 'Zimbabwe'],
                 'Myanmar': ['Bangladesh', 'China', 'India', 'Lao PDR', 'Thailand'], 'N. Mariana Is.': [],
                 'Namibia': ['Angola', 'Botswana', 'South Africa', 'Zambia'], 'Nauru': [],
                 'Nepal': ['China', 'India'], 'Netherlands': ['Belgium', 'Germany'], 'New Caledonia': [],
                 'New Zealand': [], 'Nicaragua': ['Costa Rica', 'Honduras'],
                 'Niger': ['Algeria', 'Benin', 'Burkina Faso', 'Chad', 'Libya', 'Mali', 'Nigeria'],
                 'Nigeria': ['Benin', 'Cameroon', 'Chad', 'Niger'], 'Niue': [], 'Norfolk Island': [],
                 'Norway': ['Finland', 'Russia', 'Sweden'], 'Oman': ['Saudi Arabia', 'United Arab Emirates', 'Yemen'],
                 'Pakistan': ['Afghanistan', 'China', 'India', 'Iran'], 'Palau': [],
                 'Palestine': ['Israel', 'Jordan'], 'Panama': ['Colombia', 'Costa Rica'],
                 'Papua New Guinea': ['Indonesia'], 'Paraguay': ['Argentina', 'Bolivia', 'Brazil'],
                 'Peru': ['Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador'], 'Philippines': [],
                 'Pitcairn Is.': [],
                 'Poland': ['Belarus', 'Czech Rep.', 'Germany', 'Lithuania', 'Russia', 'Slovakia', 'Ukraine'],
                 'Portugal': ['Spain'], 'Puerto Rico': [], 'Qatar': ['Saudi Arabia'],
                 'Romania': ['Bulgaria', 'Hungary', 'Moldova', 'Serbia', 'Ukraine'],
                 'Russia': ['Azerbaijan', 'Belarus', 'China', 'Estonia', 'Finland', 'Georgia', 'Kazakhstan', 'Latvia',
                            'Lithuania', 'Mongolia', 'Dem. Rep. Korea', 'Norway', 'Poland', 'Ukraine'],
                 'Rwanda': ['Burundi', 'Dem. Rep. Congo', 'Tanzania', 'Uganda'], 'S. Geo. and S. Sandw. Is.': [],
                 'S. Sudan': ['Central African Rep.', 'Dem. Rep. Congo', 'Ethiopia', 'Kenya', 'Sudan', 'Uganda'],
                 'Saint Helena': [], 'Saint Lucia': [], 'Samoa': [], 'San Marino': ['Italy'],
                 'Saudi Arabia': ['Iraq', 'Jordan', 'Kuwait', 'Oman', 'Qatar', 'United Arab Emirates', 'Yemen'],
                 'Senegal': ['Gambia', 'Guinea', 'Guinea-Bissau', 'Mali', 'Mauritania'],
                 'Serbia': ['Albania', 'Bosnia and Herz.', 'Bulgaria', 'Croatia', 'Hungary', 'Kosovo', 'Macedonia',
                            'Montenegro', 'Romania'], 'Seychelles': [], 'Sierra Leone': ['Guinea', 'Liberia'],
                 'Singapore': [], 'Sint Maarten': ['St-Martin'],
                 'Slovakia': ['Austria', 'Czech Rep.', 'Hungary', 'Poland', 'Ukraine'],
                 'Slovenia': ['Austria', 'Croatia', 'Hungary', 'Italy'], 'Solomon Is.': [],
                 'Somalia': ['Djibouti', 'Ethiopia', 'Kenya'],
                 'South Africa': ['Botswana', 'Lesotho', 'Mozambique', 'Namibia', 'Swaziland', 'Zimbabwe'],
                 'Spain': ['Andorra', 'France', 'Gibraltar', 'Portugal'], 'Sri Lanka': [], 'St-BarthÃ©lemy': [],
                 'St-Martin': ['Sint Maarten'], 'St. Kitts and Nevis': [], 'St. Pierre and Miquelon': [],
                 'St. Vin. and Gren.': [],
                 'Sudan': ['Central African Rep.', 'Chad', 'Egypt', 'Eritrea', 'Ethiopia', 'Libya', 'S. Sudan'],
                 'Suriname': ['Brazil', 'Guyana'], 'Swaziland': ['Mozambique', 'South Africa'],
                 'Sweden': ['Finland', 'Norway'],
                 'Switzerland': ['Austria', 'France', 'Germany', 'Italy', 'Liechtenstein'],
                 'Syria': ['Iraq', 'Israel', 'Jordan', 'Lebanon', 'Turkey'], 'SÃ£o TomÃ© and Principe': [],
                 'Taiwan': [], 'Tajikistan': ['Afghanistan', 'China', 'Kyrgyzstan', 'Uzbekistan'],
                 'Tanzania': ['Burundi', 'Dem. Rep. Congo', 'Kenya', 'Malawi', 'Mozambique', 'Rwanda', 'Uganda',
                              'Zambia'], 'Thailand': ['Cambodia', 'Lao PDR', 'Malaysia', 'Myanmar'],
                 'Timor-Leste': ['Indonesia'], 'Togo': ['Benin', 'Burkina Faso', 'Ghana'], 'Tonga': [],
                 'Trinidad and Tobago': [], 'Tunisia': ['Algeria', 'Libya'],
                 'Turkey': ['Armenia', 'Azerbaijan', 'Bulgaria', 'Georgia', 'Greece', 'Iran', 'Iraq', 'Syria'],
                 'Turkmenistan': ['Afghanistan', 'Iran', 'Kazakhstan', 'Uzbekistan'], 'Turks and Caicos Is.': [],
                 'Tuvalu': [], 'U.S. Minor Outlying Is.': [], 'U.S. Virgin Is.': [],
                 'Uganda': ['Dem. Rep. Congo', 'Kenya', 'Rwanda', 'S. Sudan', 'Tanzania'],
                 'Ukraine': ['Belarus', 'Hungary', 'Moldova', 'Poland', 'Romania', 'Russia', 'Slovakia'],
                 'United Arab Emirates': ['Oman', 'Saudi Arabia'], 'United Kingdom': ['Ireland'],
                 'United States': ['Canada', 'Cuba', 'Mexico'], 'Uruguay': ['Argentina', 'Brazil'],
                 'Uzbekistan': ['Afghanistan', 'Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Turkmenistan'],
                 'Vanuatu': [], 'Vatican': ['Italy'], 'Venezuela': ['Brazil', 'Colombia', 'Guyana'],
                 'Vietnam': ['Cambodia', 'China', 'Lao PDR'], 'W. Sahara': ['Algeria', 'Mauritania', 'Morocco'],
                 'Wallis and Futuna Is.': [], 'Yemen': ['Oman', 'Saudi Arabia'],
                 'Zambia': ['Angola', 'Dem. Rep. Congo', 'Malawi', 'Mozambique', 'Namibia', 'Tanzania', 'Zimbabwe'],
                 'Zimbabwe': ['Botswana', 'Mozambique', 'South Africa', 'Zambia']}
    expected = world_map
    result = ex11_map_coloring.read_adj_file(map_file2)
    check("2.1.1", expected, result, map_file1, dict_check)

    usa_solution = {'Alabama': 'red', 'Alaska': 'red', 'Arizona': 'red', 'Arkansas': 'red', 'California': 'blue',
                    'Colorado': 'red', 'Connecticut': 'red', 'Delaware': 'red', 'District of Columbia': 'red',
                    'Florida': 'blue', 'Georgia': 'green', 'Hawaii': 'red', 'Idaho': 'red', 'Illinois': 'red',
                    'Indiana': 'blue', 'Iowa': 'blue', 'Kansas': 'blue', 'Kentucky': 'green', 'Louisiana': 'blue',
                    'Maine': 'red', 'Maryland': 'blue', 'Massachusetts': 'blue', 'Michigan': 'red', 'Minnesota': 'red',
                    'Mississippi': 'green', 'Missouri': 'magenta', 'Montana': 'green', 'Nebraska': 'green',
                    'Nevada': 'green', 'New Hampshire': 'green', 'New Jersey': 'blue', 'New Mexico': 'blue',
                    'New York': 'magenta', 'North Carolina': 'red', 'North Dakota': 'blue', 'Ohio': 'magenta',
                    'Oklahoma': 'green', 'Oregon': 'magenta', 'Pennsylvania': 'green', 'Rhode Island': 'green',
                    'South Carolina': 'blue', 'South Dakota': 'magenta', 'Tennessee': 'blue', 'Texas': 'magenta',
                    'Utah': 'magenta', 'Vermont': 'red', 'Virginia': 'magenta', 'Washington': 'blue',
                    'West Virginia': 'red', 'Wisconsin': 'green', 'Wyoming': 'blue'}

    # 2.2.0
    s = time.clock()
    expected = None
    result = ex11_map_coloring.run_map_coloring(map_file1, 2)
    e = time.clock()
    check("2.2.0", expected, result, "usa map, color=2", time_took=str(e - s))

    # 2.2.1
    s = time.clock()
    expected = True
    result = valid_map(ex11_map_coloring.run_map_coloring(map_file1, 4), usa_map)
    e = time.clock()
    check("2.2.1", expected, result, "usa map, color=4", time_took=e - s)

    if long_map_check:
        # 2.2.2
        expected = True
        result = ex11_map_coloring.run_map_coloring(map_file2, 4)
        check("2.2.2", expected, result, "world map, color=4")

        # 2.2.3
        expected = None
        result = ex11_map_coloring.run_map_coloring(map_file2, 2)
        check("2.2.3", expected, result, "world map, color=2")

    # 3.0
    s = time.clock()
    expected = None
    result = ex11_improve_backtrack.back_track_degree_heuristic(usa_map, COLORS[:2])
    e = time.clock()
    check("3.0", expected, result, "usa map, color=2", time_took=str(e - s))

    # 3.1
    s = time.clock()
    expected = True
    result = valid_map(ex11_improve_backtrack.back_track_degree_heuristic(usa_map, COLORS[:4]), usa_map)
    e = time.clock()
    check("3.1", expected, result, "usa map, color=4", time_took=str(e - s))

    if long_map_check:
        # 3.2
        s = time.clock()
        expected = True
        result = ex11_improve_backtrack.back_track_degree_heuristic(world_map, COLORS[:4])
        e = time.clock()
        check("3.2", expected, result, "world map, color=4", time_took=str(e - s))

    # 4.0
    s = time.clock()
    expected = None
    result = ex11_improve_backtrack.back_track_MRV(usa_map, COLORS[:2])
    e = time.clock()
    check("4.0", expected, result, "usa map, color=2", time_took=str(e - s))

    # 4.1
    s = time.clock()
    expected = True
    result = valid_map(ex11_improve_backtrack.back_track_MRV(usa_map, COLORS[:4]), usa_map)
    e = time.clock()
    check("4.1", expected, result, "usa map, color=4", time_took=str(e - s))

    if long_map_check:
        # 4.2
        s = time.clock()
        expected = True
        result = ex11_improve_backtrack.back_track_degree_heuristic(world_map, COLORS[:4])
        e = time.clock()
        check("4.2", expected, result, "world map, color=4", time_took=str(e - s))

    # 5.0
    s = time.clock()
    expected = None
    result = ex11_improve_backtrack.back_track_FC(usa_map, COLORS[:2])
    e = time.clock()
    check("5.0", expected, result, "usa map, color=2", time_took=str(e - s))

    # 5.1
    s = time.clock()
    expected = True
    result = valid_map(ex11_improve_backtrack.back_track_FC(usa_map, COLORS[:4]), usa_map)
    e = time.clock()
    check("5.1", expected, result, "usa map, color=4", time_took=str(e - s))

    # 6.0
    s = time.clock()
    expected = None
    result = ex11_improve_backtrack.back_track_LCV(usa_map, COLORS[:2])
    e = time.clock()
    check("5.0", expected, result, "usa map, color=2", time_took=str(e - s))

    # 6.1
    s = time.clock()
    expected = True
    result = valid_map(ex11_improve_backtrack.back_track_LCV(usa_map, COLORS[:4]), usa_map)
    e = time.clock()
    check("5.1", expected, result, "usa map, color=4", time_took=str(e - s))
