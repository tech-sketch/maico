var socket = new WebSocket('ws://' + location.host + '/controller');
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
  if (data['action'] == 'pepper_eye'){
    var b64_img = data['data'];
    $("#pepper_eye").attr("src", b64_img);
  }
}

$('#move_left').on('click', function(){
  console.log('move_left');
  var msg = {action: 'robot_action', data: 'move_left'};
  sendAction(msg);
})

$('#move_front').on('click', function(){
  console.log('move_front');
  var msg = {action: 'robot_action', data: 'move_front'};
  sendAction(msg);
})

$('#move_right').on('click', function(){
  console.log('move_right');
  var msg = {action: 'robot_action', data: 'move_right'};
  sendAction(msg);
})

$('#move_back').on('click', function(){
  console.log('move_back');
  var msg = {action: 'robot_action', data: 'move_back'};
  sendAction(msg);
})

$('#turn_left').on('click', function(){
  console.log('turn_left');
  var msg = {action: 'robot_action', data: 'move_round90_left'};
  sendAction(msg);
})

$('#turn_right').on('click', function(){
  console.log('turn_right');
  var msg = {action: 'robot_action', data: 'move_round90_right'};
  sendAction(msg);
})

$('#turn_around_left').on('click', function(){
  console.log('turn_around_left');
  var msg = {action: 'robot_action', data: 'move_round180_left'};
  sendAction(msg);
})

$('#turn_around_right').on('click', function(){
  console.log('turn_around_right');
  var msg = {action: 'robot_action', data: 'move_round180_right'};
  sendAction(msg);
})

$('#rotation').on('click', function(){
  console.log('rotation');
  var msg = {action: 'robot_action', data: 'move_round'};
  sendAction(msg);
})

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

$('.product_img').on('click', function(){
  var src = $(this).attr('src');
  var msg = {action: 'product_img', data: src};
  sendAction(msg);
})