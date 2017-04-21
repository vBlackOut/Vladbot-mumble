from wikiapi import WikiApi
wiki = WikiApi()
wiki = WikiApi({ 'locale' : 'fr'}) # to specify your locale, 'en' is default

results = wiki.find('Barack Obama')
article = wiki.get_article(results[0])
print article.summary