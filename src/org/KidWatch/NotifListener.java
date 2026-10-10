package org.kidwatch;

import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.app.Notification;
import android.content.Intent;
import android.util.Log;

public class NotificationService extends NotificationListenerService {
    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        String packageName = sbn.getPackageName();
        Notification notification = sbn.getNotification();
        
        if (notification != null && notification.extras != null) {
            CharSequence titleChar = notification.extras.getCharSequence(Notification.EXTRA_TITLE);
            CharSequence textChar = notification.extras.getCharSequence(Notification.EXTRA_TEXT);

            String title = titleChar != null ? titleChar.toString() : "";
            String text = textChar != null ? textChar.toString() : "";

            Log.d("KidWatchJava", "Captured: " + packageName + " | " + title + ": " + text);

            // Python Service-এ ডাটা পাঠানোর জন্য Broadcast Intent
            Intent intent = new Intent("org.kidwatch.NOTIFICATION_RECEIVED");
            intent.putExtra("package", packageName);
            intent.putExtra("title", title);
            intent.putExtra("text", text);
            sendBroadcast(intent);
        }
    }

    @Override
    public void onNotificationRemoved(StatusBarNotification sbn) {
        // নোটিফিকেশন সরানো হলে প্রয়োজন অনুযায়ী কাজ করা যাবে
    }
}