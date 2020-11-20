class NameGenerator:
    @staticmethod
    def get_name(columns, column_name, suffix):
        name = column_name + suffix
        i = 2
        while name in columns:
            name = column_name + suffix + str(i)
            i += 1
        return name