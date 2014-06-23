import android.content.Context;
import android.database.Cursor;
import android.test.AndroidTestCase;

import com.whiterabbit.sqlhelpertester.DbHelperDbHelper;
import com.whiterabbit.sqlhelpertester.DbHelperProviderClient;

import java.util.Date;

/**
 * Created by fedepaol on 22/06/14.
 */
public class ProviderTest extends AndroidTestCase {
    Context mContext;

    @Override
    public void setUp() throws Exception {
        mContext = getContext();
        DbHelperProviderClient.removeAllCall(mContext);
        DbHelperProviderClient.removeAllEvent(mContext);
    }

    public void testInsert() throws Exception {
        DbHelperProviderClient.addCall("AAAA", new Date(), 23.0f, 23, mContext);
        DbHelperProviderClient.addCall("BBBB", new Date(), 23.0f, 23, mContext);

        Cursor c = DbHelperProviderClient.getAllCall(mContext);
        assertEquals(c.getCount(), 2);
    }

    public void testDelete() {
        DbHelperProviderClient.addEvent("AAAA", new Date(), "ShortEvent", mContext);
        DbHelperProviderClient.addEvent("BBBB", new Date(), "ShortEvent", mContext);
        Cursor c = DbHelperProviderClient.getAllEvent(mContext);
        c.moveToFirst();
        int index = c.getInt(0);
        DbHelperProviderClient.removeEvent(index, mContext);
        Cursor c1 = DbHelperProviderClient.getAllEvent(mContext);
        assertEquals(c1.getCount(), 1);
    }

    public void testEdit() {
        DbHelperProviderClient.addEvent("BBBB", new Date(), "ShortEvent", mContext);
        Cursor c = DbHelperProviderClient.getAllEvent(mContext);
        c.moveToFirst();
        int index = c.getInt(0);
        DbHelperProviderClient.updateEvent(index, "CCCC", new Date(), "ShortName1", mContext);
        c = DbHelperProviderClient.getAllEvent(mContext);
        c.moveToFirst();
        assertEquals(c.getString(DbHelperDbHelper.EVENT_DESCRIPTION_COLUMN_POSITION), "CCCC");
    }
}
