from random import choice, seed

def make_chains(text_string, n):
    """ Return dictionary of Markov chains with input text.

    A chain consists of a key that is a tuple of n words with
    a value of a list of word(s) that follow the tuple.
    """

    chains = {}

    words = text_string.split()

    for i in range(len(words) - n):

        key = tuple(words[i: n + i])

        value = words[i + n]

        chains.setdefault(key, []).append(value)

    return chains


def make_first_link(chains):
    """Builds first link. The first link is randomly picked from a list of keys that
    begin with a capitalized word. 

    The next word is picked randomly from the value of that key/link.
    """

    first_link = []

    caps_key = filter(lambda x: x[0][0].isupper(), chains.keys())

    start_link = choice(caps_key)

    [first_link.append(word) for word in start_link]

    next_word = choice(chains[start_link])

    first_link.append(next_word)

    return first_link


def make_text(chains, n):
    """Return tweet from chains.
    
    Make first link and keep linking by checking for keys of last n words,
    grabbing random words from lists until sentence is too long for tweet or
    until the last word contains an apostrophe signifying the end of a sentence.
    """

    markov_sentence = make_first_link(chains)

    while len(markov_sentence) < 140:
        last_n_words = tuple(markov_sentence[-n:])
        if last_n_words not in chains:
            break

        last_word = choice(chains[last_n_words])

        markov_sentence.append(last_word)

        if last_word[-1] in '.!?" ':
            break

    return " ".join(markov_sentence)