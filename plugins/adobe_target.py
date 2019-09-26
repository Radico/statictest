import re
from jinja2 import Template
from pelican import signals

ADOBE_TARGET_REGEX = re.compile(r'\[adobe_target\]')

TEMPLATE = """
<p>This is location: {{location}}</p>
<div id="{{selector}}"></div>
<script>

adobe.target.getOffer({
    mbox: {{location | tojson}},
    success: function(offers) {
        console.log('Success', offers)
        if (offers.length) {
            const offer = offers[0]
            if (offer.action === 'setContent') {
                $('#{{selector}}').html(offer.content)
            } else {
                console.log('Offer', offer)
            }
        }
    },
    error: function(status, error) {
        console.log('Error', status, error)
    },
})

</script>
"""


# Inspired by:
# https://github.com/riquellopes/pelican-adsense/blob/master/adsense.py
def add_adobe_target(generator):
    for article in generator.articles:
        for i, adobe_target in enumerate(
                ADOBE_TARGET_REGEX.findall(article._content)):
            tpl = Template(TEMPLATE)
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
