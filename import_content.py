import requests
from lxml import html,etree
import logging
import time
import sys
from model import Article

def write_batch_to_file(articles, filename="output.jsonl"):
    logging.info(f"Writing {len(articles)} articles to {filename}")
    with open(filename, 'a') as f:
        for article in articles:
            f.write(article.json() + '\n')

def browse_website():
    count_starter = 999
    prefix_url = f'https://www.vinmec.com/vie/suc-khoe-tong-quat/page_'
    articles = []
    for cnt in range(count_starter, 2,-1):
        logging.info(f'Processing Page {cnt}')
        if cnt % 5 == 0:
            write_batch_to_file(articles)
            articles = []
            time.sleep(10)
            
        url = prefix_url + str(cnt)        
        try:
            

            response = requests.get(url)
            
            if response.status_code == 200:
                
                tree = html.fromstring(response.content)
                links = tree.xpath("//a[@class='title_news_main']//@href")
                for link in links:
                    link = f'https://www.vinmec.com/{link}'
                    article = get_article(link)
                    if article:
                        articles.append(article)
            else:
                logging.error("Failed to get the webpage content, status code: {}".format(response.status_code))
        except requests.ConnectionError as e:
            logging.error("A Connection error occurred:{}".format(e))
        except requests.Timeout as e:
            logging.error("The request timed out:{}".format(e))
        except requests.RequestException as e:
            logging.error("An error occurred:{}".format(e))
        except ValueError as e:
            # The XPath expression did not match any elements in the document
            logging.error(str(e))
            
    # Flush everything out
    write_batch_to_file(articles)


def get_article(url):
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            
            tree = html.fromstring(response.content)
            title = ''.join(tree.xpath("//h1[@class='single-title single-title-line']//text()"))
            body = ''.join(tree.xpath("//div[@id='main-article']//text()"))
            tag_items = tree.xpath("//ul[@class='list-subtitle']//text()")
            tag_items = [tag_item.strip() for tag_item in tag_items if tag_item.strip()]
            result = Article(url=url,title=title, body=body, tags=tag_items)
            return result
        else:
            logging.error("Failed to get the webpage content, status code: {}".format(response.status_code))
            
    except etree.ParserError as e:
        logging.error("An error occurred while parsing the HTML: {}".format(e))
    except requests.ConnectionError as e:
        logging.error("A Connection error occurred:{}".format(e))
    except requests.Timeout as e:
        logging.error("The request timed out:{}".format(e))
    except requests.RequestException as e:
        logging.error("An error occurred:{}".format(e))
    except ValueError as e:
        # The XPath expression did not match any elements in the document
        logging.error(str(e))

if __name__ == '__main__':
    # url = "https://www.vinmec.com/vie/bai-viet/9-dau-hieu-va-trieu-chung-thieu-vitamin-b6-vi"
    # article = get_article(url)
    # print(article)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    browse_website()
    