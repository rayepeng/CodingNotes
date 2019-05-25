from BeautifulSoup import BeautifulSoup
from jinja2 import Markup

import pygments
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_by_name

def highlight(html):
	soup = BeautifulSoup(html) #使用BeautifulSoup进行解析
	code_blocks = soup.findAll('pre')
	for block in code_blocks:
		lexer = get_lexer_by_name(block.code['class']) if block.code.has_key('class') else guess_lexer(block.text)
		try:
			code = ''.join([unicode(item.text) for item in block.contents])
			formatter = HtmlFormatter(linenos='inline', formatter)
			block.contents = [BeautifulSoup(code_hl)]
			block.name = 'div'

		except Exception as e:
			raise e
    return Markup(soup)

  