
const PLAYER_ICON = 'X';
var grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];
var winner = ' ';

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function play(id) {
  if (document.getElementById(id).innerHTML.trim() != "" || winner != ' ') {
    ;
  }
  else {
    grid[id] = PLAYER_ICON;
    document.getElementById(id).innerHTML = PLAYER_ICON;

    $.ajax({
      type: "POST",
      url: djangoUrl,
      data: JSON.stringify({ grid:grid }),
      success: function(data, textStatus, XmlHttpRequest) {
           grid = data.grid
           winner = data.winner
           render(grid)
       },
      dataType: "json",
      traditional: true
    });
  }

  function render(grid) {
    for (var i = 0; i < grid.length; i++) {
      document.getElementById(i).innerHTML = grid[i];
      if (winner != ' ') {
        var winner_div = document.createElement('div');
        winner_div.id = 'winner_div';
        document.getElementsByTagName('body')[0].appendChild(winner_div);
        document.getElementById('winner_div').innerHTML = winner + " won!";
      }
    }
  }
}