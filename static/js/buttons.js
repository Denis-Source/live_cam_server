$(document).ready(function () {
    let captureObj = {
        element: $('#record-switch-btn'),
        state: true,

        startText: "Start Capture",
        stopText: "Stop Capture",
        startAction: "start_capture",
        stopAction: "stop_capture"
    };
    let searchObj = {
        element: $('#search-switch-btn'),
        state: true,

        startText: "Start Search",
        stopText: "Stop Search",
        startAction: "start_search",
        stopAction: "stop_search"
    };

    $.ajax({
        url: '/api',
        type: 'GET',
        data: {
            action: "status"
        },
        success: function (msg) {
            captureObj.state = msg.info.capturing;
            searchObj.state = msg.info.searching;
        },
        complete: function (msg) {
            if (captureObj.state) {
                captureObj.element.text(captureObj.stopText);
            } else {
                captureObj.element.text(captureObj.startText);
            }
            if (searchObj.state) {
                searchObj.element.text(searchObj.stopText);
            } else {
                searchObj.element.text(searchObj.startText);
            }
        }

    });

    function changeButtonText(obj) {
        let action;
        if (obj.state) {
            action = obj.stopAction;
        } else {
            action = obj.startAction;
        }
        $.ajax({
            url: '/api',
            type: 'GET',
            data: {
                action: action
            },
            success: function (msg) {
                let newText;
                obj.state = !obj.state;
                if (obj.state) {
                    newText = obj.stopText;
                } else {
                    newText = obj.startText;
                }
                obj.element.text(newText);
            }
        });
    }

    captureObj.element.click(function () {
        changeButtonText(captureObj);
    });

    searchObj.element.click(function () {
        changeButtonText(searchObj);
    });
});


