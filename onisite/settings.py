import ConfigParser
from settings_base import *
from settings_local import *

def override_core(conf):
  global BASE_URL
  if conf.has_option("core", "BASE_URL"):
    BASE_URL = conf.get("core", "BASE_URL")

def override_db(conf):
  global DATABASES
  for key in ("ENGINE", "HOST", "PORT", "NAME", "USER", "PASSWORD"):
    if conf.has_option("database", key):
      DATABASES['default'][key] = conf.get("database", key)

def override_solr(conf):
  global SOLR
  if conf.has_option("solr", "URL"):
    SOLR = conf.get("solr", "URL")

def override_image_server(conf):
  global RESIZE_SERVER, TILE_SERVER
  if conf.has_option("images", "RESIZE_SERVER"):
    RESIZE_SERVER = conf.get("images", "RESIZE_SERVER")
  if conf.has_option("images", "TILE_SERVER"):
    TILE_SERVER = conf.get("images", "TILE_SERVER")

def override_secrets(conf):
  global SECRET_KEY
  if conf.has_option("secrets", "SECRET_KEY"):
    SECRET_KEY = conf.get("secrets", "SECRET_KEY")

# Allow for environment overrides in /etc/openoni.ini
conffile = "/etc/openoni.ini"
if os.path.isfile(conffile):
  conf = ConfigParser.RawConfigParser(allow_no_value=True)
  conf.read(conffile)

  if conf.has_section("core"):
    override_core(conf)

  if conf.has_section("database"):
    override_db(conf)

  if conf.has_section("solr"):
    override_solr(conf)

  if conf.has_section("images"):
    override_image_server(conf)

  if conf.has_section("secrets"):
    override_secrets(conf)
