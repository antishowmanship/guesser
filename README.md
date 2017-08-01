(I used Python)

I used two basic ways to simplify the matching process: dictionaries for speed, and various string transformations for section
names.  Overall this is more of a rough draft of a solution geared toward the two sample venue files; I can only assume that 
having access to a larger universe of venue manifests would invalidate parts of my solution while also allowing for a more 
general and robust approach to the problem.  My code creates a Section class, so that Section objects contain a list of 
rows (as matching row names appears to be more straightforward than section names), as well as various rule-of-thumb 
decompositions of the section names provided in the manifests.  I.e., when reading the manifest, assume there is a 
unique/semi-unique number within the name, tokenize and acronym-ize the non-numerical portions of the name.  Then the 
normalizer class can build dictionaries based on those decompositions to speed matching, at least in some cases.

Once a manifest has been loaded and we have some dictionary structures to aid in the matching process, the normalize
function is structured to look for matches in increasing order of fuzziness.  So first, based on the input section+row
name, look for an exact match within the manifest Section objects.  If an exact match isn't found, assume that there should
be a matching number between the ticket input and the manifest, and check against various decompositions to try to guess
at a match.  For example:  tokenize the input and look for any sections with a matching number that contain at least
some of the same tokens as the input; if so, assume it's a match.  Likewise, assume that the input may use some abbreviations,
and check against those.  The more assumptions you make, the more likely you are to make an incorrect match, so this
may not be a road you want to go too far down.  But finding the best threshold for how fuzzy you want to allow your
fuzzy matcher to be is always going to be somewhat subjective, if you are depending on the variability found in human-generated
inputs.

Right now the various section-matching attempts are hard-coded into the normalize function; a more adaptable solution
would be to set up each Normalizer object with an ordered list of matching functions tailored for each venue.