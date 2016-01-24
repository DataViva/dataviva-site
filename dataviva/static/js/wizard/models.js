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
            self._build = function(resp) {
                self.title = resp.title;
                self.questions = resp.questions.map(function(val){
                    return new Question(val);
                });
            };

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

            $http({
                method: "GET",
                url: "/en/wizard/session/" + self.session_name,
            })
            .success(function(resp){
                self._build();
            });

            self.get_next = function(){
                var ns = self.selected_question.pop();
                $http({
                    method: "POST",
                    url: "/en/wizard/step/" + ns,
                })
                .success(function(resp){
                    self._build();
                });
            };

            self.select = function(question){
                if(self.selected_question) {
                    self.selected_question.selected = false;
                }
                question.selected = true;
                self.selected_question = question;
            };
        }
    }]);
}());
