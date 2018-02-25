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

function contains(arr, elem) {
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] == elem) {
            return true;
        }
    }
    return false;
}

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
      data: JSON.stringify({ grid:grid, move:parseInt(id) }),
      success: function(data, textStatus, XmlHttpRequest) {
           grid = data.grid
           winner = data.winner
           render(grid)
       },
      dataType: "json",
      traditional: true
    });
  }
}

function render(grid) {
    for (var i = 0; i < grid.length; i++) {
      document.getElementById(i).innerHTML = grid[i];
    }

    if (winner != ' ') {
      document.getElementById('winner').innerHTML = winner + " won!";
      document.getElementById('winner').style.visibility = "visible";
      document.getElementById('reset_button').style.visibility = "visible";
      document.getElementById('score').style.visibility = "visible";
    }
    else if (contains(grid, ' ')) {
      ;
    }
    else {
      document.getElementById('winner').innerHTML = "It was a draw! Nobody won.";
      document.getElementById('winner').style.visibility = "visible";
      document.getElementById('reset_button').style.visibility = "visible";
      document.getElementById('score').style.visibility = "visible";
    }
}

function reset() {
    winner = ' ';
    grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];
    render(grid);
    document.getElementById('reset_button').style.visibility = "hidden";
    document.getElementById('winner').style.visibility = "hidden";
    document.getElementById('score').style.visibility = "hidden";
}

function logout() {
  $.ajax({
    type: "POST",
    url: logoutUrl,
    data: JSON.stringify({ username: username }),
    success: function(data, textStatus, XmlHttpRequest) {
      username = username
      $('html').html(data);
    },
    traditional: true
  });
}
