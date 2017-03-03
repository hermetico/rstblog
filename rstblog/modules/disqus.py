# -*- coding: utf-8 -*-
"""
    rstblog.modules.disqus
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements disqus element if asked for.
    
    To use this, include ``disqus`` in the list of modules in your ``config.yml`` file,
    and add a configuration variable to match your settings : ``disqus.shortname`` 
    
    To set developer mode on the site, set ``disqus.developer=1`` in your ``config.yml`` file.
    
    To prevent comments on a particular page, set ``disqus = no`` in the page's YAML preamble.

    :copyright: (c) 2012 by Martin Andrews.
    :license: BSD, see LICENSE for more details.
"""
import jinja2

disqus_txt = """
<div id="disqus_thread"></div>
<script>

var title = document.title.split('-');
title = title[title.length - 1].trim();

var disqus_config = function () {
    this.page.url = document.location.origin + document.location.pathname;
    this.page.identifier = '%(identifier)s';
    this.page.title = '%(title)s';
};

var shortname = '%(short_name)s';

var disqus_developer = %(developer)i;
(function() {
var d = document, s = d.createElement('script');
s.src = '//' + shortname + '.disqus.com/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>

<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
"""


@jinja2.contextfunction
def get_disqus(context, title, identifier):

    # when module enabled, it is shown by default unless its requested not to within the header with ->  discus: no
    if context['config'].get('disqus', True):
        short_name = context['builder'].config.root_get('modules.disqus.shortname', 'YOUR-DISQUS-SHORTNAME')
        developer = context['builder'].config.root_get('modules.disqus.developer', 0)

        response = disqus_txt % dict(title=title, identifier=identifier, short_name=short_name, developer=developer)
    else:
        response = ''

    return jinja2.Markup(response.encode('utf-8'))


def setup(builder):
    builder.jinja_env.globals['get_disqus'] = get_disqus
