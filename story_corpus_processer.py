import nltk
from collections import Counter


STORY_CORPUS = "story_corpus.txt"
STORY_SEP = "=="
SYSTEM_SEP = "===="

DATASET = "wikilarge"


def parse_data(file_loc):
    """ Reads in the corpus in file_loc, strips story and system
    separators and returns a list of lines, each containing one
    paragraph of story text.
    """
    print("reading in: " + file_loc)
    with open(file_loc) as f:
        lines = f.readlines()

    # remove story and system separators
    return [l for l in lines if not
            (l.startswith(STORY_SEP) or l.startswith(SYSTEM_SEP))]


def tokenize(lines):
    """ For each sentence in `line` this method performs
    word tokenization and replaces brackets as well as
    quotation marks with unified symbols as employed by
    the appropirate training corpus.
    """
    print("Tokenizing " + str(len(lines)) + " lines...")
    tokenized_lines = []
    for l in lines:
        tokenized_lines.append(nltk.word_tokenize(l))
    return [" ".join(_fix_q_marks_and_brackets(l)) for l in tokenized_lines]


def save_data(lines, filename):
    """ Saves each element in `lines` into a file `filename`, separated by
    newlines.
    """
    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")


def split_in_sentences(lines):
    """ Performs sentence tokenization. """
    text = " ".join(lines)
    return nltk.tokenize.sent_tokenize(text)


def create_sent_pairs(lines):
    """ Takes a list of sentences and creates a list of tuples,
    where each tuple consists of two subsequent sentences in `lines`.
    Each sentence is contained in exactly one tuple (no overlapping).
    """
    tup_lines = []
    for sen1, sen2 in _iterate_pairs(lines):
        tup_lines.append(sen1 + " " + sen2)
    return tup_lines


def ne_anonymization(lines):
    """ For each sentence in lines, this methods identifies named entities
    anonymizes them by replacing each occurence with a placeholder of form
    CATEGORY@NUM, where CTAGEORY stands for the type of ne, and NUM is the
    ordinal number of this entity regarding this sentence (NOT the whole
    corpus). Returns a list of sentences.
    """
    new_lines = []
    for sent in lines:
        new_sent = []
        tag_counter = Counter()
        tag_dict = {}
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                entity = chunk[0][0].lower()
                ner_tag = chunk.label()
                if ner_tag == "GPE":
                    ner_tag = "LOCATION"

                if entity+ner_tag not in tag_dict.keys():
                    tag_counter[ner_tag] += 1
                    tag_dict[entity+ner_tag] = tag_counter[ner_tag]
                new_sent.append(ner_tag + "@" + str(tag_dict[entity+ner_tag]))
            else:
                new_sent.append(chunk[0])
                assert len(chunk) == 2
        new_lines.append(" ".join(new_sent))

    return new_lines


def deunk(orig_loc, generated_loc, safe_loc):
    """ Removes <unk> words from text generated by a textual embellishment system,
    by replacing them with the words at the same position in the file that was
    used as input to the embellishment system.

    Takes as input the location of a file generated by an embellishment system,
    the location of the file that was used as input for the embellishment
    system, as well as the location of an output file.
    """
    with open(orig_loc, "r") as f:
        orig_lines = f.readlines()

    with open("generated_loc", "r") as f:
        gen_lines = f.readlines()

    gen_lines_deunked = []
    for i, line in enumerate(gen_lines):
        gen_line_list = line.split(" ")
        orig_line_list = orig_lines[i].split(" ")

        # print(gen_line_list)
        for j, word in enumerate(gen_line_list):
            if word == "<unk>":
                gen_line_list[j] = orig_line_list[j]

        gen_lines_deunked.append(" ".join(gen_line_list))

    with open(safe_loc, "w") as f:
        f.writelines(gen_lines_deunked)

    count, same = 0, 0
    for i, line in enumerate(gen_lines_deunked):
        count += 1
        if line == orig_lines[i]:
            same += 1

    print("Correct reproduction: " + str(same) + "/" + str(count) + " = "
          + str(same/float(count)))


def _fix_q_marks_and_brackets(line):
    line = [l.replace("(", "-LRB-").replace(")", "-RRB-") for l in line]

    if DATASET == "docaligned":
        return line
    if DATASET == "wikilarge":
        return [l.replace("``", "''").replace("''", "''") for l in line]


def _iterate_pairs(l):
    pairs = list(zip(l, l[1:]))[::2]
    if (len(l) % 2 == 1):
        # if l has uneven number of elements, zip ignores the (unpaired)
        # last one
        pairs.append((l[-1], ""))
    return pairs


DATASET = "wikilarge"

lines = parse_data(STORY_CORPUS)

if DATASET == "wikilarge":
    lines = split_in_sentences(lines)
    lines = tokenize(lines)
    lines = create_sent_pairs(lines)
    lines = ne_anonymization(lines)

    save_data(lines, "story_corpus.pairs.ne.txt")
