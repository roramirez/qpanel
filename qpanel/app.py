{% extends theme('base.html') %}
{% block title %} QPanel - {{ name }} {% endblock %}

    {% block main %}
      <!--main content start-->
      <section id="main-content" style="margin-left: 0px;">


          <section class="wrapper">
              <h3><i class="fa fa-angle-right"></i> {{ name }} - <span id="strategy"</span></h3>

              <div class="row">
                  <div class="col-lg-12 main-chart">

                      <div class="row"><!-- row general data-->
                        {% include 'row_general_data.html' %}
                      </div><!-- /row general data-->

                     <div class="row mt">
                    </div><!-- /row -->

                  <div class="col-md-12">
                      <div class="content-panel">
                          <table class="table table-striped table-advance table-hover" id="agents">
                            <h4><i class="fa fa-angle-right"></i> {{ _('Agents') }}: <span id="total_agent" class="label label-default"></span></h4>
                            <hr>
                              <thead>
                              <tr>
                                  <th><i class="fa fa-user"></i> {{ _('Name') }}</th>
                                  <th><i class="fa fa-plug"></i> {{ _('Interface') }}</th>
                                  <th><i class=" fa fa-question-circle "></i> {{ _('Status') }}</th>
                                  <th><i class="fa fa-bookmark"></i> <span data-toggle="tooltip" data-placement="left" title="{{ _('Attend calls') }}"></i> {{ _('Calls') }}</span></th>
                                  <th><i class="fa fa-clock-o"></i> {{ _('Last call at') }}</th>

                                  <th><i class="fa fa-action-o"></i> {{_('Actions')}}</th>

                              </tr>
                              </thead>
                              <tbody>
                              {% for agent_id, agent in data.members.items() %}
                              <tr id="agent-{{ clean_str_to_div_id(agent_id) }}">
                                  <td>{{ agent.Name }}</td>
                                  <td class="hidden-phone">{{ agent.StateInterface }}</td>
                                  <td id="status">
                                    <span class="label label-info label-mini state">
                                        {{ str_status_agent(agent.Status) }}
                                    </span>
                                  <td id="calls">{{ agent.CallsTaken }}</td>
                                  <td id="last_call">{{ agent.LastCall }}</td>
                                  <td id="actions" data-channel="{{ agent.StateInterface }}">
                                    <a href="#" data-action="spy">{{ _('Spy') }}</a> |
                                    <a href="#" data-action="whisper">{{ _('Whisper') }}</a> |
                                    <a href="#" data-action="barge">{{ _('Barge') }}</a> |
                                    <button data-queue="{{ name }}" class="remove-queue">{{ _('Remove from queue') }}</button>
                                  </td>
                              </tr>
                              {% endfor %}
                              </tbody>
                          </table>
                      </div><!-- /content-panel -->
                  </div><!-- /col-md-12 -->

                  <div class="col-md-12">
                      <div class="content-panel">
                          <table class="table table-striped table-advance table-hover" id="callers">
                            <h4><i class="fa fa-angle-right"></i> {{ _('Callers') }}: <span id="total_callers" class="label label-default"></span></h4>
                            <hr>
                              <thead>
                              <tr>
                                  <th><i class="fa fa-user"></i> {{ _('Id Name') }}</th>
                                  <th class="hidden-phone"><i class="fa fa-phone"></i> {{ _('Id Number') }}</th>
                                  <th><i class="fa fa-sort-numeric-asc"></i> {{ _('Position') }}</th>
                                  <th><i class="fa fa-clock-o"></i> {{ _('Wait') }}</th>
                                  <th></th>
                              </tr>
                              </thead>
                              <tbody>
                              {% for key, caller in data.entries.items() %}
                              <tr id="caller-{{ caller.Uniqueid }}" data-uniqueid="{{ caller.Uniqueid }}">
                                  <td>{{ caller.CallerIDName }}</td>
                                  <td class="hidden-phone">{{ caller.CallerIDNum }}</td>
                                  <td id="position">{{ caller.Position }}</td>
                                  <td id="wait">{{ caller.Wait }}</td>
                                  <td>
                                      <button class="btn btn-danger btn-xs" id="stop-call">
                                          <i class="fa fa-ban"></i>
                                      </button>
                                  </td>
                              </tr>
                              {% endfor %}
                              </tbody>
                          </table>
                      </div><!-- /content-panel -->
                  </div><!-- /col-md-12 -->

          </section>
      </section>

    <!-- Modal spy and whisper -->
    <div id="spy_whisperk" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="swModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button> 
                    <h4 class="modal-title"></h4>
                </div>
                <div class="col-lg-2">
                    <h4><i class="fa fa-headphones fa-5x"></i> </h4>
                </div>
                <div class="col-lg-10">
                    <br/>
                    <p>{{ _('Insert where  you listen the call, example: <i>SIP/1001</i>')}}</p>
                    <div class="input-group">
                        <input id="to_exten" type="text" class="form-control" value="">
                        <span class="input-group-btn">
                            <button class="btn btn-default" id="execute-action" data-action="" data-channel=""  title="{{_('Listen ')}}"></button>
                        </span>
                    </div>
                    <div class="input-group">
                        <label class="modal-message"></label>
                    </div>
                </div>
                <div class="modal-footer">
                </div>
            </div>
         </div>
    </div>
    <!-- End Modal spy and whisper -->
    {% endblock %}

    {% block script_end %}
    <script type="application/javascript">
        $(document).ready(function () {
            getDataQueue(); //load data on page ready :)
            setInterval(function () {
                getDataQueue();
            }, {{ request_interval() }});
        });
        // parse data and put values on view
        function parseDataQueue(data){
          $('#answered').html(data.Completed);
          $('#abandoned').html(data.Abandoned);
          $('#incoming').html(data.Calls);
          $('#av_wait').html(parseInt(data.Holdtime).toString().toMMSS());
          $('#av_time').html(parseInt(data.TalkTime).toString().toMMSS());

          {% if show_service_level() %}
          $("#servicelevel").html(data.ServicelevelPerf + '%');
          {% endif %}

          //agents
          var agents_ids = Array();
          for (agent in data.members) {
            agent_id_div = clean_div_name(agent);
            $('#agent-' + agent_id_div + ' #calls').html(data.members[agent].CallsTaken)

            str_time_ago = ''
            if (data.members[agent].LastCall > 0) {
               str_time_ago = data.members[agent].LastCallAgo;
            }
            $('#agent-' + agent_id_div + ' #last_call').html(str_time_ago)

            $('#agent-' + agent_id_div + ' #status .state').html(data.members[agent].Status.toStrStatusAgent())
            addLabelDivStatusAgent($('#agent-' + agent_id_div + ' #status .state'));

            if (data.members[agent].Paused == true) {
                // reason pause introduced in https://goo.gl/Njm6H5
                // if dont have feature in your Asterisk
                // check directory patches
                var reason = '';
                if (data.members[agent].PausedReason){
                    reason = ": {reason}".format({'reason': data.members[agent].PausedReason});
                }
                var last_pause_time = '';
                if (parseInt(data.members[agent].LastPauseAgo.split(" ")[0]) > 0){
                    last_pause_time = " {{ _('was') }} {last_pause} {{_('ago') }}".format({'last_pause': data.members[agent].LastPauseAgo});
                }

                $('#agent-' + agent_id_div + ' #status .pause').remove();
                $('#agent-'+ agent_id_div +' #status .state')
                   .after(' <span class="label label-success label-mini pause">{{ _('paused') }}'+ reason + last_pause_time + '</span>');
            } else {
                $('#agent-' + agent_id_div + ' #status .pause').remove();
            }


            if ($('#agent-' + agent_id_div).length == 0) {

                var tr = '<tr id="agent-'+agent_id_div+'"><td>'
                         + data.members[agent].Name + '</td>'
                         + '<td>'+data.members[agent].StateInterface + '</td>'
                         + '<td id="status"> <span class="label label-info label-mini state">'
                         + data.members[agent].Status.toStrStatusAgent()
                         + '</span></td>'
                         + '<td id="calls">'+ data.members[agent].CallsTaken +'</td>'
                         + '<td id="last_call"></td>'
                         + '<td id="actions" data-channel="' + data.members[agent].StateInterface + '">'
                         +      '<a href="#" data-action="spy">{{ _('Spy') }}</a> |'
                         +      '<a href="#" data-action="whisper">{{ _('Whisper') }}</a> |'
                         +      '<a href="#" data-action="barge">{{ _('Barge') }}</a> |'
                         +      '<button data-queue="{{ name }}" class="remove-queue">{{ _('Remove from queue') }}</button>'
                         + '</td>'
                         + '</tr>';

                if ($('#agents tbody tr:last').length > 0){
                    $('#agents tbody tr:last').after(tr);
                } else {
                    $('#agents tbody').append(tr);
                }
                addLabelDivStatusAgent($('#agent-' + agent_id_div + ' #status .state'));
            }

            agents_ids.push(agent_id_div);
          }
          $('#total_agent').html("{total}".format({total:  Object.keys(data.members).length}));

          //callers
          var uniques_ids = Array();
          for (caller in data.entries) {
            c = data.entries[caller];

            if ($("[id='caller-"+ c.Uniqueid + "']").length == 0) {
              console.log('add:' + c.Uniqueid);

              var tr = '<tr id="caller-' + c.Uniqueid + '" data-uniqueid="' + c.Uniqueid + '"><td>'
                        + c.CallerIDName + '</td>'
                        + '<td>' + c.CallerIDNum + '</td>'
                        + '<td id="position">'  + c.Position + '</td>'
                        + '<td id="wait">' + c.WaitAgo + '</td>'
                        + '<td>'
                        +    '<button class="btn btn-danger btn-xs" id="stop-call">'
                        +       '<i class="fa fa-ban"></i>'
                        +     '</button>'
                        + '</td>'
                        + '</tr>'


              if ($('#callers tbody tr:last').length > 0){
                $('#callers tbody tr:last').after(tr);
              } else {
                $('#callers tbody').append(tr);
              }
            }

            $("[id='caller-"+ c.Uniqueid + "'] #wait").html(c.WaitAgo);
            $("[id='caller-"+ c.Uniqueid + "'] #position").html(c.Position);
            uniques_ids.push(c.Uniqueid);
          }
          $.each($("[id^='caller-']"), function( index, value ) {
            uid = $(value).data('uniqueid');
            if (uniques_ids.indexOf(uid.toString()) == -1) {
              console.log('removed: ' + uid);
              $("[id='caller-"+ uid +"']").remove();
            }
          });
          $('#total_callers').html("{total}".format({total:  Object.keys(data.entries).length}));
          $.each($("[id^='agent-']"), function( index, value ) {
            uid = $(value).attr('id').substring(6);
            if (agents_ids.indexOf(uid.toString()) == -1) {
              console.log('removed: ' + uid);
              $("[id='agent-"+ uid +"']").remove();
            }
          });

          $('#strategy').html(data.Strategy);
        }

        function getDataQueue() {
            var result;
            var r = $.ajax({
                type: 'GET',
                url: '{{ url_for('.queue', name=name+".json") }}'
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


        //handle show modal for Spy and Whisper
        $('#actions* a').not('.remove-queue').on('click', function() {
            var action = $(this).data('action');
            channel = $(this.closest('td')).data('channel');
            $('#spy_whisperk #execute-action').data('channel', channel);
            $('#spy_whisperk #execute-action').data('action', action);
            $('#spy_whisperk #execute-action').html(action);
            $('#spy_whisperk .modal-header h4').html('{{_('Execute a ')}}' + action);
            $('#spy_whisperk').modal();
        });
        var r=null;
        $('#execute-action').on('click', function() {
            var to_exten = $('#spy_whisperk  #to_exten').val();
            if (to_exten == "") {
                $('.modal-message').html('{{_('Insert where do need listen')}}');
                $('.modal-message').addClass('has-error')
                return 0;
            }

            $('.modal-message').removeClass('has-error');
            $('.modal-message').html('{{_('Try...')}}');

            $('#execute-action').prop("disabled", true);

            var channel = $(this).data('channel');
            var action = $(this).data('action');

            console.log("do a %s to channel %s", action, channel);

            var url_action = ''
            if (action == 'spy') {
                url_action = '{{url_for('.spy')}}';
            } else if (action == 'whisper') {
                url_action = '{{url_for('.whisper')}}';
            } else if (action == 'barge') {
                url_action = '{{url_for('.barge')}}';
            }
            var r = $.ajax({
                type: 'post',
                url: url_action,
                data: {channel: channel, to_exten: to_exten}
            });
            r.done(function (response) {
                if (response) {
                    var status = response.result.Response;
                    console.log(status);
                    if (status == 'failed') {
                        $('.modal-message').html("Failed:" +  response.result.Message);
                        $('.modal-message').addClass('has-error')
                    } else {
                        $('.modal-message').html(response.result.Message);
                        $('.modal-message').removeClass('has-error')
                    }
                }
            });
            r.fail(function (response) {
                console.log(response);
            });

            r.always(function () {
                $('#execute-action').prop("disabled", false);
            });
        });



        $('#stop-call').on('click', function() {
            var tr = $(this).closest("tr");
            var uniqueid = tr.data('uniqueid');
            console.log('stop call %s...', uniqueid );
            button = $(this);
            $('.message-hangup').remove();

            var r = $.ajax({
                type: 'post',
                url: '/hangup',
                data: {channel: uniqueid}
            });
            r.done(function (response) {
                if (response) {
                    console.log(response.result.Response);
                    msg = '<span class="btn btn-xs message-hangup">'
                        + response.result.Message + '</span>';

                    $(button).after(msg);
                    var status = response.result.Response;
                    console.log(status);
                    if (status == 'failed') {
                        $('.message-hangup').addClass('btn-danger');
                    } else {
                        $('.message-hangup').addClass('btn-success');
                        setTimeout(function() { tr.remove(); }, 1000);
                        var total_callers = (parseInt($('#total_callers').html()) - 1);
                        $('#total_callers').html("{total}".format({total:  total_callers}));
                    }
                }
            });
            r.fail(function (response) {
                console.log(response);
            });

        });

        $('.remove-queue').on('click', function() {
            var tr = $(this).closest("tr");
            var queue = $(this).data('queue');
            var agent = $(this.closest('td')).data('channel');

            console.log('remove agent %s from %s', agent, queue);
            button = $(this);
            $('.message-hangup').remove();

            var r = $.ajax({
                type: 'post',
                url: '{{ url_for('.remove_from_queue') }}',
                data: {agent: agent, queue: queue}
            });
            r.done(function (response) {
                if (response) {
                    console.log(response.result.Response);
                    msg = '<span class="btn btn-xs message-hangup">'
                        + response.result.Message + '</span>';

                    $(button).after(msg);
                    var status = response.result.Response;
                    console.log(status);
                    if (status == 'failed') {
                        $('.message-hangup').addClass('btn-danger');
                    } else {
                        $('.message-hangup').addClass('btn-success');
                        setTimeout(function() { tr.remove(); }, 1000);
                        var total_agents = (parseInt($('#total_agent').html()) - 1);
                        $('#total_agent').html("{total}".format({total:  total_agents}));
                    }
                }
            });
            r.fail(function (response) {
                console.log(response);
            });

        });


    </script>
    {% endblock %}