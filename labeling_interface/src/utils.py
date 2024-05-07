class Text:
    def __init__(self, t_id, text):
        self.rating = 1200
        self.num_matches = 0
        self.t_id = t_id
        self.text = text
        
    def set_rating(self, rating):
        self.rating = rating
    
    def get_rating(self):
        return self.rating

    def increment_num_matches(self):
        self.num_matches +=1
    
    def get_num_matches(self):
        return self.num_matches

    def get_t_id(self):
        return self.t_id

    def get_text(self):
        return self.text

    def __str__(self):
        return f"ID:\t{self.t_id} \n RATING:\t{self.rating}\n MATCHES:\t{self.num_matches}\n TEXT:\t {self.text}"


def _exspected_score(rating_1, rating_2):
    e_1 = 1 / (1 + 10**((rating_2-rating_1)/400))
    return e_1

def _update_score(rating, s, e, k=16):
    rating_p = rating + k*(s-e)
    return rating_p

def handle_scores(t1, t2):
    #t1 is expected to be the winner
    #Update score according to the elo algorithm

    t1.increment_num_matches()
    t2.increment_num_matches()

    e1 = _exspected_score(t1.get_rating(), t2.get_rating())
    e2 = 1-e1

    t1.set_rating(_update_score(t1.get_rating(), 1, e1))
    t2.set_rating(_update_score(t2.get_rating(), 0, e2))

def apply_history(history, texts):

    for _, val in history.items():
        cands = val[0]
        winner = val[1]
        loser = sum(cands)-winner
        
        handle_scores(texts[winner], texts[loser])


