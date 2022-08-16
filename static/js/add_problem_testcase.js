var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Testcase_Component = function (_React$Component) {
    _inherits(Testcase_Component, _React$Component);

    function Testcase_Component(props) {
        _classCallCheck(this, Testcase_Component);

        var _this = _possibleConstructorReturn(this, (Testcase_Component.__proto__ || Object.getPrototypeOf(Testcase_Component)).call(this, props));

        _this.state = { testcase: props.testcase, trigger_event_list: {} };
        _this.componentClose = _this.componentClose.bind(_this);
        return _this;
    }

    _createClass(Testcase_Component, [{
        key: "componentClose",
        value: function componentClose(name) {
            console.log("trigger");
            if (document.getElementById(name).classList.contains("h-0")) {
                document.getElementById(name).classList.remove("h-0");
                document.getElementById(name).classList.add("h-[19vh]");
            } else {
                document.getElementById(name).classList.remove("h-[19vh]");
                document.getElementById(name).classList.add("h-0");
            }
        }
    }, {
        key: "componentDidUpdate",
        value: function componentDidUpdate() {
            var _this2 = this;

            var _state = this.state,
                testcase = _state.testcase,
                trigger_event_list = _state.trigger_event_list;

            for (var i = 0; i < testcase.length; i++) {
                document.getElementById("testcase-" + (i + 1)).removeEventListener("click", trigger_event_list[i]);
            }

            var _loop = function _loop(_i) {
                var trigger = function trigger() {
                    _this2.componentClose("data-" + (_i + 1));
                };
                document.getElementById("testcase-" + (_i + 1)).addEventListener("click", trigger);
                trigger_event_list[_i] = trigger;
            };

            for (var _i = 0; _i < testcase.length; _i++) {
                _loop(_i);
            }
        }
    }, {
        key: "render",
        value: function render() {
            var testcase = this.state.testcase;

            if (testcase.length === 0) {
                return React.createElement(
                    "div",
                    { id: "no_solution_current", "class": "my-5 p-5 border-2 rounded-lg" },
                    React.createElement(
                        "p",
                        { "class": "text-center" },
                        " \u76EE\u524D\u9084\u6C92\u6709\u6E2C\u8A66\u8CC7\u6599\uFF0C\u9EDE\u64CA\u4E0B\u65B9\u300C\u65B0\u589E\u6E2C\u8A66\u8CC7\u6599\u300D\u6309\u9215\u4F86\u65B0\u589E\u4E00\u500B\u6E2C\u8A66\u8CC7\u6599 "
                    )
                );
            } else {
                testcase_component_list = [];
                for (var i = 0; i < testcase.length; i++) {
                    var component = React.createElement(
                        "div",
                        { className: "my-5 p-5 border-2 rounded-lg " },
                        React.createElement(
                            "p",
                            { id: "testcase-" + (i + 1), className: "text-center text-lg hover:bg-slate-200 p-5 cursor-pointer" },
                            " \u6E2C\u8A66\u8CC7\u6599 ",
                            i + 1,
                            " "
                        ),
                        React.createElement(
                            "div",
                            { id: "data-" + (i + 1), className: "w-full flex flex-row h-0 overflow-hidden transition-all duration-500" },
                            React.createElement(
                                "div",
                                { className: "w-[30%] p-5" },
                                React.createElement("textarea", { className: "w-full h-[15vh] bg-slate-200 resize-none p-5 font-mono", value: testcase[i]["input"], readOnly: true })
                            ),
                            React.createElement(
                                "div",
                                { className: "w-[30%] p-5" },
                                React.createElement("textarea", { className: "w-full h-[15vh] bg-slate-200 resize-none p-5 font-mono", value: testcase[i]["output"], readOnly: true })
                            ),
                            React.createElement(
                                "div",
                                { className: "w-[40%] p-5 flex flex-col gap-5 justify-center relative" },
                                React.createElement(
                                    "button",
                                    { "class": "bg-orange-500 text-white transition-colors duration-200 hover:bg-orange-400 w-full p-3 text-lg rounded-lg" },
                                    " \u4FEE\u6539\u6E2C\u8A66\u8CC7\u6599 "
                                ),
                                React.createElement(
                                    "button",
                                    { "class": "bg-red-500 text-white transition-colors duration-200 hover:bg-red-400 w-full p-3 text-lg rounded-lg" },
                                    " \u522A\u9664\u6E2C\u8A66\u8CC7\u6599 "
                                )
                            )
                        )
                    );
                    testcase_component_list.push(component);
                }
                return testcase_component_list;
            }
        }
    }]);

    return Testcase_Component;
}(React.Component);

