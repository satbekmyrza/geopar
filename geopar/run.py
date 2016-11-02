from geopar.triangulated_figure import TriangulatedFigure
from geopar.triangle import Triangle
from geopar.angle import Angle
from geopar.tfvalidator import TFValidator
from geopar.tfpreprocessor import TFPreprocessor

"""
ISSUES:
1. Does not check the input for correctness
"""

__author__ = 'satbek'


def parse_a_file(filename):
    # (Opened): a file is opened
    # AND number_of_triangles, figure instantiated
    a_file = open('../inputs/' + filename)

    # first line contains the number_of_triangles to read and dimension of Angle
    line = a_file.readline()
    line = line.split()
    number_of_triangles = int(line[0])
    dim = int(line[1])

    # all read triangles will be added to figure
    figure = TriangulatedFigure()

    # (Parsed): parsing the input.txt

    # 'point1, point2, point3; angle1, angle2, angle3'
    for i in range(number_of_triangles):
        # line = ['point1, point2, point3', 'angle1, angle2, angle3']
        line = a_file.readline().split(';')

        # _points = [point1, point2, point3]
        _points = list(map(int, line[0].split(',')))

        # angles_str = ['angle1', 'angle2', 'angle3']
        angles_str = list(map(str.strip, line[1].split(',')))

        a1 = Angle.from_str(angles_str[0], dim)
        a2 = Angle.from_str(angles_str[1], dim)
        a3 = Angle.from_str(angles_str[2], dim)

        _angles = [a1, a2, a3]
        figure.add(Triangle(_points, _angles))

    return figure


def run(figure):

    validator = TFValidator()
    preprocessor = TFPreprocessor()

    # Apply 180 and 360 rules until no new angles deduced
    preprocessor.preprocess_theorem_1(figure)
    preprocessor.preprocess_theorem_2(figure)
    while figure.anything_new:
        figure.anything_new = False
        preprocessor.preprocess_theorem_1(figure)
        preprocessor.preprocess_theorem_2(figure)

    # All angles known?
    if figure.all_angles_known():
        # 180, 360, and pairing valid?
        if validator.rule_360_valid(figure) and validator.rule_180_valid(figure) and validator.rule_pairing_valid(figure):
            print("Pre-process complete.")
            print("Here is your triangulated figure:")
            print(figure)
            print("1B. UNIQUE ALL-ANGLE CONSEQUENCE OF THE PREMISES.")

        else:
            print("Pre-process complete.")
            print('INCONCLUSIVE (1)')
    else:
        # pairing wanted?
        user_input = input('Do you want angle pairing to be applied? (y/n): ')
        print()

        if user_input == 'y':

            # Apply pairing, 180, and 360 rules until no new angles deduced
            preprocessor.preprocess_theorem_3_pairing(figure)
            preprocessor.preprocess_theorem_1(figure)
            preprocessor.preprocess_theorem_2(figure)
            while figure.anything_new:
                figure.anything_new = False
                preprocessor.preprocess_theorem_3_pairing(figure)
                preprocessor.preprocess_theorem_1(figure)
                preprocessor.preprocess_theorem_2(figure)

            # All angles known; 180, 360, and pairing valid?
            if figure.all_angles_known() and validator.rule_180_valid(figure) and validator.rule_360_valid(figure) \
                    and validator.rule_pairing_valid(figure):
                print('-------------------------')
                print("Pre-process complete.")
                print('-------------------------')
                print("2. A CONSEQUENCE OF THE PREMISES.")
                print("Here is your triangulated figure:")
                print(figure)
            else:
                print('-------------------------')
                print("Pre-process complete.")
                print('-------------------------')
                print("INCONCLUSIVE (2)")
                print("Here is your triangulated figure:")
                print(figure)

        elif user_input == 'n':
            print('-------------------------')
            print("Pre-process complete.")
            print('-------------------------')
            print('1A. INCONCLUSIVE')
            print("Here is your triangulated figure:")
            print(figure)

        else:
            print('-------------------------')
            print("Pre-process incomplete.")
            print('-------------------------')
            print('BAD INPUT. RUN THE PROGRAM AGAIN. TYPE y OR n.')

# "Pre-processing" stage
triangulated_figure = parse_a_file('input.txt')


print('-------------------------')
print('Before pre-processing:')
print('-------------------------')
print("Here is your triangulated figure:")
print(triangulated_figure)


print('-------------------------')
print('Pre-process is running...')
print('-------------------------')

run(triangulated_figure)
