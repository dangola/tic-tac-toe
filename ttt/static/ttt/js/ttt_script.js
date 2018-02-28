const PLAYER_ICON = 'X';
var username;

$(function () {
    var winner = ' ';
    var grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];

    $('.signup-redirect').click(function() {
      renderSignupPage();
    });

    $('.login-redirect').click(function() {
      renderLoginPage();
    });

    $('button.endgame-dialogue').click(function() {
      flush();
    });

    $('td').click(function(){
      play(this.id);
    });

    $('button.logout').click(function(){
      $.ajax({
        type: "POST",
        url: '/ttt/logout',
        success: function(data, textStatus, XmlHttpRequest) {
          if (data.status == 'OK') {
            flush();
            renderLoginPage();
            username = null;
          }
          else
            console.log('There was an error in logging out.');
        },
        dataType: "json",
        traditional: true
      });
    });

    $('button.verify').click(function() {
      $.ajax({
        type: "POST",
        url: '/ttt/verify',
        contentType: 'application/json',
        data: JSON.stringify({ email:username, key:'abracadabra'}),
        success: function(data, textStatus, XmlHttpRequest) {
          if (data.status == 'OK')
            renderPlayPage();
          else
            console.log('There was an error verifying your account');
        }
      });
    });

    $('form.login-form').on('submit', function(event){
      event.preventDefault();
      var temp = $(this).serializeArray()[0].value;
      $.ajax({
        type: 'POST',
        url: '/ttt/login',
        contentType: 'application/json',
        data: JSON.stringify($(this).serializeArray().reduce(
          (obj, field) => {
            obj[field.name] = field.value;
            return obj;
          },{})),
        success: function(data, textStatus, XmlHttpRequest) {
          username = temp;
          if (data.status == 'OK') {
            renderPlayPage();
          }
          else
            renderVerifyPage();
        },
        dataType: "json",
        traditional: true
      });
      return false;
    });

    $('form.register-form').on('submit', function(event){
      event.preventDefault();
      var temp = $(this).serializeArray()[0].value;
      $.ajax({
        type: 'POST',
        url: '/ttt/adduser',
        contentType: 'application/json',
        data: JSON.stringify($(this).serializeArray().reduce(
          (obj, field) => {
            obj[field.name] = field.value;
            return obj;
          },{})),
        success: function(data, textStatus, XmlHttpRequest) {
          if (data.status == 'OK') {
            username = temp;
            renderVerifyPage();
          }
          else
            console.log('There was an error in creating your account.');
        },
        dataType: "json",
        traditional: true
      });
      return false;
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
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

    function renderLoginPage() {
      $('.container .page').hide();
      $('.login-page').show();
    }

    function renderSignupPage() {
      $('.container .page').hide();
      $('.signup-page').show();
    }

    function renderPlayPage() {
      $('.container .page').hide();
      $('.play-page').show();
    }

    function renderVerifyPage() {
      $('.container .page').hide();
      $('.verify-page').show();
    }

    function renderGrid(grid) {
      for (var i = 0; i < grid.length; i++) {
        document.getElementById(i).innerHTML = grid[i];
      }
    }

    function renderEndGame(winner) {
      if (winner != ' ')
        $('div.endgame-dialogue').html(winner + ' won!');
      else
        $('div.endgame-dialogue').html('Nobody won. It was a draw!');
      $('.endgame-dialogue').show();
    }

    function flush() {
      winner = ' ';
      grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];
      renderGrid(grid);
      $('.endgame-dialogue').hide();
    }

    function play(id) {
      function checkGameEnded(grid, winner) {
        if (winner != ' ') {
          return true;
        }
        else {
          for (var i = 0; i < grid.length; i++)
            if (grid[i] == ' ')
              return false;
          return true;
        }
      }

      if (document.getElementById(id).innerHTML.trim() != "" || winner != ' ') {;}   // Ignore if grid box contains a move or if winner is decided
      else {
        document.getElementById(id).innerHTML = PLAYER_ICON;
        id = parseInt(id, 10);
        var arr = {"move":id};
        $.ajax({
          type: "POST",
          url: '/ttt/play',
          contentType: 'application/json',
          data: JSON.stringify(arr),
          success: function(data, textStatus, XmlHttpRequest) {
            grid = data.grid
            winner = data.winner
            renderGrid(grid)
            if (checkGameEnded(grid, winner))
              renderEndGame(winner);
          },
          dataType: "json",
          traditional: true
        });
      }
    };

    var sessionid = getCookie('sessionid')
    if (sessionid == null) {
      renderLoginPage();
    }
    else {
      renderPlayPage();
    }
});