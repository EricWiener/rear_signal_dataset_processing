import os

def write_difficulty_levels(output_path, easy, medium, hard):
    with open(os.path.join(output_path, 'easy.txt'), 'w') as f:
        for el in easy:
            f.write("%s\n" % el)

    with open(os.path.join(output_path, 'moderate.txt'), 'w') as f:
        for el in medium:
            f.write("%s\n" % el)

    with open(os.path.join(output_path, 'hard.txt'), 'w') as f:
        for el in hard:
            f.write("%s\n" % el)

class DifficultyLevels:
    def __init__(self, path_to_easy, path_to_moderate, path_to_hard):
        """
        Example usage:
        ```
        difficulties = DifficultyLevel('./Easy.txt', './Moderate.txt', './Hard.txt')
        ```
        """

        # Read the Easy, Medium, and Hard sequence lists
        with open(path_to_easy) as f:
            self.easy = f.read().splitlines()

        with open(path_to_moderate) as f:
            self.moderate = f.read().splitlines()

        with open(path_to_hard) as f:
            self.hard = f.read().splitlines()

        print("E: {}, M: {}, H: {}".format(len(self.easy), len(self.moderate), len(self.hard)))

    def get_difficulty_level(self, sequence_dir_name):
        if sequence_dir_name in self.easy:
            return "E"
        elif sequence_dir_name in self.moderate:
            return "M"
        elif sequence_dir_name in self.hard:
            return "H"
        else:
            print('Unrecognized sequence dir name: {}'.format(sequence_dir_name))
            return None

    def write_difficulty_levels(self, output_path, easy, medium, hard):
        write_difficulty_levels(output_path, easy, medium, hard)
