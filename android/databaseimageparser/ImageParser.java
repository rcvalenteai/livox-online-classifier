package databaseimageparser;

import java.util.LinkedList;
import java.util.List;

public class ImageParser {
    // TODO: proper initialization of db
    MySQLDB db = new MySQLDB();

    private String notFound(String keyword) {
        String path = "symbol00071621.png";
        try {
            path = searchImageWord(keyword.substring(0, keyword.length()));
        } catch (Exception e) {
            try {
                path = stemmed(keyword);
            } catch (Exception e2) {
                try {
                    path = translate(keyword);
                } catch (Exception e3) {
                    try {
                        path = closest(keyword);
                    } catch (Exception e4) {
                        assert true;
                    }
                }
            }
        }
        return path;
    }

    private String stemmed(String keyword) {
        // TODO: convert logic
        return "";
    }

    private String closest(String keyword) {
        // TODO: convert logic
        return "";
    }

    private String translate(String keyword) {
        // TODO: convert logic
        return "";
    }

    private List<String> searchTags(String keyword) {
        // TODO: convert logic
        return new LinkedList<String>();
    }

    private String searchImageWord(String keyword) {
        // TODO: convert logic
        return "";
    }

    public String getImage(String keyword) {
        // TODO: convert logic
        return "";
    }
}
