$(document).ready(function () {
    let capture_info = {
        start_text: "Start Capture",
        stop_text: "Stop Capture",
        start_action: "start_capture",
        stop_action: "stop_capture"
    };
    let search_info = {
        start_text: "Start Search",
        stop_text: "Stop Search",
        start_action: "start_search",
        stop_action: "stop_search"
    };

    let capture_btn_element = $('#record_switch_btn');
    let search_btn_element = $('#search_switch_btn');

    let to_capture = true;
    let to_search = true;

    $.ajax({
        url: '/api',
        type: 'GET',
        data: {
            action: "status"
        },
        success: function (msg) {
            to_capture = msg.info.capturing;
            to_search = msg.info.searching;
        },
        complete: function (msg) {
            if (to_capture) {
                capture_btn_element.text(capture_info.stop_text);
            } else {
                capture_btn_element.text(capture_info.start_text);
            }

            if (to_search) {
                search_btn_element.text(search_info.stop_text);
            } else {
                search_btn_element.text(search_info.start_text);
            }
        }

    });
    capture_btn_element.click(function () {
        let action;
        if (to_capture) {
            action = capture_info.stop_action;
        } else {
            action = capture_info.start_action;
        }
        $.ajax({
            url: '/api',
            type: 'GET',
            data: {
                action: action
            },
            success: function (msg) {
                let newText;
                to_capture = !to_capture
                if (to_capture) {
                    newText = capture_info.stop_text;
                } else {
                    newText = capture_info.start_text;
                }
                capture_btn_element.text(newText);
            }
        });
    });

    search_btn_element.click(function () {
        let action;
        if (to_search) {
            action = search_info.stop_action;
        } else {
            action = search_info.start_action;
        }
        $.ajax({
            url: '/api',
            type: 'GET',
            data: {
                action: action
            },
            success: function (msg) {
                let newText;
                to_search = !to_search
                if (to_search) {
                    newText = search_info.stop_text;
                } else {
                    newText = search_info.start_text;
                }
                search_btn_element.text(newText);
            }
        });
    });
});


