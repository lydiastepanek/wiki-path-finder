from lxml import html
import re
import requests
import sys

class WikiCrawler(object) :

  final_counts = {}
  body_text_selector = '//div[@id="bodyContent"]/div[@id="mw-content-text"]/'
  path_length_distribution = {}
  url_count_cache = {}

  def run(self, number):
    for _ in xrange(number):
      page = requests.get('https://en.wikipedia.org/wiki/Special:Random')
      url = page.url.split("en.wikipedia.org")[-1]
      count = self.get_path_length(url)
      self.final_counts[url] = count
    self.create_distribution()

  def create_distribution(self):
    for link, count in self.final_counts.iteritems():
      self.path_length_distribution[count] = self.path_length_distribution.get(count, 0) + 1

  def get_path_length(self, url):
    count = 0
    temp_url_count_cache = {}
    while not url == '/wiki/Philosophy':
      if url in self.url_count_cache: # if url is in cache
        count += self.url_count_cache[url]
        break
      if url in temp_url_count_cache: # if it is going into a never ending loop
        return None
      temp_url_count_cache[url] = count
      url = self.get_next_url_in_path(url)
      if not url:
        return None
      count += 1
    temp_url_count_cache = {k: count - v for k, v in temp_url_count_cache.iteritems()}
    self.url_count_cache.update(temp_url_count_cache)
    return count

  def get_next_url_in_path(self, url):
    page = requests.get('https://en.wikipedia.org' + str(url))
    tree = html.fromstring(page.content)
    content_paragraph_links = tree.xpath(self.body_text_selector + 'p/a/@href[1]')
    content_paragraph_texts_of_links = tree.xpath(self.body_text_selector + 'p/a//text()')
    main_text = ''.join(tree.xpath(self.body_text_selector + 'p//text()'))
    if content_paragraph_texts_of_links and content_paragraph_links:
      return self.find_first_link(content_paragraph_links, content_paragraph_texts_of_links, main_text)

  def find_first_link(self, content_paragraph_links, content_paragraph_texts_of_links, main_text):
    for i in xrange(len(content_paragraph_links)):
      link_candidate_text = content_paragraph_texts_of_links[i]
      link_candidate = content_paragraph_links[i]
      if (self.link_is_valid(link_candidate) and not
          self.surrounded_by_parentheses(link_candidate_text, main_text)):
        return link_candidate

  def surrounded_by_parentheses(self, link_candidate_text, main_text):
    index_of_link = main_text.find(link_candidate_text)
    main_text_after_link = main_text[index_of_link:]
    index_of_first_open_perenthesis_after_link = main_text_after_link.find('(')
    index_of_first_closed_perenthesis_after_link = main_text_after_link.find(')')
    return index_of_first_open_perenthesis_after_link > index_of_first_closed_perenthesis_after_link

  def link_is_valid(self, link_candidate):
    return link_candidate[0] == "/" and link_candidate.find('redlink=1') == -1

crawler = WikiCrawler()
crawler.run(int(sys.argv[1]))
print "Final Path Lengths for all 500 random URLs:"
print crawler.final_counts
print "Distribution of path lengths:"
print crawler.path_length_distribution
