from settings import *

# These are explicitly overridden in order to verify the JSON is using the
# proper URLs, and not "http://testserver"
BASE_URL="https://oni.example.com"
RESIZE_SERVER = BASE_URL+"/images/resize"
TILE_SERVER = BASE_URL+"/images/tile"
