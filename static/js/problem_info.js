var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function LineBreakDescription(props) {
    var description = props.description;
    var descriptions = description.split("\n");
    var descriptionObject = [];
    for (var i = 0; i < descriptions.length; i++) {
        var descriptionLine = React.createElement(
            "p",
            { id: "description", "class": "py-1" },
            " ",
            descriptions[i],
            " "
        );
        descriptionObject.push(descriptionLine);
    }
    return descriptionObject;
}

var App = function (_React$Component) {
    _inherits(App, _React$Component);

    function App(props) {
        _classCallCheck(this, App);

        var _this = _possibleConstructorReturn(this, (App.__proto__ || Object.getPrototypeOf(App)).call(this, props));

        _this.state = {
            basic_setting: undefined,
            problem_content: undefined,
            complete_third_party_render: false
        };
        _this.fecthProblemID = _this.fecthProblemID.bind(_this);
        return _this;
    }

    _createClass(App, [{
        key: "fecthProblemID",
        value: function fecthProblemID() {
            var pathname = window.location.pathname;
            var problemID = pathname.split("/")[2];

            return problemID;
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            var problemID = this.fecthProblemID();
            $.ajax({
                url: "/api/problem/" + problemID,
                type: "GET",
                success: function (data, status, xhr) {
                    document.title = "NuOJ - " + data["content"]["title"];
                    this.setState({
                        basic_setting: data["setting"],
                        problem_content: data["content"]
                    });
                }.bind(this)
            });
        }
    }, {
        key: "componentDidUpdate",
        value: function componentDidUpdate() {
            if (this.state.complete_third_party_render === false) {
                MathJax.typesetPromise();
                var textarea = document.getElementById("code_area");
                editor = CodeMirror.fromTextArea(textarea, {
                    lineNumbers: true,
                    matchBrackets: true,
                    mode: "text/x-c++src",
                    theme: "darcula"
                });
                this.setState({ editor: editor, complete_third_party_render: true });
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _state = this.state,
                problem_content = _state.problem_content,
                basic_setting = _state.basic_setting;

            if (problem_content != undefined) {
                return React.createElement(
                    "div",
                    null,
                    React.createElement(
                        "div",
                        { "class": "flex gap-10" },
                        React.createElement(
                            "div",
                            { "class": "w-3/4 mx-auto h-fit rounded border-2 shadow flex flex-col p-10 gap-10 bg-white" },
                            React.createElement(
                                "div",
                                { "class": "text-center" },
                                React.createElement(
                                    "p",
                                    { id: "title", "class": "text-4xl font-medium my-2" },
                                    " ",
                                    problem_content["title"],
                                    " "
                                ),
                                React.createElement(
                                    "p",
                                    { id: "TL-text", "class": "text-lg font-medium my-2" },
                                    " \u7A0B\u5F0F\u904B\u884C\u6642\u9593\u9650\u5236\uFF08TL\uFF09\uFF1A",
                                    basic_setting["time_limit"],
                                    " \u79D2"
                                ),
                                React.createElement(
                                    "p",
                                    { id: "ML-text", "class": "text-lg font-medium my-2" },
                                    " \u7A0B\u5F0F\u904B\u884C\u6642\u9593\u9650\u5236\uFF08ML\uFF09\uFF1A",
                                    basic_setting["memory_limit"],
                                    " MB"
                                )
                            ),
                            React.createElement(
                                "div",
                                null,
                                React.createElement(
                                    "p",
                                    { "class": "text-xl font-semibold my-5" },
                                    "\u984C\u76EE\u6558\u8FF0"
                                ),
                                React.createElement(LineBreakDescription, { description: problem_content["description"] })
                            ),
                            React.createElement(
                                "div",
                                null,
                                React.createElement(
                                    "p",
                                    { "class": "text-xl font-semibold my-5" },
                                    "\u8F38\u5165\u8AAA\u660E"
                                ),
                                React.createElement(LineBreakDescription, { description: problem_content["input_description"] })
                            ),
                            React.createElement(
                                "div",
                                null,
                                React.createElement(
                                    "p",
                                    { "class": "text-xl font-semibold my-5" },
                                    "\u8F38\u51FA\u8AAA\u660E"
                                ),
                                React.createElement(LineBreakDescription, { description: problem_content["output_description"] })
                            ),
                            React.createElement("div", null),
                            React.createElement(
                                "div",
                                null,
                                React.createElement(
                                    "p",
                                    { "class": "text-xl font-semibold my-5" },
                                    "\u5099\u8A3B"
                                ),
                                React.createElement(LineBreakDescription, { description: problem_content["note"] })
                            )
                        )
                    ),
                    ",",
                    React.createElement(
                        "div",
                        { "class": "w-3/4 mx-auto border-2 text-lg flex flex-col gap-10 p-10 shadow bg-white" },
                        React.createElement("textarea", { id: "code_area", "class": "resize-none w-full h-20" }),
                        React.createElement(
                            "button",
                            { "class": "bg-blue-700 w-full delay-50 p-2 hover:bg-blue-500 rounded text-white text-2xl", onclick: "submit_code()" },
                            " \u63D0\u4EA4 "
                        )
                    )
                );
            }
        }
    }]);

    return App;
}(React.Component);

var app = ReactDOM.createRoot(document.getElementById("app"));
app.render(React.createElement(App, null));