var Connector = {
    socket: null,
    begin: function (url) {
        Connector.socket = new ReconnectingWebSocket(url, null, { reconnectInterval: 3000 });
        Connector.socket.onmessage = function (event) {
            var protocol = JSON.parse(event.data);
            Vm.updateTracker(protocol);
        }
    },
    send: function (payload) {
        Connector.socket.send(JSON.stringify(payload));
    }

}


function buildViewModel(target, template, chartDef, makeFeedback) {

    Vue.config.delimiters = ["[[", "]]"]
    Vue.component("target-tracker", {
        props: ["t"],
        data: function () {
            return {
                feedbacking: false,
            }
        },
        template: template,
        attached: function () {
            this.$dispatch("readyTracker", this.t);
        },
        methods: {
            toggle_feedback: function () {
                this.feedbacking = !this.feedbacking; //toggle
                f_frame = {}
                for (k in this.t.feedback) { //copy struct
                    f_frame[k] = 0;
                }
                f = makeFeedback(this.feedbacking, f_frame);
                this.$dispatch("feedback", this.t, f);
            }
        }
    });

    var vm = new Vue({
        el: target,
        data: {
            trackers: []
        },
        methods: {
            updateTracker: function (protocol) {
                var _id = protocol._id;
                var tracker = this.getTracker(_id);
                if (tracker == null) {
                    tracker = new TargetTracker(_id, chartDef, [protocol]);
                    this.trackers.push(tracker);
                } else {
                    if (tracker.rendered) {
                        tracker.update(protocol);
                    } else {
                        tracker.initial.push(protocol);
                    }
                }
            },
            getTracker: function (target_id) {
                var result = null;
                for (var i = 0; i < this.trackers.length; i++) {
                    if (this.trackers[i]._id === target_id) {
                        result = this.trackers[i];
                        break;
                    }
                }
                return result;
            }
        },
        events: {
            readyTracker: function (t) {
                t.render();
                if (t.initial.length > 0) {
                    for (var i = 0; i < t.initial.length; i++) {
                        t.update(t.initial[i]);
                    }
                    t.initial = [];
                }
            },
            feedback: function (t, feedback) {
                var payload = {
                    "_id": t._id,
                    "feedback": feedback
                }
                Connector.send(payload);
            }
        }
    })

    return vm;
}
