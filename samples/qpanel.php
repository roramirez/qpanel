<?php
/*
	QPanel
*/
//includes
require_once "require.php";

$sql = "SELECT v_call_center_queues.* 
    FROM v_users, 
         v_domains, 
         v_call_center_queues 
    WHERE 
        v_users.domain_uuid = v_domains.domain_uuid AND
        v_domains.domain_uuid = v_call_center_queues.domain_uuid AND
        v_domains.domain_uuid = :domain_uuid AND
        v_users.username = :username AND
        v_users.user_uuid = :user_uuid AND
        v_domains.domain_name = :domain_name;";


    $parameters['domain_name'] = $_GET["domain_name"];
    $parameters['domain_uuid'] = $_GET["domain_uuid"];
    $parameters['user_uuid']   = $_GET["user_uuid"];
    $parameters['username']    = $_GET["username"];
    $database = new database;
    $result = $database->select($sql, $parameters, 'all');

    $queues = Array();
	foreach ($result as $queue) {
        $obj = (object) array('id' => $queue['call_center_queue_uuid'], 'name' => $queue['queue_name']);
        $queues[] = $obj;
	}
    header('Content-Type: application/json');
    echo json_encode($queues);

?>
