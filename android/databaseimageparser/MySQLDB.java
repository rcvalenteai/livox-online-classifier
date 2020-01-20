package com.example.speechclassifier.richs_layer;


import android.content.ContentValues;
import android.content.Context;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteDatabase;

import java.util.List;
import java.lang.Double;
import utils.ResourceLoader;


public class MySQLDB extends SQLiteOpenHelper {


    public static final String DATABASE_NAME = "imagelabels.db";

    public MySQLDB(Context context) {
        super(context, DATABASE_NAME, null, 1);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        this.createTableStatements(db);
        this.loadTableValues(db);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        this.dropTable(db,"Images");
        this.dropTable(db,"Labels");
        this.dropTable(db, "Tags");
        onCreate(db);

    }

    private void createTableStatements(SQLiteDatabase db) {
        db.execSQL(ResourceLoader.loadSQL("resources/sql/images.db"));
        db.execSQL(ResourceLoader.loadSQL("resources/sql/labels.db"));
        db.execSQL(ResourceLoader.loadSQL("resources/sql/tags.db"));
    }

    private void loadTableValues(SQLiteDatabase db) {
        loadImageValues(db);
        loadTagValues(db);
        loadLabelValues(db);
    }

    private void loadImageValues(SQLiteDatabase db) {
        List<List<String>> values = ResourceLoader.loadTSVList("resources/images.tsv");
        for(List<String> row: values) {
            insertImage(row.get(0), row.get(1));
        }

    }

    private void loadLabelValues(SQLiteDatabase db) {
        List<List<String>> values = ResourceLoader.loadTSVList("resources/labels.tsv");
        for(List<String> row: values) {
            insertLabel(row.get(0), row.get(1), Double.valueOf(row.get(2)));
        }
    }

    private void loadTagValues(SQLiteDatabase db) {
        List<List<String>> values = ResourceLoader.loadTSVList("resources/tags.tsv");
        for(List<String> row: values) {
            insertTag(row.get(0), row.get(1));
        }
    }



    private void insertImage(String image_id, String location) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues contentValues = new ContentValues();
        contentValues.put("image_id", image_id);
        contentValues.put("location", location);
        db.insert("images", null, contentValues);
    }

    private void insertLabel(String image_id, String label, double confidence) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues contentValues = new ContentValues();
        contentValues.put("image_id", image_id);
        contentValues.put("label", label);
        contentValues.put("confidence", confidence);
        db.insert("labels", null, contentValues);
    }

    private void insertTag(String image_id, String tag) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues contentValues = new ContentValues();
        contentValues.put("image_id", image_id);
        contentValues.put("tag", tag);
        db.insert("tags", null, contentValues);
    }

    private void dropTable(SQLiteDatabase db, String tableName) {
        String stmt =  "DROP TABLE IF EXISTS " + tableName;
        db.execSQL(stmt);
    }
}
