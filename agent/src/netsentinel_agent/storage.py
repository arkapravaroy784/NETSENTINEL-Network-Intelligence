import json, sqlite3
from pathlib import Path
class Store:
 def __init__(self,path="netsentinel-agent.db"):
  self.c=sqlite3.connect(path);self.c.execute("CREATE TABLE IF NOT EXISTS queue(id INTEGER PRIMARY KEY, payload TEXT UNIQUE, state TEXT DEFAULT 'PENDING', retries INTEGER DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP, last_attempt TEXT)");self.c.commit()
 def add(self,payload):self.c.execute("INSERT OR IGNORE INTO queue(payload) VALUES(?)",(json.dumps(payload,default=str),));self.c.commit()
 def pending(self,limit=100):return self.c.execute("SELECT id,payload FROM queue WHERE state IN ('PENDING','FAILED') AND retries<5 ORDER BY id LIMIT ?",(limit,)).fetchall()
 def sent(self,id):self.c.execute("UPDATE queue SET state='UPLOADED' WHERE id=?",(id,));self.c.commit()
 def failed(self,id):self.c.execute("UPDATE queue SET state='FAILED', retries=retries+1,last_attempt=CURRENT_TIMESTAMP WHERE id=?",(id,));self.c.commit()
