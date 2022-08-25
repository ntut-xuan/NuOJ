var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var SolutionArea = function (_React$Component) {
    _inherits(SolutionArea, _React$Component);

    function SolutionArea(props) {
        _classCallCheck(this, SolutionArea);

        var _this = _possibleConstructorReturn(this, (SolutionArea.__proto__ || Object.getPrototypeOf(SolutionArea)).call(this, props));

        _this.state = {
            solution_data: props.solution_data,
            delete_data: props.delete_data
        };
        _this.expend = _this.expend.bind(_this);
        return _this;
    }

    _createClass(SolutionArea, [{
        key: "expend",
        value: function expend(ID) {
            if ($("#solution_area_" + ID).hasClass("h-0")) {
                $("#solution_area_" + ID).removeClass("h-0");
                $("#solution_area_" + ID).addClass("h-[40vh]");
            } else {
                $("#solution_area_" + ID).removeClass("h-[40vh]");
                $("#solution_area_" + ID).addClass("h-0");
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _this2 = this;

            var _state = this.state,
                solution_data = _state.solution_data,
                delete_data = _state.delete_data;

            if (solution_data.length == 0) {
                return React.createElement(
                    "div",
                    { id: "no_solution_current", "class": "p-5 border-2 rounded-lg" },
                    React.createElement(
                        "p",
                        { "class": "text-center" },
                        " \u76EE\u524D\u9084\u6C92\u6709\u89E3\u7B54\uFF0C\u9EDE\u64CA\u4E0B\u65B9\u300C\u65B0\u589E\u89E3\u7B54\u300D\u6309\u9215\u4F86\u65B0\u589E\u4E00\u500B\u89E3\u7B54 "
                    )
                );
            } else {
                var component_list = [];

                var _loop = function _loop(i) {
                    var component = React.createElement(
                        "div",
                        { id: "card", "class": "p-5 border-2 rounded-lg" },
                        React.createElement(
                            "p",
                            { id: "card_" + (i + 1), value: i + 1, "class": "text-center py-5 cursor-pointer hover:bg-gray-200", onClick: function onClick() {
                                    _this2.expend(i + 1);
                                } },
                            " \u89E3\u7B54 ",
                            i + 1,
                            " "
                        ),
                        React.createElement(
                            "div",
                            { id: "solution_area_" + (i + 1), "class": "h-0 overflow-hidden transition-all duration-500" },
                            React.createElement(
                                "textarea",
                                { id: "code_area_" + (i + 1), "class": "resize-none w-full h-10", readonly: true },
                                solution_data[i]
                            ),
                            React.createElement(
                                "button",
                                { "class": "bg-red-500 text-white transition-colors duration-200 hover:bg-red-400 w-full p-3 text-lg rounded-lg mt-5", onClick: function onClick() {
                                        delete_data(i);
                                    } },
                                " \u522A\u9664 "
                            )
                        )
                    );
                    component_list.push(component);
                };

                for (var i = 0; i < solution_data.length; i++) {
                    _loop(i);
                }
                return component_list;
            }
        }
    }]);

    return SolutionArea;
}(React.Component);

var App = function (_React$Component2) {
    _inherits(App, _React$Component2);

    function App(props) {
        _classCallCheck(this, App);

        var _this3 = _possibleConstructorReturn(this, (App.__proto__ || Object.getPrototypeOf(App)).call(this, props));

        _this3.state = {
            PID: window.location.pathname.split("/")[2],
            solution_editor: [],
            codearea_editor: null,
            solution_data: []
        };
        _this3.cancel = _this3.cancel.bind(_this3);
        _this3.submit = _this3.submit.bind(_this3);
        _this3.add_problem = _this3.add_problem.bind(_this3);
        _this3.delete_data = _this3.delete_data.bind(_this3);
        return _this3;
    }

    _createClass(App, [{
        key: "cancel",
        value: function cancel() {
            $("#dark").removeClass("h-screen");
            $("#dark").removeClass("bottom-0");
            $("#dark").addClass("h-0");
            $("#dark").addClass("bottom-[-100%]");
        }
    }, {
        key: "submit",
        value: function submit() {
            var _state2 = this.state,
                codearea_editor = _state2.codearea_editor,
                solution_data = _state2.solution_data;

            var code = codearea_editor.getValue();
            solution_data.push(code);
            this.cancel();
            this.setState({ solution_data: solution_data });
        }
    }, {
        key: "add_problem",
        value: function add_problem() {
            var solution_data = this.state.solution_data;

            $("#add_problem_title").text("解答設定 #" + (solution_data.length + 1));
            $("#dark").removeClass("h-0");
            $("#dark").removeClass("bottom-[-100%]");
            $("#dark").addClass("bottom-0");
            $("#dark").addClass("h-screen");
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            var codearea_editor = this.state.codearea_editor;

            var setting = {
                lineNumbers: true,
                matchBrackets: true,
                mode: "text/x-c++src",
                theme: "darcula"
            };
            codearea_editor = CodeMirror.fromTextArea(document.getElementById("code_area"), setting);
            codearea_editor.setSize("100%", "100%");
            this.setState({ codearea_editor: codearea_editor });
        }
    }, {
        key: "componentDidUpdate",
        value: function componentDidUpdate() {
            var solution_data = this.state.solution_data;

            var read_only_setting = {
                lineNumbers: true,
                matchBrackets: true,
                mode: "text/x-c++src",
                theme: "darcula",
                readOnly: true
            };
            for (var i = 0; i < solution_data.length; i++) {
                if (document.getElementById("code_area_" + (i + 1)).hasAttribute("style")) {
                    continue;
                }
                codearea_editor = CodeMirror.fromTextArea(document.getElementById("code_area_" + (i + 1)), read_only_setting);
            }
        }
    }, {
        key: "delete_data",
        value: function delete_data(index) {
            var solution_data = this.state.solution_data;

            solution_data.splice(index, 1);
            this.setState({ solution_data: solution_data });
        }
    }, {
        key: "render",
        value: function render() {
            var _state3 = this.state,
                PID = _state3.PID,
                solution_data = _state3.solution_data;

            return [React.createElement(
                "div",
                { "class": "z-20 flex flex-col" },
                React.createElement(AddProblemToolbar, null),
                React.createElement(
                    "div",
                    { "class": "relative w-[70%] mx-auto bg-white min-h-full flex" },
                    React.createElement(
                        "div",
                        { "class": "w-full p-10" },
                        React.createElement(
                            "p",
                            { "class": "font-bold text-5xl m-5 text-left" },
                            " \u89E3\u7B54\u8A2D\u5B9A "
                        ),
                        React.createElement(
                            "div",
                            { className: "border-2 p-5" },
                            React.createElement(SolutionArea, { delete_data: this.delete_data, solution_data: solution_data })
                        ),
                        React.createElement(
                            "button",
                            { "class": "bg-amber-500 text-white transition-colors duration-200 hover:bg-amber-400 w-full p-3 text-lg rounded-lg my-3", onClick: this.add_problem },
                            " \u65B0\u589E\u89E3\u7B54 "
                        ),
                        React.createElement(
                            "button",
                            { id: "compile_button", "class": "enabled:bg-blue-500 disabled:bg-slate-400 text-white transition-colors duration-200 enabled:hover:bg-blue-400 w-full p-3 text-lg rounded-lg my-3", disabled: true },
                            " \u7DE8\u8B6F\u6E2C\u8A66 "
                        ),
                        React.createElement(
                            "button",
                            { id: "save_button", "class": "enabled:bg-green-500 disabled:bg-slate-400 text-white transition-colors duration-200 hover:bg-green-400 w-full p-3 text-lg rounded-lg my-3", disabled: true },
                            " \u5B58\u6A94 "
                        )
                    )
                ),
                React.createElement(
                    "div",
                    { "class": "w-full text-center py-10" },
                    React.createElement(
                        "p",
                        { id: "PID", "class": "italic text-gray-400" },
                        " ",
                        PID,
                        " "
                    )
                )
            ), React.createElement(
                "div",
                { id: "dark", "class": "h-0 overflow-y-hidden absolute left-0 bottom-[-100%] transition-all duration-500 ease-in-out bg-opacity-50 bg-black w-screen z-50" },
                React.createElement(
                    "div",
                    { "class": "absolute bg-white p-5 rounded-lg w-[70%] h-[80vh] left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] flex flex-col" },
                    React.createElement(
                        "div",
                        { className: "w-full relative" },
                        React.createElement(
                            "p",
                            { id: "add_problem_title", "class": "font-bold text-5xl m-5 text-center" },
                            " "
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-full relative h-full flex flex-row gap-5 overflow-hidden" },
                        React.createElement(
                            "div",
                            { className: "w-[80%]" },
                            React.createElement("textarea", { id: "code_area", className: "resize-none h-20" })
                        ),
                        React.createElement(
                            "div",
                            { id: "option", className: "w-[20%] flex flex-col gap-3" },
                            React.createElement(
                                "select",
                                { className: "w-full p-3 text-center border-2 rounded-lg" },
                                React.createElement(
                                    "option",
                                    null,
                                    " \u901A\u904E\u6E2C\u8A66\uFF08AC\uFF09 "
                                ),
                                React.createElement(
                                    "option",
                                    null,
                                    " \u7121\u6CD5\u901A\u904E\u6E2C\u8A66\uFF08WA\uFF09 "
                                ),
                                React.createElement(
                                    "option",
                                    null,
                                    " \u8D85\u6642\uFF08TLE\uFF09 "
                                ),
                                React.createElement(
                                    "option",
                                    null,
                                    " \u8D85\u904E\u8A18\u61B6\u9AD4\u9650\u5236\uFF08MLE\uFF09 "
                                )
                            ),
                            React.createElement(
                                "button",
                                { "class": "bg-amber-500 text-white transition-colors duration-200 hover:bg-amber-400 w-full p-3 text-lg rounded-lg", onClick: this.submit },
                                " \u5B58\u6A94 "
                            ),
                            React.createElement(
                                "button",
                                { "class": "bg-red-500 text-white transition-colors duration-200 hover:bg-red-400 w-full p-3 text-lg rounded-lg", onClick: this.cancel },
                                " \u53D6\u6D88 "
                            )
                        )
                    )
                )
            )];
        }
    }]);

    return App;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById('app'));
root.render(React.createElement(App, null));