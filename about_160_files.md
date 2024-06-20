# Results of 2nd Labeling Session
In the export directory, you can now find the following files:
- ARTS_only_texts_160.pkl : The texts from the second labeling session
- USERNAME-160_history.pkl files : 10 Labeling result files for each of the users, with the form  1: ((10, 79), 79, '13/06/2024, 11:44:53', {4}) >> vote id: pair, winner (more simple), timestamp (like in labeling session 1) , Vote on confidence scale: 1-3 are for left text, 4-6 for right text 
- determined_pairs_640_[A/B/C].pkl : You have been assigned to one of three groups without your knowledge. Each group had a different order for the pairs of the second round (81-160). Here, matches were made based on the ranking of the texts in a GPT-produced ranking.

  - **A** is "pairs descending order of difference of difficulty, first easiest text with hardest text, then second easiest with second hardest, etc."

  - **B** is "pairs ascending order of difference of difficulty, first text of 80th ranking with 81st ranked text, etc., last easiest text with hardest text."

  - **C** is randomized als "control"

- user_group_map.pkl : contains info on which users were assigned to which group.
- userprofiles_tagged.pkl list of user profiles, also containing the info on which group the user was assigned to.
