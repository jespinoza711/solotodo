from django.db import connection, transaction
import re

class WpPost():
    
    def __init__(self):
        self.title = 'Hello World'
        self.excerpt = 'Summary of Hello World'
        self.url = 'http://www.google.cl'
        self.picture_url = 'http://www.kandar.info/wp-content/themes/corporate/images/logo.jpg'
        
    @staticmethod
    def get_latest_articles(article_count):
        cursor = connection.cursor()
        
        cursor.execute("SELECT ID, post_title, post_excerpt, post_content FROM wp_posts WHERE post_type = 'post' AND post_status = 'publish' ORDER BY post_date DESC LIMIT %d" % (article_count))
        
        latest_articles_data = cursor.fetchall()
        wp_posts = []
        
        for latest_article_data in latest_articles_data:        
            wp_post = WpPost()
            wp_post.title = latest_article_data[1]
            wp_post.excerpt = latest_article_data[2]
            wp_post.url = '/blog/?p=' + str(latest_article_data[0])
            wp_post.picture_url = re.search(r'src="(.*\....)"', latest_article_data[3]).group(1)
            
            wp_posts.append(wp_post)
        
        return wp_posts
        
    def __unicode__(self):
        return u'<br />'.join([self.title, self.excerpt, self.url, self.picture_url])
