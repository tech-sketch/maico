var socket = new WebSocket('ws://' + location.host + '/observation');

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
        chart_data.push(data['data']);
        chart.setData(chart_data);
    }
    else if (action == 'user_utt') {
        add_text_to_chat(data['data'], true);
        goBottom('chat');
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

function add_text_to_chat(text, is_left) {

  if (is_left) {
      var tag = '<div class="balloon-wrapper">' +
                  '<img class="avator-img" src="static/images/robot_icon.png" style="float:left;"/>' +
                  '<div class="balloon col s10" style="float:right;">' +
                    '<div class="msg-container">' +
                      text +
                    '</div>' +
                  '</div>' +
                '</div>';
  }
  else {
      var tag = '<div class="balloon-wrapper">' +
                  '<div class="balloon col s10" style="float:left;">' +
                    '<div class="msg-container">' +
                      text +
                    '</div>' +
                  '</div>' +
                  '<img class="avator-img" src="static/images/sayuri.png" style="float:right;"/>' +
                '</div>';
  }
  $('#chat').append(tag);
}

function goBottom(targetId) {
    var target = $("#" + targetId);

    $(target).scrollTop(target.get(0).scrollHeight);
}

$('#submit_text').on('click', function() {
    var text = $('#say_text').val();
    var msg = {action: 'robot_talk', data: text};

    $('#say_text').val('');
    sendAction(msg);
    add_text_to_chat(text, false);
    goBottom('chat');
})

$('#say_text').keypress(function(e) {
    if (e.which == 13) {
        var text = $(this).val();
        var msg = {action: 'robot_talk', data: text};

        $(this).val('');
        sendAction(msg);
        add_text_to_chat(text, false);
        goBottom('chat');
    }
})