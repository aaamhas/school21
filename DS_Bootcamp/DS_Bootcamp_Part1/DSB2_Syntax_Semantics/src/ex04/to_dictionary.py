def to_dict():
    list_of_tuples = [('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')]

    d = dict()

    for value, key in list_of_tuples:
        if key in d.keys():
            d[key].append(value)
        else:
            d[key] = [value]
    return d

def outp(d):
    for key, value in d.items():
        for i in value:
            print(f"'{key}' : '{i}'")

if __name__ == '__main__':
    outp(to_dict())