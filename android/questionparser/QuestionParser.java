package questionparser;

import java.util.Dictionary;
import java.util.Enumeration;
import java.util.LinkedList;
import java.util.List;

public class QuestionParser {
    private static Dictionary<String, Dictionary<String, Integer>> patternDict = QuestionWordGenerator.QUESTION_WORDS;

    public static List<String> phraseSplit(String phrase) {
        String[] words = phrase.split("\\s");
        Dictionary offset = patternDict.get(words[0]);
        int numOffset = 0;
        for(int i=1;i < words.length;i++) {
            if(patternDict.get(words[i]) != null) {
                numOffset = ((int) offset.get(words[i])) + i + 2;
                break;
            }
        }
        String invocationPhrase = "";
        String listPhrase = "";
        for(int i=0;i < words.length;i++) {
            if(i < numOffset) {
                invocationPhrase += words[i] + " ";
            }
            else {
                listPhrase += words[i] + " ";
            }
        }
        invocationPhrase = invocationPhrase.substring(0, invocationPhrase.length() - 1);
        listPhrase = listPhrase.substring(0, listPhrase.length() - 1);
        List<String> splitPhrases = new LinkedList<>();
        splitPhrases.add(invocationPhrase);
        splitPhrases.add(listPhrase);
        return splitPhrases;
    }

    public static boolean questionClassifier(String phrase) {
        String[] words = phrase.split("\\s");
        for(int i=0;i < words.length;i++) {
            if(words[i].equals("or")) {
                Enumeration<String> keys = patternDict.keys();
                for(int j=0; j < words.length;j++) {
                    while(keys.hasMoreElements()) {
                        String key = keys.nextElement();
                        if(key.equals(words[j])) {
                            return true;
                        }
                    }
                }
            }
        }
        return false;
    }
}
