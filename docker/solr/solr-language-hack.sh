#!/bin/bash
#
# This script runs database commands through docker in order to attempt to map
# Solr language codes with the ONI ones.  It's very hacky, and requires manual
# work in order to get some languages working.  But it's better than being
# poked in the eye with a sharp stick.

# Current list of all language codes solr supports
solr_codes="ar bg ca cjk cz da de el en es eu fa fi fr ga gl hi hu hy id it ja lv nl no pt ro ru sv th tr"

file=partial-schema.xml
echo "" > $file
for code in $solr_codes; do
  langcode=$(docker-compose exec rdbms mysql -BN -D openoni -p123456 \
      -e "select code from core_language where lingvoj like '%$code';" | \
      grep -v "mysql: \[Warning\] Using a password" | \
      tr -d '\r\n')

  # Some languages aren't stored quite so nicely in the database, and will need manual fixups
  if [[ $langcode == "" ]]; then
    langcode=XYZZY
  fi

  echo -n '<field name="ocr_'$langcode >>$file
  echo '" type="text_'$code'" indexed="true" stored="true" required="false" multiValued="false" />' >>$file
done
