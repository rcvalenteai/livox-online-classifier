import entityparser.EntityPhraseParser;
import questionparser.QuestionParser;

import java.util.Dictionary;
import java.util.Hashtable;
import java.util.LinkedList;
import java.util.List;

public class ListQuestionClassifier {
    EntityPhraseParser entityParser = new EntityPhraseParser();

    public Dictionary<String, String> getListImages(String phrase) {
        List<String> phrases = QuestionParser.phraseSplit(phrase);
        List<String> entities = entityParser.parse(phrases.get(1));
        Dictionary<String, String> urls = new Hashtable<String, String>();
        for(String entity: entities) {
            String url = getImage(entity);
            urls.put("entity", entity);
            urls.put("url", url);
        }
        return urls;
    }

    public boolean isQuestion(String phrase) {
        return QuestionParser.questionClassifier(phrase);
    }
}
