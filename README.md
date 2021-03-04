# Discord_Trello_Bot

So, this time I decided to create a discord bot that can get information of card in Trello to send a message In our channel.
Rapidly, we are in engineering school and we work every night. I thought It was a good Idea to automatise some things.
Every day we add card on Trello to say what we'll work. I wanted a Bot capable to get informations of these cards and send
us the day, the name and what we have to work. Plus, we don't have to add a date by ourselves, the program will set the
due date one day per one day everytime we add a card (just, we must create cards day by day)

# You can totally use it

You just have to create a Bot, create a file that fills some informations :
```py
client = TrelloClient(
    api_key=trello_secret.api_key,
    api_secret=trello_secret.api_secret,
    token=trello_secret.token,
    token_secret=trello_secret.token_secret
)

client.run(discord_secret.token)
```

I used this module : https://pypi.org/project/py-trello/  

# Others features

> Simple code to delete message on channel "!d"

# Futurs features

> Add !archive to archive the first card in the list ✔️  
> Add a card with a command on discord ❌  
> Music bot with (like Groovy) ❌  
> Scrapping of our school website (like agenda...) ❌  

## Me and programming langages (progression)
- *01/03/2021* 

| VHDL                        | Python                      | C                           |
|-----------------------------|-----------------------------|-----------------------------|
|  ➖🚀➖➖➖➖➖➖➖🌑  |  ➖➖➖➖➖➖🚀➖➖🌑  |  ➖➖➖➖🚀➖➖➖➖🌑  |
