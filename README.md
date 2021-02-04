# haiku-generator

A haiku is "a Japanese poem of seventeen syllables, in three lines of five, seven, and five, traditionally evoking images of the natural world." - Google

generateHaiku.py implements an n-gram based language model to generate original haiku.

Haiku are generated on a word by word basis. The likelihood of a word's generation is equal to the relative frequency with which that word followed the last n-1 generated words in the training set, syllable restrictions permitting. The beginnings of ideas are generated in one chunk drawing from a separate collection of (n-1)-grams that begin ideas in the training set. By default, n = 3.

In the training set, '+' and '~' are placed at before the beginnings and ends of ideas respectively. This was performed both manually and with the contained fitScript.py. The generation algorithm takes these symbols into account such that line 1 is one whole idea, then lines 2 and 3 form a second idea. Sensitivity to these characters significantly decreases the logical and grammatical inconsistency typical in n-gram based language generation.

## Usage

```python3 generateHaiku.py```

## Example Generations

rain on the screen door  
the silence of the new moon  
in the dark lighthouse  

the end of summer  
the shadow of a robin’s  
egg on cobble stones  

end of the stone step  
the sound of falling snow as  
we walk from the sky  
