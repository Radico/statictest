import os
import re
from jinja2 import Template
from pelican import signals

ADOBE_TARGET_REGEX = re.compile(r'\[adobe_target\]')
TEMPLATE_FILE = "template.jinja"


# Inspired by:
# https://github.com/riquellopes/pelican-adsense/blob/master/adsense.py
def add_adobe_target(generator):
    with open(os.path.dirname(__file__) + '/template.jinja') as file_:
        tpl = Template(file_.read())

    for article in generator.articles:
        for i, adobe_target in enumerate(
                ADOBE_TARGET_REGEX.findall(article._content)):
            context = generator.context.copy()
            context.update({
                'location': "{}-{}".format(article.slug, i),
                'selector': "at-selector-{}-{}".format(article.slug, i),
            })
            replacement = tpl.render(context)
            article._content = article._content.replace(
                adobe_target, replacement
            )


def register():
    signals.article_generator_finalized.connect(add_adobe_target)
