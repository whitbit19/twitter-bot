from random import choice

def make_chains(text_string, n):

    chains = {}

    words = text_string.split()

    for i in range(len(words) - n):

        key = tuple(words[i: n + i])

        value = words[i + n]

        chains.setdefault(key, []).append(value)

    return chains


def make_first_link(chains):

    first_link = []

    caps_key = filter(lambda x: x[0][0].isupper(), chains.keys())

    start_link = choice(caps_key)

    [first_link.append(word) for word in start_link]

    next_word = choice(chains[start_link])

    first_link.append(next_word)

    return first_link


def make_text(chains, n):
    """Return text from chains."""
    # get random key to start the link
        # append into words list
        # look up key in dictionary
            # get random word within the list
            # append into words list
        # evaluate last two words in words[] to find key in dictionary

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

