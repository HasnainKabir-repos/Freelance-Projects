from bs4 import BeautifulSoup
with open('sample.html', 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    '''h5_tags = soup.find_all('h5')
    for tag in h5_tags:
        print(tag.text)'''

    headlines = soup.find_all('div', class_ = 'article')
    for line in headlines:
        article_name = line.h5.text
        article_headline = line.a.text.split()[0:2]

        print(f'{article_name} for {article_headline[0]} {article_headline[1]}')

