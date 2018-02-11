# gold_digger_bot
### Authors: Michael Rupprecht and Troy Hu
##### NOTE: THIS MUST BE RUN WITH PYTHON 3.6+. CODED WITH 3.6.

**Description**: A reddit bot that finds chains of gilded comments and adds a comment on the end of the chain begging for gold.

**usage**: bot.py [-h] [-t] [-c CHAR_LIMIT] [-d DEPTH] [-n NUM_COMMENTS]  
		client_id client_secret user_agent username password log_file_path

**OPTIONAL ARGUMENTS**:  

[-h] = help option  
  
[-t] = top_child_of_gilded. That is, if -t is included in the command line, then we comment to the child at the end of the gilded thread that 	is the highest up if it exists. In which case, the child is necessarily not gilded. If -t is not included or the child does not exist, 		then the bot comments on the last gilded comment in a gold chain.  
  
[-c CHAR_LIMIT] = character limit for comment the bot replies to. If the comment the bot is trying to reply to exceeds the character limit, 	then it does not reply to the comment. This option is intended to limit begging to not serious comment threads. Default value is 200.  
  
[-d DEPTH] = the depth of the gold chain to look for. The bot will look for gold chains of depth DEPTH+1. Default value of DEPTH is 2. So in 	the case of the default, the value is 2, but the bot will search for gold chains of depth 3. **We still	 need to fix this minor bug.  
  
[-n NUM_COMMENTS] = This option tells the bot to search for the first NUM_COMMENTS that are gilded in /r/all. Default value is 200.  
  
**REQUIRED ARGUMENTS**:  
  
client_id = The client ID recieved from Reddit.  
  
client_secret = The client secret recieved from Reddit (OAuth).  
  
user_agent = An identifier for Reddit. The user can specify any string for this argument. Ex: "unix-windows:gold_digger_bot:v1.0"  
  
username = username of the bot account.  
  
password = password (What else would it be?).  
  
log_file_path = The path to the "commented on" log file. This log file stores which submissions the bot has already commented on and will avoid 	further commenting on those submissions. Note that this log file must exist even if it is empty before the bot runs.  


