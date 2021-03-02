# SurrogateTV-API-Crawlers
Here are all of my API Web Crawlers for the website Surrogate.TV. I have removed some information due to what it could reveal on the site. 

##`rawGame.py`
This script will, crawl through and provide all of the game pages on the site. 

##`after.py`
The script will take the shortIDs stored in a file and make a new file formatted as follows:
```
GameUUID|shortID
...
```

##`auto.py`
An all around script. Used for generating files that are used for a number of scripts. Takes in different arguments.

`-w` - Will do a deep dive into the users and games stored, adding more users and games as it finds them, thus making it find more users and games and so on so on. The more users you have found, the longer this will take and after a while, this isn't needed. 
`-n` - Say there is a user you know is on the site but hasn't been found by this script, you can use this to check and add a specific username to your running list. 
`-l` - Time in roughly minutes to do the following (Defaults to 1). Will look through all known games and look for *new* players who haven't been found before by checking the game's current round and the game's leaderboard.
`-t` - The number of threads utilized in different aspects of the script. Defaults to 150

##`top.py`
Will look through all known users and sort them based on website experience.

##`filter.py`
Will look through all known users and make different filter lists of users. Each list checks the usernames of the known users and if they are simialr, it ignores one of them. Output files to be used with `retention.py`

##`retention.py`
Will do a check on the hard coded user list to see if they have played A) a game in the past week and B) at least 10 games on the site. A bit of a naive approach but it provides some useful information 

##`playerLog.py`
Will look at a specific game and will give you the `endGame` state response for the given game...when it ends.