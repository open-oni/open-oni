import ConfigParser
from settings_base import *
from settings_local import *

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
  global IIIF_SERVER
  if conf.has_option("images", "IIIF_SERVER"):
    IIIF_SERVER = conf.get("images", "IIIF_SERVER")

def override_secrets(conf):
  global SECRET_KEY
  if conf.has_option("secrets", "SECRET_KEY"):
    SECRET_KEY = conf.get("secrets", "SECRET_KEY")

# Allow for environment overrides in /etc/openoni.ini
conffile = "/etc/openoni.ini"
if os.path.isfile(conffile):
  conf = ConfigParser.RawConfigParser(allow_no_value=True)
  conf.read(conffile)

  if conf.has_section("database"):
    override_db(conf)

  if conf.has_section("solr"):
    override_solr(conf)

  if conf.has_section("images"):
    override_image_server(conf)

  if conf.has_section("secrets"):
    override_secrets(conf)
