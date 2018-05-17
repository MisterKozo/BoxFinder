# BoxFinder

**V V V V V English below V V V V V**

תרגישו חופשי להשתמש במה שתמצאו לנכון. זה אמור לעבוד אם טווח הצבעים מוגדר כמו שצריך.

שולח זווית לחפץ הצהוב המרובע הכי קרוב לרובוט, ושולח וידיאו למחשב.

חשוב לעשות קליברציה ב- utils.py לצבע המתאים אחרי שמחליפים מצלמה.


על מנת שנתונים יתקבלו, השרת(ים) צריכים לקבל את הפורטים: 42069, 6969, 666. 42069 בשביל פקודות, 6969 בשביל וידיאו ו6666 בשביל דיבוג (לא השתמשתי בזה עדיין אבל אפשר לגשת לזה בקלות דרך dconn.sent("your desired string") בקובץ runner.py)

**V V V V V English below V V V V V**



Feel free to reuse whatever you may find useful in this code. This is supposed to be functional if the colors range is set correctly.

Detects the closest yellow rectangle and sends the angle to the robot and to the computer

It's important to calibrate in utils.py after switching to another camera.


For data to be accepted, the server(s) need(s) to accept ports: 42069, 6969, 6666. 42069 for commands, 6969 for video and 6666 for debugging (not implemented yet but can be accessed simply by using dconn.sent("your desired string") in runner.py)
