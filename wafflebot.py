### Programmed by Erik Fredericks
### Initially started as a research project, turned into something so much more.

### Wafflebot.  Posts the immortal gif of Olli Jokinen whenever a user requests to be 
### waffled.

import time,datetime
import praw
import mysql.connector as mariadb
import sys

# Setup a database class for easy access

# Intended schema is fairly simple:
# | id (auto int) | comment id | timestamp
class DBO(object):
  def __init__(self, user, passwd, db, table):
    self.__user   = user
    self.__passwd = passwd
    self.__db     = db
    self.__table  = table
    self.__conn   = self.initConn()
    
 
  # Initialize connection to local database
  def initConn(self):
    try:
      return mariadb.connect(user=self.__user, password=self.__passwd, database=self.__db)
    except: # die on database failure
      print "Error connecting to database."
      sys.exit()

  # Insert a new comment record
  def addWaffle(self, cid, ts):
    cursor = self.__conn.cursor(buffered=True)
    query = "INSERT INTO %s (comment_id, timestamp) VALUES ('%s', '%s')" % (self.__table, cid, ts)
    cursor.execute(query)
    self.__conn.commit()
    cursor.close()

    cnt = self.getCount()
    return cnt

  # Get count of all wafflings
  def getCount(self):
    cursor = self.__conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM %s" % self.__table)
    num_rows = cursor.rowcount
    cursor.close()
    return num_rows

  # Check if waffling exists
  def checkWaffle(self,cid):
    cursor = self.__conn.cursor(buffered=True)
    cursor.execute("SELECT id FROM %s WHERE (comment_id = '%s')" % (self.__table, cid))
    num_rows = cursor.rowcount
    cursor.close()

    if (num_rows == 0): # no comment previously found, allow insert
      return False
    else: # comment found, skip
      return True

# Build the reply string
def build_reply(t, num):
  imglink  = 'https://media3.giphy.com/media/ft4AUgOZ45YJO/200.gif'
  endtxt = "^[dev](https://github.com/efredericks/wafflebot) ^| ^[contact](https://www.reddit.com/message/compose?to=waffleme_bot&subject=Feedback)"
  reply  = ''

  if (t == 'new'):
    reply   = "[You've been automatically waffled.](%s)\n\n^(I'm a bot. beep bleep doop.  To summon me via comments use !waffleme | )%s" % (imglink,endtxt)
  else:
    reply    = "[You've been waffled.](%s)\n\n^(I'm a bot.  beep beep boop. | )%s" % (imglink,endtxt)
  reply += "\n\n^(%d waffles have been served since this bot's inception.)" % num
  return reply
  
# Main function
if __name__ == "__main__":
  # Setup trigger words 
  botname  = '<BOT NAME>'
  triggers = ['ollijokinen', 'olli jokinen', 'jokinen', '!waffleme']
  
  # Connect to Reddit via 'main' config entry
  r  = praw.Reddit('main', user_agent='WaffleBot')
  sr = r.subreddit('<subreddit1>+<subreddit2>')

  # Get database connection
  dbo = DBO('<DB USER>','<DB PASSWORD>','<DB>','<TABLE>')

  # Continually scan comments for triggers
  for comment in sr.stream.comments():
    parsed_body = comment.body.lower()
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%y-%m-%d %H:%M:%S')

    # Summoned via !waffleme
    if ((triggers[-1] in parsed_body) and (comment.author != botname) and (not dbo.checkWaffle(comment))):
      try:
        print '[%s] Replying to [%s] on comment ID [%s]' % (ts,comment.author,comment)
        cnt = dbo.addWaffle(comment,ts)
        comment.reply(build_reply('normal', cnt))
      except:
        print "Comments probably locked on %s" % comment
    else:
      # Summoned by the utterance of our dear leader's name
      for trigger in triggers[:3]:
        if ((trigger in parsed_body) and (not dbo.checkWaffle(comment))):
          try: 
            print '[%s] New instance: replying to [%s] on comment ID [%s]' % (ts,comment.author,comment)
            cnt = dbo.addWaffle(comment,ts)
            comment.reply(build_reply('new', cnt))
          except:
            print "Comments probably locked on %s" % comment
          break
