var socket;
var namespace = '/oj_socket';
$(document).ready(function() {
  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  socket.on('connect', function() {
    console.log('SocketIO connected');
    socket.emit('inited', $('#username').text());
  });
  socket.on('add', function(data) {
    $('#data').append(htmlize(data));
  });
});

function htmlize(data) {
  s = '';
  for (var oj in data) {
    s += '<h4>' + oj + '</h4>';
    if (data[oj].error != undefined)
      s += '<p>' + data[oj].error + '</p>';
    else
      s += '<p>Solved :' + data[oj].solved + ', Attempts: ' + data[oj].attempts + '</p>';
  }
  return s;
}
