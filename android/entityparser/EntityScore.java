package entityparser;

import java.util.Dictionary;
import java.util.Hashtable;

/**
 * EntityScore
 *
 * Handles scoring of ngram entities using generated/loaded dictionary vocabulary
 */
public class EntityScore {
    // TODO: correct load
    private static Dictionary ngramVocab = new Hashtable();

    /**
     * offline scoring mechanism, references dicitonary of keys
     * @param words word to check if exists
     * @return score of word, (1 for unigram, > 1 for identified ngrams, < 1 for unidentified ngrams)
     */
    public static double getNgramScore(String words) {
        double recognizedNgramOffset = 0.10;
        double unknownNgramOffset = 0.15;
        int wordsCount = words.split("\\s").length;
        double score = 1;

        if (wordsCount > 1) {
            if (ngramVocab.get(words) != null) {
                score += (recognizedNgramOffset * wordsCount);
            }
            else {
                score += (unknownNgramOffset * wordsCount);
            }
        }
        return score;
    }
}
