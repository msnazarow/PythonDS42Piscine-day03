#!sgertrud/bin/python3
import os


def main():
    if os.environ['VIRTUAL_ENV'][-8:] == 'sgertrud':
        os.system("pip install beautifulsoup4 pytest")
        os.system("pip freeze > requirements.txt")
        os.system("cat requirements.txt")
    else:
        raise PermissionError("Not valid enviroment")

if __name__ == '__main__':
    main()