import android.database.Cursor;
import android.test.AndroidTestCase;

import com.whiterabbit.sqlhelpertester.DbHelperDbHelper;

import java.util.Date;

/**
 * Created by fedepaol on 22/06/14.
 */
public class SqlLiteTests extends AndroidTestCase {
    DbHelperDbHelper mHelper;

    @Override
    public void tearDown() throws Exception {
        mHelper.close();
    }

    @Override
    public void setUp() throws Exception {
        mHelper = new DbHelperDbHelper(getContext());
        mHelper.open();
        mHelper.removeAllCall();
        mHelper.removeAllEvent();
    }

    public void testInsert() throws Exception {
        mHelper.addCall("AAAA", new Date(), 23.0f, 23);
        mHelper.addCall("BBBB", new Date(), 24.0f, 24);
        mHelper.addCall("AAAA", new Date(), 25.0f, 25);
        Cursor c = mHelper.getAllCall();
        assertEquals(c.getCount(), 3);
    }

    public void testDelete() {
        mHelper.addEvent("AAAA", new Date(), "ShortEvent");
        Cursor c = mHelper.getAllEvent();
        c.moveToFirst();
        int index = c.getInt(0);
        mHelper.removeEvent(index);
    }

    public void testEdit() {
        mHelper.addEvent("BBBB", new Date(), "ShortEvent");
        Cursor c = mHelper.getAllEvent();
        c.moveToFirst();
        int index = c.getInt(0);
        mHelper.updateEvent(index, "CCCC", new Date(), "ShortName1");
        c = mHelper.getAllEvent();
        c.moveToFirst();
        assertEquals(c.getString(DbHelperDbHelper.EVENT_DESCRIPTION_COLUMN_POSITION), "CCCC");
    }
}
