import ConfigParser

def override_db(conf):
  for key in ("ENGINE", "HOST", "PORT", "NAME", "USER", "PASSWORD"):
    if conf.has_option("database", key):
      DATABASES['default'][key] = conf.get("database", key)

def override_solr(conf):
  if conf.has_option("solr", "URL"):
    SOLR = conf.get("solr", "URL")

def override_secrets(conf):
  if conf.has_option("secrets", "SECRET_KEY"):
    SECRET_KEY = conf.get("secrets", "SECRET_KEY")

# Pull in the base settings
from settings_base import *

# Pull in overrides for things like DB, solr, etc.  This line MUST come after
# the base settings!
from settings_local import *

# Allow for environment overrides in /etc/openoni.ini
conffile = "/etc/openoni.ini"
if os.path.isfile(conffile):
  conf = ConfigParser.RawConfigParser(allow_no_value=True)
  conf.read(conffile)

  if conf.has_section("database"):
    override_db(conf)

  if conf.has_section("solr"):
    override_solr(conf)

  if conf.has_section("secrets"):
    override_secrets(conf)
