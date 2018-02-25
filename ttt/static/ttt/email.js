
// Submit the form using AJAX.
$.ajax({
    type: 'POST',
    url: verifyUrl,
    data: "JSON",
    success: function (data) {
        console.log(data);
    },
});