import os
import re
from jinja2 import Template
from pelican import signals

SIMON_SIGNAL_REGEX = re.compile(r'\[simon_signal\]')
TEMPLATE_FILE = "template.jinja"


# Inspired by:
# https://github.com/riquellopes/pelican-adsense/blob/master/adsense.py
def add_simon_signal(generator):
    with open(os.path.dirname(__file__) + '/template.jinja') as file_:
        tpl = Template(file_.read())

    for article in generator.articles:
        for i, simon_signal in enumerate(
                SIMON_SIGNAL_REGEX.findall(article._content)):
            context = generator.context.copy()
            # context.update({
            #     'location': "{}-{}".format(article.slug, i),
            #     'selector': "simon-selector-{}-{}".format(article.slug, i),
            # })
            replacement = tpl.render(context)
            article._content = article._content.replace(
                simon_signal, replacement
            )


def register():
    signals.article_generator_finalized.connect(add_simon_signal)
