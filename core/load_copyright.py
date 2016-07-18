import getopt
import sys
from openoni.core.models import Copyright

def main(argv):
  inputfile = ''
  try:
    opts, args = getopt.getopt(argv,"hi:",["ifile="])
  except getopt.GetoptError:
    print 'load_copyright.py -i <inputfile>'
    sys.exit(2)
  try:
    for opt, arg in opts:
      if opt == '-h':
        print 'load_copyright.py -i <inputfile>'
        sys.exit()
      elif opt in ("-i", "--ifile"):
        inputfile = arg
      else:
        assert False, "unhandled option"

    f = open(inputfile, 'r')
    for line in f:
      arr = line.split("\t")
      if len(arr) == 2:
        record = Copyright()
        record.uri = arr[0]
        record.label =arr[1].strip()
        record.save()

    f.close()

  except:
    print (sys.exc_info()[0])

if __name__ == "__main__":
  main(sys.argv[1:])

