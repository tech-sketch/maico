var Vm = null;
var Connector = {
    socket: null,
    begin: function (url) {
        Connector.socket = new ReconnectingWebSocket(url, null, { reconnectInterval: 3000 });
        Connector.socket.onmessage = function (event) {
            var log = JSON.parse(event.data);
            Vm.updateHuman(log);
        }
    },
    send: function (human, action, status) {
        var data = {
            "human_id": human.human_id,
            "action": action,
            "status": status ? 1 : 0
        }

        Connector.socket.send(JSON.stringify(data));
    }

}


$(function () {
    ChartSet.RANGE = 100;
    Vue.config.delimiters = ["[[", "]]"]
    Vue.component("human-observation", {
        props: ["h"],
        data: function(){
            return {
                first_action: false
            }
        },
        template: "#human-observation-template",
        attached: function () {
            this.$dispatch("readyHuman", this.h);
        },
        methods: {
            toggle_first_action: function () {
                this.first_action = !this.first_action; //toggle
                this.$dispatch("annotate", this.h, "first_action", this.first_action);
            }
        }
    });
    Vm = new Vue({
        el: "#dashboard",
        data: {
            humans: []
        },
        methods: {
            updateHuman: function (data) {
                var _id = data.human_id;
                var human = this.getHuman(_id);
                if (human == null) {
                    human = new HumanTracking(_id, [data.d]);
                    this._latest = human;
                    this.humans.push(human);
                } else {
                    if (human.rendered) {
                        human.update(data.d);
                    } else {
                        human.initial.push(data.d);
                    }
                }
            },
            getHuman: function (human_id) {
                var result = null;
                for (var i = 0; i < this.humans.length; i++) {
                    if (this.humans[i].human_id === human_id) {
                        result = this.humans[i];
                        break;
                    }
                }
                return result;
            }
        },
        events: {
            readyHuman: function (h) {
                h.render();
                if (h.initial.length > 0) {
                    for (var i = 0; i < h.initial.length; i++) {
                        h.update(h.initial[i]);
                    }
                    h.initial = [];
                }
            },
            annotate: function (h, action, status) {
                Connector.send(h, action, status);
            }
        }
    })

    if (LOGS) {
        for (var i = 0; i < LOGS.length; i++) {
            Vm.updateHuman(JSON.parse(LOGS[i]));
        }
    }
    Connector.begin("ws://" + location.host + "/monitor");
    //testRender();
})

