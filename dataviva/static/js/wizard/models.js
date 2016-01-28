(function () {
    "use strict";

    var app = angular.module("wizard.models", [
        "wizard.remote",
    ]);

    app.service('Question', ["$filter",  function ($filter) {
        return function Question(args) {

            var self = this;
            var defaults = {
                selected: false,
            };
            angular.extend(this, defaults, args);
        }
    }]);

    app.service('Wizard', ["Remote", "$http", "$filter", "Question", function (Remote, $http, $filter, Question) {
        return function Wizard(session_name) {
            var self = this;

            self.session_name = session_name;
            self.selected_question = null;
            self.answers = [];

            /*

            /en/wizard/session/enterpreneur/
                ->return basic questions

            /en/wizard/session/enterpreneur/?q1=1
                ->return locations selector

            /en/wizard/session/enterpreneur/?q1=1&q2=br123
                ->return products selector

            submit
             ns
            if(!next_steps)
                goto_profile()
            */
            self.load = function(){
                console.log("Entering Load()");
                var params = {};

                angular.forEach(self.answers, function(v, idx) {
                    params["op" + (idx + 1)] = v.id;
                });

                $http({
                    method: "GET",
                    url: "/en/wizard/session/" + self.session_name,
                    params: params,
                })
                .success(function(resp){
                    self.title = resp.title;
                    self.questions = resp.questions.map(function(val){
                        console.log(val);
                        return new Question(val);
                    });
                });
            };

            self.select = function(question) {
                if(self.selected_question) {
                    self.selected_question.selected = false;
                }
                question.selected = true;
                self.selected_question = question;
            };

            self.submit = function() {

                console.log("Entering submit");

                self.answers.push(self.selected_question);
                self.selected_question = null;
                self.load();
            };

            self.load();
        }
    }]);
}());
