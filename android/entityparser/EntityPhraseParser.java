package entityparser;

import java.util.Dictionary;
import java.util.List;
import java.util.LinkedList;
import java.util.Collections;

/**
 * Entity Phrase Parser
 *
 * Given a string of words, this class returns the most likely combination of entities,
 * including single word and compound words, interfaces through parse function
 */
public class EntityPhraseParser {
    private Dictionary STOP_WORDS = StopWords.STOP_WORDS;

    public class EntityPhrase {
        private String entityPhrase;
        private int ngramThreshold;
        private List<String> filteredEntityPhrase;

        public EntityPhrase(String entityPhrase, int ngramThreshold) {
            this.entityPhrase = entityPhrase;
            this.ngramThreshold = ngramThreshold;
            this.filteredEntityPhrase = new LinkedList<String>();;
        }

        public EntityPhrase(String entityPhrase) {
            this(entityPhrase, 2);
        }

        public void cleanEntityPhrase() {
            String cleanPhrase = this.entityPhrase.replace(" and ", "_and_");
            String[] words = cleanPhrase.split("\\s");
            for (String word: words) {
                if(STOP_WORDS.get(word) == null) {
                    filteredEntityPhrase.add(word);
                }
            }
        }

        public List<List<String>> ngrams() {
            List entityCombinations = new LinkedList<List<String>>();
            for(int i=1; i <= this.ngramThreshold;i++) {
                entityCombinations.add(this.ngramOfSize(i));
            }
            return entityCombinations;
        }

        private List<String> ngramOfSize(int ngramSize) {
            int phraseLength = filteredEntityPhrase.size();
            if (phraseLength < ngramSize) {
                ngramSize = phraseLength;
            }
            List<String>  ngrams = new LinkedList<String>();
            for(int i=0;i < (phraseLength - (ngramSize - 1));i++) {
                String entity = "";
                for(int j=0; j < ngramSize; j++) {
                    entity += this.filteredEntityPhrase.get(i + j) + " ";
                }
                entity = entity.substring(0, entity.length() - 1);
                ngrams.add(entity);
            }
            return ngrams;
        }

        private List<List<String>> entityCombinations(List<List<String>> ngrams) {
            List<List<String>> combinations = this.entityCombinationsHelper(0,
                    this.filteredEntityPhrase.size(), ngrams, new LinkedList<String>());
            return combinations;
        }

        private List<List<String>> entityCombinationsHelper(int startingPoint, int phraseLength,
                                                           List<List<String>> words, List<String> path) {
            List<List<String>> combinations = new LinkedList<List<String>>();
            if (startingPoint == phraseLength) {
                List<List<String>> return_path = new LinkedList<List<String>>();
                return_path.add(path);
                return return_path;
            }
            for(int gramCount=0; gramCount < this.ngramThreshold;gramCount++) {
                if ((startingPoint + (gramCount + 1)) <= phraseLength) {
                    List<String> newWord = new LinkedList<String>();
                    newWord.add(words.get(gramCount).get(startingPoint));
                    List<String> newPath = new LinkedList<String>();
                    newPath.addAll(path);
                    newPath.addAll(newWord);
                    List<List<String>> newCombinations = this.entityCombinationsHelper(
                            (startingPoint + (gramCount + 1)), phraseLength, words, newPath);
                    combinations.addAll(newCombinations);
                }
                else {
                    return combinations;
                }
            }
            return combinations;
        }

        public List<String> bestEntities(List<List<String>> entList) {
            List<Double> scores = new LinkedList<Double>();
            for (List<String> entities:entList) {
                double combSum = 0.0;
                for(String entity: entities) {
                    combSum += EntityScore.getNgramScore(entity);
                }
                scores.add(combSum/ (entities.size()));
            }
            int maxIndex = 0;
            double max = Double.NEGATIVE_INFINITY;
            for(int i=0; i < entList.size();i++) {
                if(scores.get(i) > max) {
                    maxIndex = i;
                    max = scores.get(i);
                }
            }
            List<String> bestComb = entList.get(maxIndex);
            for(int i=0;i < bestComb.size();i++) {
                bestComb.set(i, (bestComb.get(i).replace(" and ", "_and_")));
            }
            return bestComb;
        }



    }

    public List<String> parse(String entityPhrase, int ngramThreshold) {
        EntityPhrase phraseObject = new EntityPhrase(entityPhrase, ngramThreshold);
        phraseObject.cleanEntityPhrase();
        return phraseObject.bestEntities(phraseObject.entityCombinations(phraseObject.ngrams()));
    }

    public List<String> parse(String entityPhrase) {
        return this.parse(entityPhrase, 2);
    }

}
