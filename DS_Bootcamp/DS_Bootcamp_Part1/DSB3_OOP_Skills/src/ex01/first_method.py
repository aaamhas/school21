class Research:
    def file_reader(self):
        s = ''
        with open('data.csv') as f:
            for line in f:
                s += line
        return s
def main():
    research = Research()
    print(research.file_reader(), end = '')
if __name__ == '__main__':
    main()