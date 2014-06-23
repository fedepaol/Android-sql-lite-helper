/**********************************************************************************************************************************************************************
****** AUTO GENERATED FILE BY ANDROID SQLITE HELPER SCRIPT BY FEDERICO PAOLINELLI. ANY CHANGE WILL BE WIPED OUT IF THE SCRIPT IS PROCESSED AGAIN. *******
**********************************************************************************************************************************************************************/
package com.whiterabbit.sqlhelpertester;


import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;

import java.util.Date;

public class DbHelperProviderClient{


    // ------------- EVENT_HELPERS ------------
    public static Uri addEvent (String Description, 
                                Date Time, 
                                String ShortDesc, 
                                Context c) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(DbHelperProvider.EVENT_DESCRIPTION_COLUMN, Description);
        contentValues.put(DbHelperProvider.EVENT_TIME_COLUMN, Time.getTime());
        contentValues.put(DbHelperProvider.EVENT_SHORTDESC_COLUMN, ShortDesc);
        ContentResolver cr = c.getContentResolver();
        return cr.insert(DbHelperProvider.EVENT_URI, contentValues);
    }

    public static int removeEvent(long rowIndex, Context c){
        ContentResolver cr = c.getContentResolver();
        Uri rowAddress = ContentUris.withAppendedId(DbHelperProvider.EVENT_URI, rowIndex);
        return cr.delete(rowAddress, null, null);
    }

    public static int removeAllEvent(Context c){
        ContentResolver cr = c.getContentResolver();
        return cr.delete(DbHelperProvider.EVENT_URI, null, null);
    }

    public static Cursor getAllEvent(Context c){
    	ContentResolver cr = c.getContentResolver();
        String[] resultColumns = new String[] {
                         DbHelperProvider.ROW_ID,
                         DbHelperProvider.EVENT_DESCRIPTION_COLUMN,
                         DbHelperProvider.EVENT_TIME_COLUMN,
                         DbHelperProvider.EVENT_SHORTDESC_COLUMN
                         };

        Cursor resultCursor = cr.query(DbHelperProvider.EVENT_URI, resultColumns, null, null, null);
        return resultCursor;
    }

    public static Cursor getEvent(long rowId, Context c){
    	ContentResolver cr = c.getContentResolver();
        String[] resultColumns = new String[] {
                         DbHelperProvider.ROW_ID,
                         DbHelperProvider.EVENT_DESCRIPTION_COLUMN,
                         DbHelperProvider.EVENT_TIME_COLUMN,
                         DbHelperProvider.EVENT_SHORTDESC_COLUMN
                         };

        Uri rowAddress = ContentUris.withAppendedId(DbHelperProvider.EVENT_URI, rowId);
        String where = null;    
        String whereArgs[] = null;
        String order = null;
    
        Cursor resultCursor = cr.query(rowAddress, resultColumns, where, whereArgs, order);
        return resultCursor;
    }

    public static int updateEvent (int rowId, 
                                   String Description,
                                   Date Time,
                                   String ShortDesc,
                                   Context c) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(DbHelperProvider.EVENT_DESCRIPTION_COLUMN, Description);
        contentValues.put(DbHelperProvider.EVENT_TIME_COLUMN, Time.getTime());
        contentValues.put(DbHelperProvider.EVENT_SHORTDESC_COLUMN, ShortDesc);
        Uri rowAddress = ContentUris.withAppendedId(DbHelperProvider.EVENT_URI, rowId);

        ContentResolver cr = c.getContentResolver();
        int updatedRowCount = cr.update(rowAddress, contentValues, null, null);
        return updatedRowCount;
    }
    
    // ------------- CALL_HELPERS ------------
    public static Uri addCall (String Number, 
                                Date Time, 
                                Float value, 
                                long longnumber, 
                                Context c) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(DbHelperProvider.CALL_NUMBER_COLUMN, Number);
        contentValues.put(DbHelperProvider.CALL_TIME_COLUMN, Time.getTime());
        contentValues.put(DbHelperProvider.CALL_VALUE_COLUMN, value);
        contentValues.put(DbHelperProvider.CALL_LONGNUMBER_COLUMN, longnumber);
        ContentResolver cr = c.getContentResolver();
        return cr.insert(DbHelperProvider.CALL_URI, contentValues);
    }

    public static int removeCall(long rowIndex, Context c){
        ContentResolver cr = c.getContentResolver();
        Uri rowAddress = ContentUris.withAppendedId(DbHelperProvider.CALL_URI, rowIndex);
        return cr.delete(rowAddress, null, null);
    }

    public static int removeAllCall(Context c){
        ContentResolver cr = c.getContentResolver();
        return cr.delete(DbHelperProvider.CALL_URI, null, null);
    }

    public static Cursor getAllCall(Context c){
    	ContentResolver cr = c.getContentResolver();
        String[] resultColumns = new String[] {
                         DbHelperProvider.ROW_ID,
                         DbHelperProvider.CALL_NUMBER_COLUMN,
                         DbHelperProvider.CALL_TIME_COLUMN,
                         DbHelperProvider.CALL_VALUE_COLUMN,
                         DbHelperProvider.CALL_LONGNUMBER_COLUMN
                         };

        Cursor resultCursor = cr.query(DbHelperProvider.CALL_URI, resultColumns, null, null, null);
        return resultCursor;
    }

    public static Cursor getCall(long rowId, Context c){
    	ContentResolver cr = c.getContentResolver();
        String[] resultColumns = new String[] {
                         DbHelperProvider.ROW_ID,
                         DbHelperProvider.CALL_NUMBER_COLUMN,
                         DbHelperProvider.CALL_TIME_COLUMN,
                         DbHelperProvider.CALL_VALUE_COLUMN,
                         DbHelperProvider.CALL_LONGNUMBER_COLUMN
                         };

        Uri rowAddress = ContentUris.withAppendedId(DbHelperProvider.CALL_URI, rowId);
        String where = null;    
        String whereArgs[] = null;
        String order = null;
    
        Cursor resultCursor = cr.query(rowAddress, resultColumns, where, whereArgs, order);
        return resultCursor;
    }

    public static int updateCall (int rowId, 
                                   String Number,
                                   Date Time,
                                   Float value,
                                   long longnumber,
                                   Context c) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(DbHelperProvider.CALL_NUMBER_COLUMN, Number);
        contentValues.put(DbHelperProvider.CALL_TIME_COLUMN, Time.getTime());
        contentValues.put(DbHelperProvider.CALL_VALUE_COLUMN, value);
        contentValues.put(DbHelperProvider.CALL_LONGNUMBER_COLUMN, longnumber);
        Uri rowAddress = ContentUris.withAppendedId(DbHelperProvider.CALL_URI, rowId);

        ContentResolver cr = c.getContentResolver();
        int updatedRowCount = cr.update(rowAddress, contentValues, null, null);
        return updatedRowCount;
    }
    
}
