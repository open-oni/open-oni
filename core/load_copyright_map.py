import getopt
import sys
import datetime
import pdb
from openoni.core.models import Copyright
from openoni.core.models import LccnDateCopyright

def check_uri(_uri):
  result = Copyright.objects.filter(uri=_uri)
  return result.exists()

def strdate_to_ordinal(date):
  date_arr = date.split('-')
  date_obj = datetime.date(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))
  return date_obj.toordinal()

def main(argv):
  inputfile = ''
  try:
    opts, args = getopt.getopt(argv,"hi:",["ifile="])
  except getopt.GetoptError:
    print 'load_copyright_map.py -i <inputfile>'
    sys.exit(2)
  try:
    for opt, arg in opts:
      if opt == '-h':
        print 'load_copyright_map.py -i <inputfile>'
        sys.exit()
      elif opt in ("-i", "--ifile"):
        inputfile = arg
      else:
        assert False, "unhandled option"

    f = open(inputfile, 'r')
    for line in f:
      arr = line.split("\t")
      if len(arr) == 4:
        if check_uri(arr[3].strip()):
          record = LccnDateCopyright()
          record.lccn = arr[0]
          record.start_date = strdate_to_ordinal(arr[1])
          record.end_date = strdate_to_ordinal(arr[2])
          result = Copyright.objects.filter(uri=arr[3].strip())
          #pdb.set_trace()
          record.uri = result[0]
          record.save()
        else:
          raise ValueError("Copyright uri not in system", arr[3])

    f.close()
  except ValueError as err:
    print(err.args)
  except:
    print (sys.exc_info()[0])

if __name__ == "__main__":
  main(sys.argv[1:])


