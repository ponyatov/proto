package io.github.ponyatov.hello;

import android.app.Activity; // android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends Activity { // } AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
