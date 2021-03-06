# Simon Static Test Site

## What is this?

This is a static site hosted on S3 used to test the Adobe Target integration.
It could be a platform for testing other website integrations in the future.

This project uses [Pelican](https://github.com/getpelican/pelican) to generate a
bunch of static pages with Adobe Target integration.  The pages host *locations*
where Adobe Target can be configured to display *offers*.

## How does it work?

Pelican is a static site generator written in python.  The project was 
bootstrapped by following the 
[Pelican Quickstart](https://docs.getpelican.com/en/stable/quickstart.html)
instructions.
 
The pages themselves were generated by the custom script `generate-content.py`.
This script produced a bunch of `post*.md` files in the `content` directory. 
These files don't have much content, but they do have an anchor, 
`[adobe_target]`, that gets replaced by a custom plugin with dynamically 
generated HTML & JS.  Feel free to customise the posts or regenerate them.

The HTML & JS added by the custom plugin queries Adobe Target, asking if there
are any offers that should be displayed in a particular location.  The location
is generated from the "post" name in pelican.  A post can have multiple 
locations, which will be indexed numerically, but so far each post only has one.
If Adobe Target responds with an offer for the location, then its content is
written into the DOM also using Adobe Target.

### How to use a contact identity

Add the query string `?thirdPartyId=` to the URL and set the value to the
contact's thirdPartyId value used in Adobe Target. 

## Developing

After cloning, run `bash setup.sh` to initialize the virtualenv and install 
dependencies with pip.

Then activate the venv in your shell: `source ./venv/bin/activate`

Generate the site (creating files in the `output` folder): `pelican content`

Run the development server: `pelican --listen`

Now you can [load the site locally](http://localhost:8000)

When you're happy with it, you can deploy the site to S3 with: `make s3_upload`

## Files to be aware of

- `plugins/adobe_target/__init__.py`: this is a Pelican plugin that replaces its
token with dynamic HTML & JS.
- `plugins/adobe_target/template.jinja`: this is the dynamic HTML & JS template
- `content/`: this folder has the posts.  you can modify these to give them a
unique look.
- `generate-content.py`: quick script to generate a bunch of files in the 
`content/` folder.
- `output/`: where generated content will be written. this is excluded from git.
- `setup.sh`: bootstrap the project development environment
- `pelicanconf.py`: settings to control pelican
- `themes/elegant`: an open source theme from the internet with our
customizations
- `themes/elegant/static/simon`: this is where you can put static assets. they
can then be referenced in HTML under `theme/simon/`
- `themes/elegant/templates/base.html`: outer page container template (jinja).
we include a custom template at the end of the `<head>` in this file.
- `themes/elegant/templates/_includes/simon/adobe.html`: stuff we want to 
include in the `<head>` for Adobe Target.