$(document).ready(function () {
    let to_stop_record = true;
    let to_stop_search = false;


    $('#record_switch_btn').click(function () {
        let action;
        let newText;
        if (to_stop_record) {
            action = "stop_record";
            newText = "Start Camera";
        } else {
            action = "start_record";
            newText = "Stop Camera";
        }
        $.ajax({
            url: '/api',
            type: 'GET',
            data: {
                action: action
            },
            success: function (msg) {
                $('#record_switch_btn').text(newText);
                to_stop_record = !to_stop_record;
            }
        });
    });
    $('#search_switch_btn').click(function () {
        let action;
        let newText;
        if (to_stop_search) {
            action = "stop_search";
            newText = "Start Search";
        } else {
            action = "start_search";
            newText = "Stop Search";
        }
        $.ajax({
            url: '/api',
            type: 'GET',
            data: {
                action: action
            },
            success: function (msg) {
                $('#search_switch_btn').text(newText);
                to_stop_search = !to_stop_search;
            }
        });
    });
});


