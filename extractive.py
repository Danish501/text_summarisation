import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def summarizer(rawdocs):
    stop_words = list(STOP_WORDS)
    try:
      nlp = spacy.load("en_core_web_sm")
    except OSError:
    # If the model is not installed, download it
      import subprocess
      subprocess.call("python -m spacy download en_core_web_sm", shell=True)
      nlp = spacy.load("en_core_web_sm")

    doc = nlp(rawdocs)

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stop_words and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]
    sent_score = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text]
                else:
                    sent_score[sent] += word_freq[word.text]

    select_len = int(0.3 * len(sent_tokens))
    summary = nlargest(select_len, sent_score, key=sent_score.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return doc, summary, len(rawdocs.split(' ')), len(summary.split(' '))
# text="The sun peeked through the dense foliage, casting dappled shadows on the forest floor. Birds chirped melodiously, their vibrant feathers contrasting with the lush greenery. A gentle breeze rustled the leaves, creating a soothing symphony of nature's whispers. The scent of wildflowers filled the air, as if nature itself had woven a tapestry of fragrances. It was a serene moment, where time seemed to stand still, and one could truly immerse themselves in the tranquil beauty of the natural world."
# a,b,c,d=summarizer(text)
# print(b)
