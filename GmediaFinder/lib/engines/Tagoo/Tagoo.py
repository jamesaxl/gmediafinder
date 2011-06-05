
import re
import urllib
from BeautifulSoup import BeautifulSoup, NavigableString, BeautifulStoneSoup

try:
	from functions import *
except:
	from GmediaFinder.functions import *
	
class Tagoo(object):
    def __init__(self,gui):
        self.gui = gui
        self.current_page = 1
        self.main_start_page = 1
        self.name="Tagoo"
        self.search_url = "http://tagoo.ru/en/search.php?for=audio&search=%s&page=%d&sort=date"
        self.start_engine()


    def start_engine(self):
		self.gui.engine_list[self.name] = ''

    def load_gui(self):
		pass

    def search(self, query, page):
        data = get_url_data(self.search_url % (urllib.quote(query), self.current_page))
        return self.filter(data,query)
        
    def filter(self,data,user_search):
		soup = BeautifulStoneSoup(data.decode('utf-8'),selfClosingTags=['/>'])
		nlist = []
		link_list = []
		next_page = 1
		results_div = soup.find('div',attrs={'class':'resultinfo'})
		try:
			results_count = re.search('Found about (\d+)', str(results_div)).group(1)
		except:
			self.gui.changepage_btn.hide()
			#self.gui.informations_label.set_text(_("No results found for %s...") % (user_search))
			return
		if results_count == 0 :
			#self.gui.informations_label.set_text(_("no results for your search : %s ") % (user_search))
			return
		else:
			values = {'total': results_count, 'query': user_search}
			#self.gui.informations_label.set_text(_("%(total)s results found for your search %(query)s") % values)
			self.gui.changepage_btn.set_sensitive(1)
		try:
		    pagination_table = soup.findAll('div',attrs={'class':'pages'})[0]
		except:
			return
		if pagination_table:
			next_check = pagination_table.findAll('a')
			for a in next_check:
				l = str(a.string)
				if l == "Next":
					next_page = 1
			if next_page:
				values = {'page': self.current_page, 'query': user_search, 'total' : results_count}
				#self.gui.informations_label.set_text(_("Results page %(page)s for %(query)s...(%(total)s results)") % values)
				if self.current_page != 1:
					self.gui.pageback_btn.show()
				else:
					self.gui.pageback_btn.hide()
				self.gui.changepage_btn.show()
			else:
				self.gui.changepage_btn.hide()
				self.current_page = 1
				#self.gui.informations_label.set_text(_("no more files found for %s...") % (user_search))
				return

		flist = [ each.get('href') for each in soup.findAll('a',attrs={'class':'link'}) ]
		for link in flist:
			try:
				link = urllib2.unquote(link)
				name = urllib2.unquote(os.path.basename(link.decode('utf-8')))
				nlist.append(name)
				link_list.append(link)
			except:
				continue
		## add to the treeview if ok
		i = 0
		for name in nlist:
			if name and link_list[i]:
				try:
					markup="<small><b>%s</b></small>" % name
					self.gui.add_sound(name, markup, link_list[i])
					i += 1
				except:
					continue

