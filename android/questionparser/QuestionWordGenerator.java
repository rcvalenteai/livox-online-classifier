package questionparser;

import utils.ResourceLoader;

import java.util.Dictionary;
import java.util.Hashtable;

public class QuestionWordGenerator {
    public static Dictionary<String, Dictionary<String, Integer>> QUESTION_WORDS = new Hashtable();

    public static Dictionary initializeVocabulary() {
        String filename = "./resources/questionwords.json";
        String backup_url = "www.axonbeats.com/resources/questionwords.json";
        return ResourceLoader.initializeResource(filename, backup_url);
    }
}
