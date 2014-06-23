package com.whiterabbit.sqlhelpertester.test;

import android.test.InstrumentationTestCase;

/**
 * Created by fedepaol on 22/06/14.
 */
public class SimpleTest extends InstrumentationTestCase {
    public void test() throws Exception {
        final int expected = 1;
        final int reality = 5;
        assertEquals(expected, reality);
    }
}
