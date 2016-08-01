CREATE TABLE `queue_log` (
    `id` bigint(255) unsigned NOT NULL AUTO_INCREMENT,
    `time` varchar(26) NOT NULL DEFAULT '',
    `callid` varchar(40) NOT NULL DEFAULT '',
    `queuename` varchar(20) NOT NULL DEFAULT '',
    `agent` varchar(20) NOT NULL DEFAULT '',
    `event` varchar(20) NOT NULL DEFAULT '',
    `data` varchar(100) NOT NULL DEFAULT '',
    `data1` varchar(40) NOT NULL DEFAULT '',
    `data2` varchar(40) NOT NULL DEFAULT '',
    `data3` varchar(40) NOT NULL DEFAULT '',
    `data4` varchar(40) NOT NULL DEFAULT '',
    `data5` varchar(40) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`),
    KEY `queue` (`queuename`),
    KEY `event` (`event`)
);
