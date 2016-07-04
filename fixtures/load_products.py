from os import listdir
from lxml import html

files = listdir('../ah_data/products')

i = 0
while i < 10:
    fh = open('../ah_data/products/' + files[i], 'r')
    tree = html.fromstring(fh.read())

    for u in tree.xpath('//p[@class="unit"]'):
        print(u.text_content().rstrip())

    for p in tree.xpath('//p[@class="price"]/ins'):
        print(p.text_content())

    for tags in tree.xpath('//div[@class="product-detail__header"]/div[@class="hide"]'):
        print(tags.text_content().rstrip())

    i = i+1