var App = function (_React$Component2) {
    _inherits(App, _React$Component2);

    function App(props) {
        _classCallCheck(this, App);

        var _this3 = _possibleConstructorReturn(this, (App.__proto__ || Object.getPrototypeOf(App)).call(this, props));

        _this3.state = { testcase: [] };
        _this3.add_test_case = _this3.add_test_case.bind(_this3);
        _this3.save_test_case = _this3.save_test_case.bind(_this3);
        return _this3;
    }

    _createClass(App, [{
        key: "add_test_case",
        value: function add_test_case() {
            document.getElementById("add_testcase_platform").classList.remove("top-[100%]");
            document.getElementById("add_testcase_platform").classList.add("top-0");
        }
    }, {
        key: "save_test_case",
        value: function save_test_case() {
            var testcase = this.state.testcase;
            // Get Testcase

            var input = document.getElementById("testcase").value;
            var output = document.getElementById("answer").value;
            testcase.push({ "input": input, "output": output });
            this.setState({ testcase: testcase });
            // Clean Testcase
            document.getElementById("testcase").value = "";
            document.getElementById("answer").value = "";
            // Finish Save Testcase
            document.getElementById("add_testcase_platform").classList.add("top-[100%]");
            document.getElementById("add_testcase_platform").classList.remove("top-0");
        }
    }, {
        key: "render",
        value: function render() {
            var testcase = this.state.testcase;

            return [React.createElement(
                "div",
                { "class": "z-20 flex flex-col" },
                React.createElement(AddProblemToolbar, null)
            ), React.createElement(
                "div",
                { id: "main_platform", "class": "relativ mx-auto w-[70%] bg-white h-screen flex" },
                React.createElement(
                    "div",
                    { "class": "w-screen p-10" },
                    React.createElement(
                        "p",
                        { "class": "font-bold text-5xl mt-5 text-left" },
                        " \u6E2C\u8CC7\u8A2D\u5B9A "
                    ),
                    React.createElement(
                        "div",
                        { id: "testcase_area", className: "max-h-[50vh] overflow-y-auto my-5 border-2 px-5" },
                        React.createElement(Testcase_Component, { testcase: testcase })
                    ),
                    React.createElement(
                        "div",
                        { className: "flex flex-col gap-5" },
                        React.createElement(
                            "div",
                            { className: "flex flex-row gap-5" },
                            React.createElement(
                                "button",
                                { "class": "bg-amber-500 text-white transition-colors duration-200 hover:bg-amber-400 w-full p-3 text-lg rounded-lg", onClick: this.add_test_case },
                                " \u65B0\u589E\u6E2C\u8A66\u8CC7\u6599 "
                            ),
                            React.createElement(
                                "button",
                                { "class": "bg-teal-500 text-white transition-colors duration-200 hover:bg-teal-400 w-full p-3 text-lg rounded-lg", onClick: this.add_test_case },
                                " \u4E0A\u50B3\u6E2C\u8A66\u8CC7\u6599 "
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "flex flex-col gap-5" },
                            React.createElement(
                                "button",
                                { "class": "bg-gray-500 transition-colors duration-200 w-full p-3 text-lg rounded-lg text-gray-300", disabled: true },
                                " \u4E0A\u50B3\u6E2C\u8A66\u8CC7\u6599\u58D3\u7E2E\u6A94 "
                            ),
                            React.createElement(
                                "button",
                                { "class": "bg-gray-500 transition-colors duration-200 w-full p-3 text-lg rounded-lg text-gray-300", disabled: true },
                                " \u5229\u7528\u6E2C\u8CC7\u7522\u751F\u5668\u65B0\u589E\u8CC7\u6599 "
                            )
                        )
                    )
                )
            ), React.createElement(
                "div",
                { id: "add_testcase_platform", className: "w-screen h-screen bg-black bg-opacity-50 absolute top-[100%] transition-all duration-500" },
                React.createElement(
                    "div",
                    { className: "absolute top-[50%] left-[50%] p-5 translate-x-[-50%] translate-y-[-50%] bg-white w-[50%] h-fit rounded-lg" },
                    React.createElement(
                        "p",
                        { className: "text-center text-2xl pb-5" },
                        " \u65B0\u589E\u6E2C\u8A66\u8CC7\u6599 "
                    ),
                    React.createElement(
                        "div",
                        { className: "flex flex-row gap-5" },
                        React.createElement(
                            "div",
                            { className: "w-full h-fit border-2 rounded-xl p-5" },
                            React.createElement(
                                "p",
                                { className: "text-center text-xl pb-5" },
                                " \u6E2C\u8A66\u8CC7\u6599 "
                            ),
                            React.createElement("textarea", { id: "testcase", className: "bg-slate-200 h-[30vh] w-full resize-none font-mono text-lg p-5" })
                        ),
                        React.createElement(
                            "div",
                            { className: "w-full h-fit border-2 rounded-xl p-5" },
                            React.createElement(
                                "p",
                                { className: "text-center text-xl pb-5" },
                                " \u89E3\u7B54 "
                            ),
                            React.createElement("textarea", { id: "answer", className: "bg-slate-200 h-[30vh] w-full resize-none font-mono text-lg p-5", placeholder: "\u5982\u679C\u4F60\u60F3\u81EA\u52D5\u751F\u6210\u7B54\u6848\uFF0C\u8ACB\u7559\u7A7A\u3002" })
                        )
                    ),
                    React.createElement(
                        "button",
                        { "class": "bg-amber-500 text-white transition-colors duration-200 hover:bg-amber-400 w-full p-3 text-lg rounded-lg mt-5", onClick: this.save_test_case },
                        " \u65B0\u589E\u6E2C\u8A66\u8CC7\u6599 "
                    )
                )
            )];
        }
    }]);

    return App;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById('app'));
root.render(React.createElement(App, null));