        $(document).ready(function () {
            getDataQueue(); //load data on page ready :)
            setInterval(function () {
                getDataQueue();
            }, REQUEST_INTERVAL);
        });

        // parse data and put values on view
        function parseDataQueue(data){
            var answers = 0, unattended = 0, incoming = 0;
            var c_hold = 0, holdtime = 0, c_talk = 0, talktime = 0;
            var call_in_service_level = 0;
            for (var d in data) {
                answers = answers + parseInt(data[d].Completed);
                unattended = unattended + parseInt(data[d].Abandoned);
                incoming = incoming + parseInt(data[d].Calls);

                $("[id='data-"+ d + "'] #queue_completed").html(parseInt(data[d].Completed));
                $("[id='data-"+ d + "'] #queue_abandoned").html(parseInt(data[d].Abandoned));
                $("[id='data-"+ d + "'] #queue_incoming").html(parseInt(data[d].Calls));
                $("[id='data-"+ d + "'] #queue_users").html(len(data[d].members));
                $(".header-"+ d + " #strategy").html(data[d].Strategy);

                if (SHOW_SERVICE_LEVEL === true) {
                $("[id='data-"+ d + "'] #queue_servicelevel").html(data[d].ServicelevelPerf + '%');
                call_in_service_level +=  data[d].Completed * parseFloat(data[d].ServicelevelPerf) / 100;
                }

                if (data[d].Abandoned > 0) {
                    $("[id='"+ d + "-percent_abandoned']")
                        .html(parseInt(parseInt(data[d].Abandoned)  * 100 / (parseInt(data[d].Abandoned) + parseInt(data[d].Completed) )));
                }

                if (parseInt(data[d].TalkTime) > 0 ) {
                    talktime = talktime + parseInt(data[d].TalkTime);
                    c_talk++;
                }

                if (parseInt(data[d].Holdtime) > 0 ) {
                    holdtime = holdtime + parseInt(data[d].Holdtime);
                    c_hold++;
                }

                var agent_free = 0, agent_busy = 0, agent_unavailable = 0;
                for (agent in data[d].members) {
                    var status_agent = parseInt(data[d].members[agent].Status);
                    if (data[d].members[agent].Paused == true) {
                        agent_busy++;
                    } else if (C.status_agent.NOT_INUSE == status_agent) {
                        agent_free++;
                    } else if (status_agent.isUnavailableInAsterisk()) {
                        agent_unavailable++;
                    } else {
                        agent_busy++;
                    }
                }
                agents = agent_free + agent_busy + agent_unavailable;
                //bugfix NaN division by 0
                if (agents == 0) {
                    agents = 1;
                }
                $("[id='data-"+ d + "'] #queue_free")
                    .html( "{agents} ({percent}% {status})"
                        .format({agents: agent_free, percent: Math.round(agent_free * 100 / agents), status: STATUSES.free }));
                $("[id='data-"+ d + "'] #queue_busy")
                    .html( "{agents} ({percent}% {status})"
                        .format({agents: agent_busy, percent: Math.round(agent_busy * 100 / agents), status: STATUSES.busy }));

                $("[id='data-"+ d + "'] #queue_unavailable")
                    .html( "{agents} ({percent}% {status})"
                        .format({agents: agent_unavailable, percent: Math.round(agent_unavailable * 100 / agents), status: STATUSES.unavailable}));

            }
            $('#answered').html(answers);
            $('#abandoned').html(unattended);
            $('#incoming').html(incoming);
            if (c_hold > 0 ) {
              $('#av_wait').html(parseInt((holdtime / c_hold)).toString().toMMSS());
            }
            if (c_talk > 0){
              $('#av_time').html(parseInt((talktime / c_talk)).toString().toMMSS());
            }

            if (SHOW_SERVICE_LEVEL === true) {
                if (answers == 0) {
                    $('#servicelevel').html( "{percent}%".format({percent: 0.0}));
                } else {
                    $('#servicelevel').html( "{percent}%".format({percent: Math.round(call_in_service_level * 100 / answers)}));
                }
            }

        }
        function getDataQueue() {
            var result;
            var r = $.ajax({
                type: 'GET',
                url: URL_QUEUE_DATA
            });
            r.done(function (response) {
                if (response) {
                    result = response.data;
                    parseDataQueue(result);
                }
            });
            r.fail(function (response) {
            });

            r.always(function () {
            });
        }




