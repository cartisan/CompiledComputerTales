# CompiledComputerTales
This is a (necessarily incomplete) corpus of stories created by computational storytelling algorithms, compiled by Leonid Berov and Kai Standvoss.
To reflect the breadth of the field of computational storytelling, it collects at most three stories from as many systems as available to us. Because it is unfeasible to manually deploy all individual systems and generate stories for this purpose, we instead opted for using stories that have been reported in scientific publications. Be advised that this runs the danger of biasing the corpus towards high-quality exemplars. The sources that have been used to extract the stories for each storytelling system are reported in the file "references.txt".

If you use this corpus in your research, kindly refer to the associated publication:<br>
<i>Berov, L., & Standvoss, K. (2018). Discourse Embellishment Using a Deep Encoder-Decoder Network</i>

## Format
The corpus is located in the file "story_corpus.txt".

The individual storytelling systems are separated by a line of the following form: `==== name of system ====`.<br>
Individual stories are separated by a line of the following form: `==`.<br>
Paragraphs inside the stories are separated by a newline symbol `\n`, which means that each line contains one paragraph of story text.

## Preprocessing
To pre-process the corpus for common recurrent neural network frameworks like tensorflow, a python script is provided in the file "story_corpus_processer.py". At the moment it supports parsing the data from the corpus, word and sentence tokenization, cleaning up special symbols, named-entity anonymization as well as sentence-pair generation (as employed in section 3.4 of the associated publication).
For post-processing the output of a neural network that performed inference on this corpus, a naive method for dealing with out-of-vocabulary tokens is
provided.

THIS SCRIPT IS PROVIDED “AS IS” AND THE DEVELOPERS MAKE NO OTHER WARRANTIES, EXPRESSED OR IMPLIED, AND HEREBY DISCLAIM ALL IMPLIED WARRANTIES.

## Content
<pre>
state   date        content
v1      05.09.18    8 storytellers, 14 stories, 45 paragraphs, 290 sentences
</pre>