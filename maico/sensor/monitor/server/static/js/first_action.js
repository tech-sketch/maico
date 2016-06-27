var Vm = null;

$(function () {
    var chartDef = {
        moving_rate: {
            series: {
                mean_moving_rate: true,
                mean_stopping_rate: true
            },
            skip: 3,
            limit: 1
        },
        speed: {
            series: { mean_moving_speed: true },
            skip: 3
        },
        prediction: {
            series: {
                probability: true,
                execution: true,
                execution_fb: { color: COLORS[2] }
            },
            skip: 3,
            limit: 1
        }
    }

    var makeFeedback = function (feedback_switch, feedback_template) {
        if(feedback_switch){
            feedback_template.execution = 1;        
        }else{
            feedback_template.execution = 0;
        }
        return feedback_template;
    }

    ChartSet.RANGE = 100;
    Vm = buildViewModel("#dashboard", "#target-tracker-template", chartDef, makeFeedback);
    if (INITIAL_DATA) {
        for (var i = 0; i < INITIAL_DATA.length; i++) {
            Vm.updateTracker(JSON.parse(INITIAL_DATA[i]));
        }
    }
    Connector.begin("ws://" + location.host + "/monitor");

})

