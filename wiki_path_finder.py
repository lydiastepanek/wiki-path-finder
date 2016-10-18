from lxml import html
import requests

# working now
#/wiki/Tax
# /wiki/Bolivia (holy shit!)
#^ has an empty first paragraph which i solved for
# wiki/Sea_of_Galilee
# ^ these are in perens and i cant solve it
# /wiki/Greek_language
# # well this is the right logic just a double () perenthesis which is wrong
#/wiki/Finn_McLaine
# #Mike_Milligan but i need a non # one

body_text_selector = '//div[@id="bodyContent"]/div[@id="mw-content-text"]/'

def surrounded_by_perentheses(text_of_link, main_text):
  index_of_link = main_text.find(text_of_link)
  main_text_after_link = main_text[index_of_link:]
  index_of_first_open_perenthesis_after_link = main_text_after_link.find('(')
  index_of_first_closed_perenthesis_after_link = main_text_after_link.find(')')
  return index_of_first_open_perenthesis_after_link > index_of_first_closed_perenthesis_after_link

def find_link(tree):
    content_paragraph_links = tree.xpath(body_text_selector + 'p/a/@href[1]')
    content_paragraph_texts_of_links = tree.xpath(body_text_selector + 'p/a//text()')
    print content_paragraph_texts_of_links and content_paragraph_links
    if not content_paragraph_texts_of_links or not content_paragraph_links:
      return None
    main_text = ''.join(tree.xpath(body_text_selector + 'p//text()'))
    link_idx = 0
    link = None
    while not link:
      text_of_link = content_paragraph_texts_of_links[link_idx]
      link_candidate = content_paragraph_links[link_idx]
      if (link_candidate[0] == "/" and not
          surrounded_by_perentheses(text_of_link, main_text) and
          link_candidate.find('redlink=1') == -1):
        link = link_candidate
      link_idx += 1
    return link

page = requests.get('https://en.wikipedia.org/wiki/Conceptualisation')
tree = html.fromstring(page.content)
print find_link(tree)
