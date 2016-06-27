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
  console.log(data);
  var action = data['action'];
  if (action == 'pepper_eye'){
    var b64_img = data['data'];
    $("#pepper_eye").attr("src", b64_img);
  }
  else if (action == 'update_chart') {
    if (chart_data.length > 30) {
        chart_data.shift();
    }
    chart_data.push(data['data']);
    chart.setData(chart_data);
  //console.log(chart.data);
   // chart.setData([data['data']]);
  }
}

$('#submit_access_token').on('click', function(){
  console.log('access_token');
  var access_token = $('#access_token').val();
  $('#access_token').val('');
  var msg = {action: 'send_access_token', data: access_token};
  sendAction(msg);
})

$('#access_token').keypress(function(e){
  if (e.which == 13) {
    var access_token = $(this).val();
    $(this).val('');
    console.log(access_token);
    var msg = {action: 'send_access_token', data: access_token};
    sendAction(msg);
  }
})

$('#submit_text').on('click', function(){
  var text = $('#say_text').val();
  $('#say_text').val('');
  console.log(text);
  var msg = {action: 'robot_talk', data: text};
  sendAction(msg);
})

$('#say_text').keypress(function(e){
  if (e.which == 13) {
    var text = $(this).val();
    $(this).val('');
    console.log(text);
    var msg = {action: 'robot_talk', data: text};
    sendAction(msg);
  }
})