import re
from jinja2 import Template
from pelican import signals

ADOBE_TARGET_REGEX = re.compile(r'\[adobe_target\]')

TEMPLATE = """
<p>This is location: {{location}}</p>
<div id="{{selector}}"></div>
<script>

const params = (new URL(document.location)).searchParams;
const thirdPartyId = params.get('thirdPartyId')

adobe.target.getOffers({
    request: {
        id: thirdPartyId,
        execute: {
            mboxes: [
                {index: 0, name: {{location | tojson}}}
            ]
        }
    }
}).then(response => {
    adobe.target.applyOffers({
        selector: "#{{selector}}",
        response: response,
    })
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
