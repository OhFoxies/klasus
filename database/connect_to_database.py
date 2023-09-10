import sqlite3


def connect():
    with sqlite3.connect("database/database.db") as db:
        db.execute("CREATE TABLE IF NOT EXISTS `guilds` ("
                   "`ID` INTEGER , "
                   "`guild_id` VARCHAR(99) NOT NULL , "
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")

        db.execute("CREATE TABLE IF NOT EXISTS `schools` ("
                   "`ID` INTEGER, "
                   "`school_name` VARCHAR(99) NOT NULL , "
                   "`guild_id` VARCHAR(99) NOT NULL , "
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")

        db.execute("CREATE TABLE IF NOT EXISTS `classes` ("
                   "`ID` INTEGER, "
                   "`school_name` VARCHAR(99) NOT NULL, "
                   "`class_name` VARCHAR(99) NOT NULL , "
                   "`guild_id` VARCHAR(99) NOT NULL, "
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")

        db.execute("CREATE TABLE IF NOT EXISTS `group` ("
                   "`ID` INTEGER, "
                   "`school_name` VARCHAR(99) NOT NULL, "
                   "`class_name` VARCHAR(99) NOT NULL , "
                   "`group_name` VARCHAR(99) NOT NULL , "
                   "`keystore` TEXT NOT NULL , "
                   "`account` TEXT NOT NULL , "
                   "`guild_id` VARCHAR(99) NOT NULL, "
                   "`user_vulcan` VARCHAR(99) NOT NULL, "
                   "`channel_id` VARCHAR(99) NOT NULL, "
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")

        db.execute("CREATE TABLE IF NOT EXISTS `user` ("
                   "`ID` INTEGER, "
                   "`user_id` VARCHAR(999) NOT NULL , "
                   "`class_name` VARCHAR(999) NOT NULL , "
                   "`school_name` VARCHAR(999) NOT NULL , "
                   "`group_name` VARCHAR(999) NOT NULL , "
                   "`guild_id` VARCHAR(99) NOT NULL, "
                   "`number` VARCHAR(99) NOT NULL, "
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")
        db.commit()