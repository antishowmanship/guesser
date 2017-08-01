import re
from string import digits


NUMBERS_RE = re.compile("\d+")
STADIUM_REPLACEMENTS = {'fd': 'field'}


def abbreviate(word_list):
    """
    Turn a list of words into a string w/first letter from each word
    :param word_list: list of strings representing words
    :return: string of first char in each word in word_list
    """
    if word_list:
        first_letters = [word[0] for word in word_list if word]
        return "".join(first_letters)
    else:
        return None


def tokenize(section_name, replacements = {}):
    """
    Provided a string with zero or more words separated by spaces, convert
    to a list of word strings, while stripping out all numerical characters
    :param section_name: string, presumably representing a section name
    :param replacements: map of tokens which, if found in section_name,
    should be replaced: key is token to be replace, val is replacement.  This seems
    dangerous so should probably be used on a per-venue basis
    :return: list of strings of all words in section_name, without numerals
    """
    if not section_name:
        return None
    token_list = [word.translate(None, digits).lower() for word in section_name.split() if word.translate(None, digits)]
    if replacements and token_list:
        for index, token in enumerate(token_list):
            if token in replacements:
                token_list[index] = replacements[token]
    if len(token_list) > 0:
        return token_list
    return None


def extract_number(canonical_section_name):
    """
    Assumes that section names have a (possibly) unique number in their
    name - find the number token in a section name(if there are multiple number tokens,
    we don't know which one is unique, so we return None)
    :param canonical_section_name: string of a section_name from arena manifest
    :return: if there is a single contiguous number in input, return that number
    """
    numbers = NUMBERS_RE.findall(canonical_section_name) if canonical_section_name else []
    if len(numbers) != 1:
        return None
    else:
        return numbers[0]


def fuzzy_section_chooser(tokens, sections):
    """
    Use tokenized words from section name to guess the associated
    section based on names in a manifest.  Scores each section in sections
    list by how many tokens in token list show up anywhere in canonical
    section name.  If any section in sections gets a score >= 1, the section
    with the highest score is returned.  Otherwise, return None
    :param tokens: list of tokenized words (minus numerals)
    :param sections: list of pre-filtered section objects that we think
    may match section represented by tokens
    :return: matching section, if any
    """
    scored_sections = []
    for section in sections:
        score = 0
        for token in tokens:
            if token in section.name_alpha_tokens:
                score += 1
        if score > 0:
            scored_sections.append((section, score))
    scored_sections = sorted(scored_sections, key=lambda x: x[1], reverse=True)
    if len(scored_sections) > 0:
        return scored_sections[0][0]
    return None
