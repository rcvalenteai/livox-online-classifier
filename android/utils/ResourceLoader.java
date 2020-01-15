package utils;

import java.util.Dictionary;
import java.util.Hashtable;

public class ResourceLoader {
    private static Dictionary loadDict(String filename) {
        // TODO: android loading local resources for vocabulary
        Dictionary jsonDict = new Hashtable();
        return jsonDict;
    }

    private static Dictionary downloadDict(String url) {
        // TODO: android downloading cloud resources for vocabulary
        Dictionary internetJsonDict = new Hashtable();
        return internetJsonDict;
    }

    public static Dictionary initializeResource(String filename, String url) {
        // TODO: correct exception handling for android
        Dictionary resourceDict = null;
        try {
            resourceDict = loadDict(filename);
        } catch (Exception e) {
            resourceDict = downloadDict(url);
        }
        return resourceDict;
    }
}
