
import re
import urllib
from BeautifulSoup import BeautifulSoup, NavigableString, BeautifulStoneSoup

try:
	from functions import *
except:
	from GmediaFinder.functions import *

class Mp3Realm(object):
    def __init__(self,gui):
        self.gui = gui
        self.name="Mp3Realm"
        self.current_page = 1
        self.main_start_page = 1
        self.search_url = "http://mp3realm.org/search?q=%s&bitrate=&dur=0&pp=50&page=%s"
        self.start_engine()


    def start_engine(self):
		self.gui.engine_list[self.name] = ''

    def load_gui(self):
		pass

    def search(self, query, page):
        print self.search_url % (urllib.quote(query), self.current_page)
        data = get_url_data(self.search_url % (urllib.quote(query), self.current_page))
        return self.filter(data,query)
        
    def filter(self,data,user_search):
		soup = BeautifulStoneSoup(data.decode('utf-8'),selfClosingTags=['/>'])
		## reset the treeview
		nlist = []
		link_list = []
		files_count = None
		try:
			#search results div
			files_count = soup.findAll('div',attrs={'id':'searchstat'})[0].findAll('strong')[1].string
			if self.current_page != 1:
				self.gui.pageback_btn.show()
			else:
				self.gui.pageback_btn.hide()
		except:
			#self.gui.informations_label.set_text(_("no results found for %s...") % (user_search))
			self.gui.changepage_btn.hide()
			return
		
		values = {'query': user_search, 'total' : files_count}
		#self.gui.informations_label.set_text(_("%(total)s files found for %(query)s...") % values)
		if re.search(r'(\S*Aucuns resultats)', soup.__str__()):
			self.gui.changepage_btn.hide()
			self.current_page = 1
			#self.gui.informations_label.set_text(_("no results found for %s...") % (user_search))
			return
		else:
			values = {'page': self.current_page, 'query': user_search, 'total' : files_count}
			#self.gui.informations_label.set_text(_("Results page %(page)s for %(query)s...(%(total)s results)") % values)

		self.gui.changepage_btn.show()
		
		flist = re.findall('(http://.*\S\.mp3|\.mp4|\.ogg|\.aac|\.wav|\.wma)', data.lower())
		for link in flist:
			if re.match('http://\'\+this', link) :
				continue
			try:
				link = urllib2.unquote(link)
				name = urllib2.unquote(os.path.basename(link.decode('UTF8')))
				nlist.append(name)
				link_list.append(link)
			except:
				continue
		## add to the treeview if ok
		i = 0
		for name in nlist:
			if name and link_list[i]:
				markup="<small><b>%s</b></small>" % name
				self.gui.add_sound(name, markup, link_list[i])
				i += 1


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
				    self.gui.add_sound(name, link_list[i])
				    i += 1
				except:
					continue

