import datetime
from jinja2 import Template

TEMPLATE = """Title: Post {{i}} 
Date: {{date}}
Category: Page

# This is post {{i}}

[simon_signal]

"""

for i in range(10):
    tpl_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')  # 2019-09-25 10:20
    tpl = Template(TEMPLATE)
    output = tpl.render({
        'i': i,
        'date': tpl_date,
    })
    f = open('content/post{}.md'.format(i), 'wb')
    f.write(bytearray(output, 'utf-8'))
    f.flush()
    f.close()
