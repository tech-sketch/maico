var COLORS = [
    { // blue
        backgroundColor: "rgba(151,187,205,0.2)",
        borderColor: "rgba(151,187,205,1)",
        pointBackgroundColor: "rgba(151,187,205,1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(151,187,205,0.8)"
    },
    { // light grey
        backgroundColor: "rgba(220,220,220,0.2)",
        borderColor: "rgba(220,220,220,1)",
        pointBackgroundColor: "rgba(220,220,220,1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(220,220,220,0.8)"
    },
    { // red
        backgroundColor: "rgba(247,70,74,0.2)",
        borderColor: "rgba(247,70,74,1)",
        pointBackgroundColor: "rgba(247,70,74,1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(247,70,74,0.8)"
    },
    { // green
        backgroundColor: "rgba(70,191,189,0.2)",
        borderColor: "rgba(70,191,189,1)",
        pointBackgroundColor: "rgba(70,191,189,1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(70,191,189,0.8)"
    },
    { // yellow
        backgroundColor: "rgba(253,180,92,0.2)",
        borderColor: "rgba(253,180,92,1)",
        pointBackgroundColor: "rgba(253,180,92,1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(253,180,92,0.8)"
    },
    { // grey
        backgroundColor: "rgba(148,159,177,0.2)",
        borderColor: "rgba(148,159,177,1)",
        pointBackgroundColor: "rgba(148,159,177,1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(148,159,177,0.8)"
    },
    { // dark grey
        backgroundColor: "rgba(77,83,96,0.2)",
        borderColor: "rgba(77,83,96,1)",
        pointBackgroundColor: "rgba(77,83,96,1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(77,83,96,1)"
    }
];


var ChartSet = (function () {
    function ChartSet(chart, config) {
        this.chart = chart;
        this.config = config;
    }
    ChartSet.COLORS = COLORS;
    ChartSet.RANGE = 50;
    ChartSet.prototype.getLabels = function () {
        return this.config.data.labels;
    }
    ChartSet.prototype.getSeries = function (name) {
        ref = null;
        for (var i = 0; i < this.config.data.datasets.length; i++) {
            if (name === this.config.data.datasets[i].label) {
                ref = this.config.data.datasets[i];
                break;
            }
        }
        return ref;
    }
    ChartSet.prototype.addData = function (json, label) {
        var isOverflow = false;
        var labels = this.getLabels();

        //auto generate label
        var label_push = function (t) {
            if (t !== undefined) {
                labels.push(t)
            } else {
                if (labels.length == 0) {
                    labels.push(0);
                } else {
                    var n = labels[labels.length - 1] + 1;
                    labels.push(n);
                }
            }
        }

        //add data to dataset
        for (k in json) {
            s = this.getSeries(k);
            if (s != null) {
                s.data.push(json[k]);
                if (s.data.length > ChartSet.RANGE) {
                    isOverflow = true;
                    s.data.shift(); // remove first data
                }
            }
        }

        label_push(label);
        if (isOverflow) {
            labels.shift();
        }
    }

    ChartSet.create = function (canvas_id, chartName, chartDef) {
        // get canvas
        var canvas = document.getElementById(canvas_id);
        var ctx = document.getElementById(canvas_id).getContext("2d");
        
        // get prop if defined
        var getProp = function (key, defaultValue) {
            if (key in chartDef) {
                return chartDef[key];
            } else {
                //if defaultValue is missing, return undefined
                return defaultValue;
            }
        }

        var chartType = getProp("chartType", "line");
        var title = getProp("title", chartName);
        var axisName = getProp("axisName", chartName);
        var series = chartDef.series;

        // create labels
        var labels = [];
        /*
        for (var r = 1; r <= ChartSet.RANGE; r++) {
            labels.push("");
        }*/

        // create chart config
        var defaultConfig = {
            type: chartType,
            data: {
                labels: labels,
                datasets: []
            },
            options: {
                responsive: true,
                legend: {
                    position: "bottom",
                },
                hover: {
                    mode: 'label'
                },
                scales: {
                    xAxes: [{
                        display: true,
                        type: "time",
                        time: {
                            unit: "second",
                            displayFormats: {
                                "millisecond": "mm:ss.SSS",
                                "second": "mm:ss",
                                "minute": "mm:ss",
                                "hour": "HH:mm:ss"
                            },
                            tooltipFormat: "HH:mm:ss.SSS"
                        },
                        ticks: {
                        },
                        scaleLabel: {
                            display: true,
                            labelString: "elapse"
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: axisName
                        },
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                title: {
                    display: true,
                    text: title
                }
            }
        }

        // add series
        var index = 0;
        for (var s in series) {
            if (!series[s]) {
                continue;
            }

            var color = null;
            if (series[s].color !== undefined) {
                color = series[s].color;
            } else {
                var colorIndex = index % ChartSet.COLORS.length;
                var color = ChartSet.COLORS[colorIndex];
            }

            defaultConfig.data.datasets.push({
                label: s,
                data: [],
                fill: false,
                backgroundColor: color.backgroundColor,
                borderColor: color.borderColor,
                pointBackgroundColor: color.pointBackgroundColor,
                pointBorderColor: color.pointBorderColor,
                pointHoverBackgroundColor: color.pointHoverBackgroundColor,
                pointHoverBorderColor: color.pointHoverBorderColor
            });
            index++;
        }

        if (getProp("limit") !== undefined) {
            defaultConfig.options.scales.yAxes[0].ticks.max = getProp("limit");
        }
        if (getProp("skip") !== undefined) {
            defaultConfig.options.scales.xAxes[0].ticks.userCallback = (function (s) {
                return function (dataLabel, index) {
                    return index % s === 0 ? dataLabel : "";
                }
            })(getProp("skip"));
        }

        var chart = new Chart(ctx, defaultConfig);
        var config = defaultConfig;
        return new ChartSet(chart, config);
    }

    return ChartSet;
}());


var TargetTracker = (function () {
    function TargetTracker(target_id, chartDef, initial) {
        this._id = target_id;
        this.initial = (initial === undefined) ? [] : initial;
        this.rendered = false;
        this.track_begin = moment();
        this.chartDef = chartDef
        this.charts = {};
    };
    TargetTracker.prototype.isMine = function (data) {
        return (data._id === this._id) ? true : false;
    };
    TargetTracker.prototype.render = function () {
        for (var key in this.chartDef) {
            if (!(key in this.charts)) {
                var _id = this._id + "_" + key;
                var canvas = document.getElementById(_id);
                if (canvas) {
                    var chartSet = ChartSet.create(_id, key, this.chartDef[key]);
                    this.charts[key] = chartSet;
                }
            }
        }
        this.rendered = true;
    };

    TargetTracker.prototype.getElapse = function () {
        var elapse = moment().diff(this.track_begin);
        return elapse
    }
    TargetTracker.prototype.update = function (protocol) {
        var prediction = protocol.prediction;
        var feedback = protocol.feedback;
        var elapse = this.getElapse();

        //show feature attributes
        var feature = protocol.feature;
        for (var key in this.charts) {
            if (key != "prediction") {
                this.charts[key].addData(feature["attributes"]);
                this.charts[key].chart.update();
            }
        }

        // prediction and feedback
        p_and_f = {}
        for (var k in protocol.prediction) {
            p_and_f[k] = protocol.prediction[k]
        }
        for (var k in protocol.feedback) {
            if (protocol.feedback[k] !== null) {
                p_and_f[k + "_fb"] = protocol.feedback[k];
            }
        }

        this.charts["prediction"].addData(p_and_f);
        this.charts["prediction"].chart.update();

    };

    return TargetTracker;
}());
