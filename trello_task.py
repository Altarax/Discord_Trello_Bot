# Librairies
from datetime import timedelta
import trello_secret
from trello import TrelloClient

# Trello client
client = TrelloClient(
    api_key=trello_secret.api_key,
    api_secret=trello_secret.api_secret,
    token=trello_secret.token,
    token_secret=trello_secret.token_secret
)

# Get the board we want in trello
board = client.list_boards()[-1]
work_list = board.list_lists()[0]

last_card_work_list = work_list.list_cards()[-1]
last_id = last_card_work_list.id


# Get information of the new card in trello
def get_new_card():
    global last_id, last_card_work_list

    information_list = []

    new_card = work_list.list_cards()[-1]
    id_new_card = new_card.id

    # Add the day + 1 of the last card if no date
    if not new_card.due_date:
        new_card.set_due(last_card_work_list.due_date+timedelta(days=1))
    else:
        pass

    # Verify if we get a new card
    if last_id != id_new_card:
        last_id = id_new_card
        last_card_work_list = new_card

        """
        [0] : ID,
        [1] : NAME,
        [2] : DATE,
        """

        # Save information of the new card in a list
        information_list.append(id_new_card)
        information_list.append(new_card.name)
        information_list.append(new_card.due_date)

        return information_list

    else:
        return 0
