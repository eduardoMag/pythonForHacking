import zipfile
import optparse
from threading import Thread


def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password)
        print('[+] Found Password ' + password + '\n')
    except:
        pass


def main():
    parser = optparse.OptionParser("usage%prog " + "-f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string', help='specify')
    zFile = zipfile.ZipFile('evil.zip')
    passFile = open('dictonary.txt')
    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()


if __name__ == '__main__':
    main()
