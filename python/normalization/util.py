import re
from string import digits


def abbreviate(word_list):
    if word_list:
        first_letters = [word[0] for word in word_list if word]
        return "".join(first_letters)
    else:
        return None


def tokenize(section_name):
    if not section_name:
        return None
    token_list = [word.translate(None, digits) for word in section_name.split() if word.translate(None, digits)]
    if len(token_list) > 0:
        return token_list
    return None


def arena_section_name_stripper(canonical_section_name):
    numbers = NUMBERS_RE.findall(canonical_section_name)
    if len(numbers) <> 1:
        return None
    else:
        return numbers[0]


def fuzzy_section_chooser(tokens, sections):
    scored_sections = []
    for section in sections:
        score = 0
        for token in tokens:
            if token in section.name_alpha_tokens:
                score += 1
        if score > 0:
            scored_sections.add((section, score))
        print "score out of num tokens: {} / {}".format(score, len(section.name_alpha_tokens))
    sorted(scored_sections, key=lambda x: x[1])
    if len(scored_sections) > 0:
        return scored_sections[0]
    return None


NUMBERS_RE = re.compile("\d+")