var socket = new ReconnectingWebSocket('ws://' + location.host + '/observation');

function sendAction(msg) {
    socket.send(JSON.stringify(msg));
}

socket.onopen = function(event) {
    var msg = {action: 'browsertoken', data: 'none'};

    sendAction(msg);
}

socket.onclose = function() {
}

socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var action = data['action'];

    if (action == 'pepper_eye') {
        var b64_img = data['data'];
        $("#pepper_eye").attr("src", b64_img);
    }
    else if (action == 'update_chart') {
        if (chart_data.length > 30) {
            chart_data.shift();
        }
        console.log(data['data']);
        /*chart_data.push(data['data']);
        chart.setData(chart_data);*/
        if (chart.options.ykeys.indexOf(data['data']['id']) == -1) {
            chart.options.ykeys.push(data['data']['id']);
            chart.options.labels.push(data['data']['id']);
        }
        var key = data['data']['id'];
        var d = {time: data['data']['time']};
        d[key] = data['data']['value'];
        chart_data.push(d);
        chart.setData(chart_data);
    }
    else if (action == 'user_utt') {
        add_text_to_chat(data['data'], true);
        scrollBottom('chat');
    } else if (action == 'system_utt') {
        add_text_to_chat(data['data'], false);
        scrollBottom('chat');
    } else {
        Lobibox.notify('error', {
                        sound: false,
                        position: 'bottom left',
                        size: 'mini',
                        title: '助けて！',
                        msg: '私ではこれ以上対応できません。'
        });
    }
}

$('#submit_access_token').on('click', function() {
    var access_token = $('#access_token').val();
    var msg = {action: 'send_access_token', data: access_token};

    $('#access_token').val('');
    sendAction(msg);
})

$('#access_token').keypress(function(e) {
    if (e.which == 13) {
        var access_token = $(this).val();
        var msg = {action: 'send_access_token', data: access_token};

        $(this).val('');
        sendAction(msg);
    }
})

$('#connect2robot').on('click', function() {
    var access_token = '';
    var msg = {action: 'send_access_token', data: access_token};
    sendAction(msg);
})

function add_text_to_chat(text, is_left) {

    if (is_left) {
        var tag = '<li class="left clearfix">' +
                    '<span class="chat-img pull-left">' +
                      '<img src="http://placehold.it/50/55C1E7/fff" alt="User Avatar" class="img-circle" />' +
                    '</span>' +
                    '<div class="chat-body clearfix">' +
                      '<div class="header">' +
                        '<strong class="primary-font">Customer</strong>' +
                        '<small class="pull-right text-muted"><i class="fa fa-clock-o fa-fw"></i></small>' +
                      '</div>' +
                      '<p>' +
                        text +
                      '</p>' +
                    '</div>' +
                  '</li>';
    }
    else {
        var tag = '<li class="right clearfix">' +
                    '<span class="chat-img pull-right">' +
                      '<img src="http://placehold.it/50/FA6F57/fff" alt="User Avatar" class="img-circle" />' +
                    '</span>' +
                    '<div class="chat-body clearfix">' +
                      '<div class="header">' +
                        '<small class=" text-muted"><i class="fa fa-clock-o fa-fw"></i></small>' +
                        '<strong class="pull-right primary-font">Robot</strong>' +
                      '</div>' +
                      '<p>' +
                        text
                      '</p>' +
                    '</div>' +
                  '</li>';
    }
    $('.chat').append(tag);
}

function scrollBottom(targetId) {
    var target = $("#" + targetId);

    $(target).scrollTop(target.get(0).scrollHeight);
}

$('#btn-chat').on('click', function() {
    var text = $('#btn-input').val();
    var msg = {action: 'robot_talk', data: text};

    $('#btn-input').val('');
    sendAction(msg);
    add_text_to_chat(text, false);
    scrollBottom('chat');
})

$('#btn-input').keypress(function(e) {
    if (e.which == 13) {
        var text = $(this).val();
        var msg = {action: 'robot_talk', data: text};

        $(this).val('');
        sendAction(msg);
        add_text_to_chat(text, false);
        scrollBottom('chat');
    }
})