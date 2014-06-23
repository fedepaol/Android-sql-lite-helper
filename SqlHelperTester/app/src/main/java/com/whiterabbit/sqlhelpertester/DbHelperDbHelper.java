/**********************************************************************************************************************************************************************
****** AUTO GENERATED FILE BY ANDROID SQLITE HELPER SCRIPT BY FEDERICO PAOLINELLI. ANY CHANGE WILL BE WIPED OUT IF THE SCRIPT IS PROCESSED AGAIN. *******
**********************************************************************************************************************************************************************/
package com.whiterabbit.sqlhelpertester;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.util.Log;

import java.util.Date;

public class DbHelperDbHelper {
    private static final String TAG = "DbHelper";

    private static final String DATABASE_NAME = "DbHelper.db";
    private static final int DATABASE_VERSION = 5;


    // Variable to hold the database instance
    protected SQLiteDatabase mDb;
    // Context of the application using the database.
    private final Context mContext;
    // Database open/upgrade helper
    private DbHelper mDbHelper;
    
    public DbHelperDbHelper(Context context) {
        mContext = context;
        mDbHelper = new DbHelper(mContext, DATABASE_NAME, null, DATABASE_VERSION);
    }
    
    public DbHelperDbHelper open() throws SQLException { 
        mDb = mDbHelper.getWritableDatabase();
        return this;
    }
                                                     
    public void close() {
        mDb.close();
    }

    public static final String ROW_ID = "_id";

    
    // -------------- EVENT DEFINITIONS ------------
    public static final String EVENT_TABLE = "Event";
    
    public static final String EVENT_DESCRIPTION_COLUMN = "Description";
    public static final int EVENT_DESCRIPTION_COLUMN_POSITION = 1;
    
    public static final String EVENT_TIME_COLUMN = "Time";
    public static final int EVENT_TIME_COLUMN_POSITION = 2;
    
    public static final String EVENT_SHORTDESC_COLUMN = "ShortDesc";
    public static final int EVENT_SHORTDESC_COLUMN_POSITION = 3;
    
    
    // -------------- CALL DEFINITIONS ------------
    public static final String CALL_TABLE = "Call";
    
    public static final String CALL_NUMBER_COLUMN = "Number";
    public static final int CALL_NUMBER_COLUMN_POSITION = 1;
    
    public static final String CALL_TIME_COLUMN = "Time";
    public static final int CALL_TIME_COLUMN_POSITION = 2;
    
    public static final String CALL_VALUE_COLUMN = "value";
    public static final int CALL_VALUE_COLUMN_POSITION = 3;
    
    public static final String CALL_LONGNUMBER_COLUMN = "longnumber";
    public static final int CALL_LONGNUMBER_COLUMN_POSITION = 4;
    
    


    // -------- TABLES CREATION ----------

    
    // Event CREATION 
    private static final String DATABASE_EVENT_CREATE = "create table " + EVENT_TABLE + " (" +
                                "_id integer primary key autoincrement, " +
                                EVENT_DESCRIPTION_COLUMN + " text, " +
                                EVENT_TIME_COLUMN + " integer, " +
                                EVENT_SHORTDESC_COLUMN + " text" +
                                ")";
    
