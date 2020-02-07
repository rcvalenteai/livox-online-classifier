package databaseimageparser;

import java.util.LinkedList;
import java.util.List;
import java.util.Dictionary;
import android.database.sqlite.SQLiteDatabase;

public class ImageParser {
    // TODO: proper initialization of db
    MySQLDB db_open = new MySQLDB();
    SQLiteDatabase db = db_open.getReadableDatabase();


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
        // TODO: convert logic (non-essential)
        throw new Exception();
        return "";
    }

    private String closest(String keyword) {
        // TODO: convert logic (non-essential)
        throw new Exception();
        return "";
    }

    private String translate(String keyword) {
        throw new Exception();
        // TODO: convert logic (non-essential)
        return "";
    }

    private List<String> searchTags(String keyword) {
        // TODO: convert logic (non-essential)
        return new LinkedList<String>();
    }


    private Dictionary searchLabels(String keyword) {
        String stmt = "SELECT image_id, confidence FROM Labels WHERE label = ?s";
        Cursor labels_response = db.rawQuery(stmt, [keyword]);
        labels_response.moveToFirst();
        Dictionary labels = new Hashtable();
        while (!labels_response.isAfterLast())
            labels.put(labels_response.getString("image_id"), labels.getDouble("confidence"));
        }
        return labels;
    }

    private String searchImages(String image_id) {
        String stmt = "SELECT location FROM Images WHERE image_id = ?s";
        Cursor images_response = db.rawQuery(stmt, [image_id]);
        images_response.moveToFirst();
        String path = images_response.getString("location");
        return path;
    }

    private String findMaxImageID(Dictionary labels) {
    if (labels.isEmpty()) {
        throw new Exception();
    }
    // TODO: convert logic
    return ""
    }

    private String searchImageWord(String keyword) {
        Dictionary labels = searchLabels(keyword);
        LinkedList tags = searchTags(keyword);
        for(String tag: tags) {
            if (labels.get(tag) != null) {
                labels.put(tag, labels.get(tag) + 0.85);
            }
            else {
                labels.put(tag, 0.85);
            }
        }

        String path = searchImages(findMaxImageID(labels);
        return path;
    }

    public String getImage(String keyword) {
        String path = "";
        try {
            path = searchImageWord(keyword);
        } catch (Exception e5) {
            path = notFound(keyword);
        }
        path = "https://storage.googleapis.com/livox-images/full/" + path;
        return path;
    }
}
