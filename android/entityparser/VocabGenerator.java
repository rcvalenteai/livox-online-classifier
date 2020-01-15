package entityparser;

import utils.ResourceLoader;

import java.util.Dictionary;

public class VocabGenerator {

    public static Dictionary initializeVocabulary() {
        String filename = "./resources/vocabulary.json";
        String backup_url = "www.axonbeats.com/resources/vocabulary.json";
        return ResourceLoader.initializeResource(filename, backup_url);
    }
}