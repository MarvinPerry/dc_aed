import os
import urlparse



# uncomment for local testing
# dbpass  = 'dbpass'
# host = '127.0.0.1'
# AED = 'AED'
# postgres = 'postgres'
# port = '5432'

googMapKey = 'AIzaSyATHC7NschEdRyTTlu5RxVWXT4YTYRPrFs'



# uncomment when pushing to heroku
# AED = 'd73vgqjq6cl4lr'
# postgres = 'gdzwpdhassdkgp'
# dbpass = 'nSbqtdY9eHHOVOGAmiHVOE_3s7'
# host = 'ec2-54-227-250-148.compute-1.amazonaws.com'
# port = '5432'




urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

AED = url.path[1:]
postgres = url.username
dbpass = url.password
host = url.hostname
port = url.port