    // Call CREATION 
    private static final String DATABASE_CALL_CREATE = "create table " + CALL_TABLE + " (" +
                                "_id integer primary key autoincrement, " +
                                CALL_NUMBER_COLUMN + " text, " +
                                CALL_TIME_COLUMN + " integer, " +
                                CALL_VALUE_COLUMN + " float, " +
                                CALL_LONGNUMBER_COLUMN + " integer" +
                                ")";
    

    
    // ----------------Event HELPERS -------------------- 
    public long addEvent (String Description, Date Time, String ShortDesc) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(EVENT_DESCRIPTION_COLUMN, Description);
        contentValues.put(EVENT_TIME_COLUMN, Time.getTime());
        contentValues.put(EVENT_SHORTDESC_COLUMN, ShortDesc);
        return mDb.insert(EVENT_TABLE, null, contentValues);
    }

    public long updateEvent (long rowIndex,String Description, Date Time, String ShortDesc) {
        String where = ROW_ID + " = " + rowIndex;
        ContentValues contentValues = new ContentValues();
        contentValues.put(EVENT_DESCRIPTION_COLUMN, Description);
        contentValues.put(EVENT_TIME_COLUMN, Time.getTime());
        contentValues.put(EVENT_SHORTDESC_COLUMN, ShortDesc);
        return mDb.update(EVENT_TABLE, contentValues, where, null);
    }

    public boolean removeEvent(long rowIndex){
        return mDb.delete(EVENT_TABLE, ROW_ID + " = " + rowIndex, null) > 0;
    }

    public boolean removeAllEvent(){
        return mDb.delete(EVENT_TABLE, null, null) > 0;
    }

    public Cursor getAllEvent(){
    	return mDb.query(EVENT_TABLE, new String[] {
                         ROW_ID,
                         EVENT_DESCRIPTION_COLUMN,
                         EVENT_TIME_COLUMN,
                         EVENT_SHORTDESC_COLUMN
                         }, null, null, null, null, null);
    }

    public Cursor getEvent(long rowIndex) {
        Cursor res = mDb.query(EVENT_TABLE, new String[] {
                                ROW_ID,
                                EVENT_DESCRIPTION_COLUMN,
                                EVENT_TIME_COLUMN,
                                EVENT_SHORTDESC_COLUMN
                                }, ROW_ID + " = " + rowIndex, null, null, null, null);

        if(res != null){
            res.moveToFirst();
        }
        return res;
    }
    
    // ----------------Call HELPERS -------------------- 
    public long addCall (String Number, Date Time, Float value, long longnumber) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(CALL_NUMBER_COLUMN, Number);
        contentValues.put(CALL_TIME_COLUMN, Time.getTime());
        contentValues.put(CALL_VALUE_COLUMN, value);
        contentValues.put(CALL_LONGNUMBER_COLUMN, longnumber);
        return mDb.insert(CALL_TABLE, null, contentValues);
    }

    public long updateCall (long rowIndex,String Number, Date Time, Float value, long longnumber) {
        String where = ROW_ID + " = " + rowIndex;
        ContentValues contentValues = new ContentValues();
        contentValues.put(CALL_NUMBER_COLUMN, Number);
        contentValues.put(CALL_TIME_COLUMN, Time.getTime());
        contentValues.put(CALL_VALUE_COLUMN, value);
        contentValues.put(CALL_LONGNUMBER_COLUMN, longnumber);
        return mDb.update(CALL_TABLE, contentValues, where, null);
    }

    public boolean removeCall(long rowIndex){
        return mDb.delete(CALL_TABLE, ROW_ID + " = " + rowIndex, null) > 0;
    }

    public boolean removeAllCall(){
        return mDb.delete(CALL_TABLE, null, null) > 0;
    }

    public Cursor getAllCall(){
    	return mDb.query(CALL_TABLE, new String[] {
                         ROW_ID,
                         CALL_NUMBER_COLUMN,
                         CALL_TIME_COLUMN,
                         CALL_VALUE_COLUMN,
                         CALL_LONGNUMBER_COLUMN
                         }, null, null, null, null, null);
    }

    public Cursor getCall(long rowIndex) {
        Cursor res = mDb.query(CALL_TABLE, new String[] {
                                ROW_ID,
                                CALL_NUMBER_COLUMN,
                                CALL_TIME_COLUMN,
                                CALL_VALUE_COLUMN,
                                CALL_LONGNUMBER_COLUMN
                                }, ROW_ID + " = " + rowIndex, null, null, null, null);

        if(res != null){
            res.moveToFirst();
        }
        return res;
    }
    

    private static class DbHelper extends SQLiteOpenHelper {
        public DbHelper(Context context, String name, CursorFactory factory, int version) {
            super(context, name, factory, version);
        }

        // Called when no database exists in disk and the helper class needs
        // to create a new one. 
        @Override
        public void onCreate(SQLiteDatabase db) {      
            db.execSQL(DATABASE_EVENT_CREATE);
            db.execSQL(DATABASE_CALL_CREATE);
            
        }

        // Called when there is a database version mismatch meaning that the version
        // of the database on disk needs to be upgraded to the current version.
        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            // Log the version upgrade.
            Log.w(TAG, "Upgrading from version " + 
                        oldVersion + " to " +
                        newVersion + ", which will destroy all old data");
            
            // Upgrade the existing database to conform to the new version. Multiple 
            // previous versions can be handled by comparing _oldVersion and _newVersion
            // values.

            // The simplest case is to drop the old table and create a new one.
            db.execSQL("DROP TABLE IF EXISTS " + EVENT_TABLE + ";");
            db.execSQL("DROP TABLE IF EXISTS " + CALL_TABLE + ";");
            
            // Create a new one.
            onCreate(db);
        }
    }
}

