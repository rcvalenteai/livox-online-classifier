package entityparser;

import utils.ResourceLoader;

import java.util.Dictionary;
import java.util.Hashtable;

public class StopWords {
    //# TODO: correct load
    public static Dictionary STOP_WORDS = new Hashtable();

    public static Dictionary initializeVocabulary() {
        String filename = "./resources/stopwords.json";
        String backup_url = "www.axonbeats.com/resources/stopwords.json";
        return ResourceLoader.initializeResource(filename, backup_url);
    }
}
