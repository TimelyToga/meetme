from mako import util

from mako.lookup import TemplateLookup
import os
import posixpath
import re
import camoji.settings
from mako import exceptions


_template_lookup = None


def get_template(template, uri, directories):
  a_directories = [posixpath.normpath(d) for d in util.to_list(directories, ())]

  try:
    if template.filesystem_checks:
      return template._check(uri, template._collection[uri])
    else:
      return template._collection[uri]
  except KeyError:
    u = re.sub(r'^\/+', '', uri)
    for dir in a_directories:
      srcfile = os.path.join(camoji.settings.APP_DIR, dir, u)
      if os.path.isfile(srcfile):
        return template._load(srcfile, uri)
    else:
      raise exceptions.TopLevelLookupException(
        "Cant locate template for uri %r" % uri)


def render_template(template_name, **kwargs):
  global _template_lookup
  if not _template_lookup:
    _template_lookup = TemplateLookup(input_encoding='utf-8', output_encoding='utf-8')
  template = get_template(_template_lookup, template_name, ['camoji/data/templates'])
  if not template:
    return None

  return template.render(**kwargs)
