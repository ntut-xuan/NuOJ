var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Inputbox = function (_React$Component) {
    _inherits(Inputbox, _React$Component);

    function Inputbox(pro) {
        _classCallCheck(this, Inputbox);

        var _this = _possibleConstructorReturn(this, (Inputbox.__proto__ || Object.getPrototypeOf(Inputbox)).call(this, pro));

        _this.state = {
            key: "",
            value: ""
        };
        _this.onchange = _this.onchange.bind(_this);
        _this.update = _this.update.bind(_this);
        return _this;
    }

    _createClass(Inputbox, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.setState({
                title: this.props.title,
                value: this.props.value
            });
            this.props.new(this.props.title, this.props.value);
        }
    }, {
        key: "onchange",
        value: function onchange(event) {
            this.setState({
                value: event.target.value
            });
        }
    }, {
        key: "update",
        value: function update() {
            this.props.new(this.state.title, this.state.value);
        }
    }, {
        key: "render",
        value: function render() {
            var type;
            if (this.state.title == "about_me") {
                type = React.createElement("textarea", { cols: "30", rows: "5", value: this.state.value, onChange: this.onchange, onBlur: this.update });
            } else {
                type = React.createElement("input", { type: "text", value: this.state.value, onChange: this.onchange, onBlur: this.update });
            }
            var main = [React.createElement(
                "div",
                null,
                React.createElement(
                    "p",
                    null,
                    this.state.title
                )
            ), React.createElement(
                "div",
                { className: "w-full" },
                type
            )];
            return main;
        }
    }]);

    return Inputbox;
}(React.Component);

var Subtitle = function (_React$Component2) {
    _inherits(Subtitle, _React$Component2);

    function Subtitle() {
        _classCallCheck(this, Subtitle);

        return _possibleConstructorReturn(this, (Subtitle.__proto__ || Object.getPrototypeOf(Subtitle)).apply(this, arguments));
    }

    _createClass(Subtitle, [{
        key: "render",
        value: function render() {
            var main = React.createElement(
                "div",
                { className: "flex" },
                React.createElement(
                    "div",
                    { className: "w-full" },
                    React.createElement(
                        "p",
                        { className: "text-size-small text-little_gray" },
                        this.props.content
                    )
                )
            );
            return main;
        }
    }]);

    return Subtitle;
}(React.Component);

var Introduce = function (_React$Component3) {
    _inherits(Introduce, _React$Component3);

    function Introduce(pro) {
        _classCallCheck(this, Introduce);

        var _this3 = _possibleConstructorReturn(this, (Introduce.__proto__ || Object.getPrototypeOf(Introduce)).call(this, pro));

        _this3.state = {
            accountType: null,
            handle: null,
            sub_data: {},
            changing: false,
            input_tmp: {}
        };
        _this3.render_subtitles = _this3.render_subtitles.bind(_this3);
        _this3.changing = _this3.changing.bind(_this3);
        _this3.render_input = _this3.render_input.bind(_this3);
        _this3.update = _this3.update.bind(_this3);
        return _this3;
    }

    _createClass(Introduce, [{
        key: "get_user_data",
        value: function get_user_data() {
            var _this4 = this;

            fetch("/get_user").then(function (res) {
                return res.json();
            }).then(function (json) {
                _this4.setState({
                    accountType: json.main.accountType,
                    handle: json.main.handle,
                    sub_data: json.sub
                });
            });
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            this.get_user_data();
        }
    }, {
        key: "render_subtitles",
        value: function render_subtitles() {
            var _this5 = this;

            var sub_datas = Object.entries(this.state.sub_data);
            resp = [];
            sub_datas.forEach(function (element) {
                if (element[1] != "") resp.push(React.createElement(Subtitle, { key: element[0], title: element[0], content: element[1], mode: _this5.state.changing }));
            });
            return resp;
        }
    }, {
        key: "render_input",
        value: function render_input() {
            var _this6 = this;

            resp = [React.createElement(Inputbox, { title: "handel", value: this.state.handle, "new": function _new(i, j) {
                    return _this6.new_input(i, j);
                } })];
            var sub_datas = Object.entries(this.state.sub_data);
            sub_datas.forEach(function (element) {
                resp.push(React.createElement(Inputbox, { title: element[0], value: element[1], "new": function _new(i, j) {
                        return _this6.new_input(i, j);
                    } }));
            });
            return resp;
        }
    }, {
        key: "new_input",
        value: function new_input(i, j) {
            var temp = this.state.input_tmp;
            temp[i] = j;
            this.setState({
                input_tmp: temp
            });
        }
    }, {
        key: "changing",
        value: function changing() {
            this.setState({
                changing: !this.state.changing
            });
        }
    }, {
        key: "update",
        value: function update() {
            var _this7 = this;

            fetch("#", { method: "PUT",
                body: JSON.stringify(this.state.input_tmp),
                headers: new Headers({
                    'Content-Type': 'application/json'
                }) }).then(function (res) {
                return res.json();
            }).then(function (respons) {
                if (respons.status == "OK") {
                    _this7.get_user_data();
                }
            });
            this.changing();
        }
    }, {
        key: "render",
        value: function render() {
            var _this8 = this;

            var pos = "container g-15 p-40 flex flex-col profile-area absolute";
            var main_showing;
            if (this.state.changing) {
                main_showing = [React.createElement(this.render_input, null), React.createElement(
                    "div",
                    { className: "flex w-full" },
                    React.createElement(
                        "button",
                        { className: "large-btu-bg w-full", onClick: function onClick() {
                                _this8.update();
                            } },
                        "\u78BA\u8A8D\u4FEE\u6539"
                    )
                ), React.createElement(
                    "div",
                    { className: "flex w-full" },
                    React.createElement(
                        "button",
                        { className: "large-btu-bg w-full", onClick: function onClick() {
                                return _this8.changing();
                            } },
                        "\u53D6\u6D88"
                    )
                )];
            } else {
                main_showing = [React.createElement(
                    "div",
                    { className: "w-full flex flex-col" },
                    React.createElement(
                        "p",
                        { className: "text-size-small font-mono" },
                        this.state.accountType
                    ),
                    React.createElement(
                        "p",
                        { className: "text-size-large font-mono " },
                        this.state.handle
                    )
                ), React.createElement(this.render_subtitles, null), React.createElement(
                    "div",
                    { className: "flex w-full" },
                    React.createElement(
                        "button",
                        { className: "large-btu-bg w-full", onClick: function onClick() {
                                return _this8.changing();
                            } },
                        "\u4FEE\u6539\u500B\u4EBA\u8CC7\u6599"
                    )
                )];
            }
            var context = React.createElement(
                "div",
                { className: pos },
                React.createElement(
                    "div",
                    { className: "m-auto" },
                    React.createElement(
                        "div",
                        { className: "profile-picture-container" },
                        React.createElement("img", { className: "main-img", src: "/static/logo-black.svg", alt: "" })
                    )
                ),
                main_showing
            );
            return context;
        }
    }]);

    return Introduce;
}(React.Component);

var PageSlecter = function (_React$Component4) {
    _inherits(PageSlecter, _React$Component4);

    function PageSlecter(props) {
        _classCallCheck(this, PageSlecter);

        var _this9 = _possibleConstructorReturn(this, (PageSlecter.__proto__ || Object.getPrototypeOf(PageSlecter)).call(this, props));

        _this9.state = {
            inputbox: "1"
        };
        _this9.change = _this9.change.bind(_this9);
        _this9.limit = _this9.limit.bind(_this9);
        return _this9;
    }

    _createClass(PageSlecter, [{
        key: "change",
        value: function change(event) {
            this.setState({ inputbox: event.target.value.replace(/[^\d]/g, '') });
        }
    }, {
        key: "limit",
        value: function limit() {
            var showing = this.state.inputbox;
            var real_page;
            if (showing == "") real_page = 1;else if (parseInt(showing) < 1) real_page = 1;else if (parseInt(showing) > this.props.Lastpage) real_page = this.props.Lastpage;else real_page = parseInt(showing);

            this.setState({ inputbox: real_page });

            this.props.topage(real_page);
        }
    }, {
        key: "bigjump",
        value: function bigjump(i) {
            var real_page;
            if (i) {
                this.props.topage(1);
                real_page = 1;
            } else {
                this.props.topage(this.props.Lastpage);
                real_page = this.props.Lastpage;
            }
            this.setState({
                inputbox: real_page
            });
        }
    }, {
        key: "littlejump",
        value: function littlejump(i) {
            var showing;
            if (i) showing = this.state.inputbox - 1;else showing = this.state.inputbox + 1;
            if (parseInt(showing) < 1) real_page = 1;else if (parseInt(showing) > this.props.Lastpage) real_page = this.props.Lastpage;else real_page = parseInt(showing);

            this.setState({ inputbox: real_page });
            this.props.topage(real_page);
        }
    }, {
        key: "render",
        value: function render() {
            var _this10 = this;

            var main = React.createElement(
                "div",
                { className: "page_container" },
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this10.bigjump(1);
                        } },
                    "<<"
                ),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this10.littlejump(1);
                        } },
                    "<"
                ),
                React.createElement("div", { className: "page_showing" }),
                React.createElement("div", { className: "page_showing" }),
                React.createElement("input", { type: "text",
                    value: this.state.inputbox,
                    className: "page_showing page_now_showing",
                    onChange: this.change,
                    onBlur: this.limit,
                    maxLength: 2 }),
                React.createElement("div", { className: "page_showing" }),
                React.createElement("div", { className: "page_showing" }),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this10.littlejump(0);
                        } },
                    ">"
                ),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this10.bigjump(0);
                        } },
                    ">>"
                )
            );
            return main;
        }
    }]);

    return PageSlecter;
}(React.Component);

var Problem_info = function (_React$Component5) {
    _inherits(Problem_info, _React$Component5);

    function Problem_info() {
        _classCallCheck(this, Problem_info);

        return _possibleConstructorReturn(this, (Problem_info.__proto__ || Object.getPrototypeOf(Problem_info)).apply(this, arguments));
    }

    _createClass(Problem_info, [{
        key: "render",
        value: function render() {
            var status;
            if (this.props.permission == true) {
                status = React.createElement(
                    "p",
                    null,
                    "\u516C\u958B"
                );
            } else {
                status = React.createElement(
                    "p",
                    null,
                    "\u672A\u516C\u958B"
                );
            }
            var url = "/edit/" + this.props.problem_pid;

            var main = React.createElement(
                "div",
                { className: "w-50" },
                React.createElement(
                    "div",
                    { className: "problem-container" },
                    React.createElement(
                        "div",
                        { className: "border-sd p-10 flex flex-col" },
                        React.createElement(
                            "div",
                            { className: "flex g-10 align-items-center problem-title" },
                            React.createElement(
                                "a",
                                { href: url, className: "text-size-small problem-info-col text-bule" },
                                this.props.title
                            ),
                            status
                        ),
                        React.createElement("div", { className: "problem-info-col" })
                    )
                )
            );

            if (this.props.mode = true) {
                return main;
            } else {}
        }
    }]);

    return Problem_info;
}(React.Component);

var Problem_List = function (_React$Component6) {
    _inherits(Problem_List, _React$Component6);

    function Problem_List(prop) {
        _classCallCheck(this, Problem_List);

        var _this12 = _possibleConstructorReturn(this, (Problem_List.__proto__ || Object.getPrototypeOf(Problem_List)).call(this, prop));

        _this12.state = {
            num_per_page: 10,
            showing: 1,
            problems: [],
            num_of_problem: 0
        };

        _this12.topage = _this12.topage.bind(_this12);
        _this12.get_problem_list = _this12.get_problem_list.bind(_this12);
        return _this12;
    }

    _createClass(Problem_List, [{
        key: "getProblems",
        value: function getProblems(i, j) {
            var _this13 = this;

            fetch("/problem_list?" + new URLSearchParams({ numbers: i, from: j })).then(function (res) {
                return res.json();
            }).then(function (list) {
                _this13.setState({
                    problems: _this13.state.problems.concat(list)
                });
            });
        }
    }, {
        key: "getMoerProblems",
        value: function getMoerProblems(i) {
            var from = this.state.problems.length;
            this.getProblems(i, from);
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            this.getProblems(20, 0);
        }
    }, {
        key: "topage",
        value: function topage(i) {
            if (i == this.state.showing) return;
            var real_page = 0;
            var max = Math.ceil(this.props.num_of_problem / this.state.num_per_page);

            if (i > max) {
                real_page = max;
            } else if (i < 1) {
                real_page = 1;
            } else {
                real_page = i;
            }

            num_should_be = this.state.showing * this.state.num_per_page;
            if (this.state.problems.length < num_should_be) {
                var needed = num_should_be - this.state.problems.length + 20;
                this.getMoerProblems(needed);
            }
        }
    }, {
        key: "get_problem_list",
        value: function get_problem_list() {
            re = [];
            var from = (this.state.showing - 1) * this.state.num_of_problem;
            var to = this.state.num_of_problem + from;
            var max = this.state.problems.length;
            for (var i = from; i < to; i++) {
                if (i >= max) {
                    break;
                }
                var element = this.state.problems[i];
                var info = React.createElement(Problem_info, { key: element.problem_pid, problem_pid: element.problem_pid, title: element.title, permission: element.permission });
                re.push(info);
            }

            var main = React.createElement(
                "div",
                { className: "problem-overview-list" },
                re
            );
            if (re.length == 0) {
                var None_problems = React.createElement(
                    "p",
                    { className: "problem-notification p-40" },
                    " You didn't released any problem yet"
                );
                return None_problems;
            } else {
                return main;
            }
        }
    }, {
        key: "render",
        value: function render() {
            var main = React.createElement(
                "div",
                null,
                React.createElement(
                    "div",
                    { className: "m-b-10" },
                    React.createElement(
                        "p",
                        null,
                        "Problrm list"
                    )
                ),
                React.createElement(
                    "div",
                    { className: "" },
                    React.createElement(this.get_problem_list, null)
                )
            );

            return main;
        }
    }]);

    return Problem_List;
}(React.Component);

var OverView_problem = function (_React$Component7) {
    _inherits(OverView_problem, _React$Component7);

    function OverView_problem(props) {
        _classCallCheck(this, OverView_problem);

        var _this14 = _possibleConstructorReturn(this, (OverView_problem.__proto__ || Object.getPrototypeOf(OverView_problem)).call(this, props));

        _this14.state = {
            problem_number: 0,
            problems: []
        };

        _this14.getProblems = _this14.getProblems.bind(_this14);
        return _this14;
    }

    _createClass(OverView_problem, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this15 = this;

            fetch("/problem_list?" + new URLSearchParams({ numbers: 4, from: 0 })).then(function (res) {
                return res.json();
            }).then(function (list) {
                _this15.setState({
                    problems: list["data"]
                });
            });

            fetch("/problem_list_setting").then(function (res) {
                return res.json();
            }).then(function (data) {
                _this15.setState({
                    problem_number: data["count"]
                });
            });
        }
    }, {
        key: "getProblems",
        value: function getProblems() {
            re = [];
            var max = this.state.problems.length;
            for (var i = 0; i < 4; i++) {
                if (i >= max) {
                    break;
                }
                var element = this.state.problems[i];
                var info = React.createElement(Problem_info, { key: element.problem_pid, problem_pid: element.problem_pid, title: element.title, permission: element.permission });
                re.push(info);
            }

            var main = React.createElement(
                "div",
                { className: "problem-overview-list" },
                re
            );
            if (re.length == 0) {
                var None_problems = React.createElement(
                    "p",
                    { className: "problem-notification p-40" },
                    " You didn't released any problem yet"
                );
                return None_problems;
            } else {
                return main;
            }
        }
    }, {
        key: "render",
        value: function render() {
            var overflow_tag;
            if (this.props.num_of_problem > 4) {
                overflow_tag = React.createElement(
                    "a",
                    { href: "", className: "text-align-end" },
                    "...see more"
                );
            } else {
                overflow_tag = "";
            }

            var main = React.createElement(
                "div",
                null,
                React.createElement(
                    "div",
                    { className: "m-b-10" },
                    React.createElement(
                        "p",
                        null,
                        "Problrm list"
                    )
                ),
                React.createElement(
                    "div",
                    { className: "" },
                    React.createElement(this.getProblems, null)
                ),
                React.createElement(
                    "div",
                    { className: "flex justify-content-end" },
                    overflow_tag
                )
            );
            return main;
        }
    }]);

    return OverView_problem;
}(React.Component);

var Tool_bar = function (_React$Component8) {
    _inherits(Tool_bar, _React$Component8);

    function Tool_bar() {
        _classCallCheck(this, Tool_bar);

        return _possibleConstructorReturn(this, (Tool_bar.__proto__ || Object.getPrototypeOf(Tool_bar)).apply(this, arguments));
    }

    _createClass(Tool_bar, [{
        key: "render",
        value: function render() {
            var main = React.createElement(
                "div",
                { className: "items-center container g-20 tool_bar" },
                React.createElement(
                    "div",
                    { className: "flex g-20 w-80 align-items-center" },
                    React.createElement(
                        "div",
                        { className: "h-50" },
                        React.createElement(
                            "a",
                            { href: "/" },
                            React.createElement("img", { width: 100, src: "/static/logo-black.svg" })
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/problem" },
                        React.createElement(
                            "p",
                            { className: "text-size-normal" },
                            "\u984C\u76EE"
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/about" },
                        React.createElement(
                            "p",
                            { className: "text-size-normal" },
                            "\u95DC\u65BC"
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/status" },
                        React.createElement(
                            "p",
                            { className: "text-size-normal" },
                            "\u72C0\u614B"
                        )
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-20 flex justify-end" },
                    React.createElement(
                        "div",
                        null,
                        React.createElement(
                            "button",
                            { className: "text-size-normal" },
                            "\u767B\u51FA"
                        )
                    )
                )
            );
            return main;
        }
    }]);

    return Tool_bar;
}(React.Component);

var Info_selecter = function (_React$Component9) {
    _inherits(Info_selecter, _React$Component9);

    function Info_selecter() {
        _classCallCheck(this, Info_selecter);

        return _possibleConstructorReturn(this, (Info_selecter.__proto__ || Object.getPrototypeOf(Info_selecter)).apply(this, arguments));
    }

    _createClass(Info_selecter, [{
        key: "render",
        value: function render() {
            var _this18 = this;

            var indecater_class = "page-info flex page-info-indecater " + this.props.pos;
            var main = [React.createElement(
                "div",
                { className: "flex g-10 m-b-10 page-info-title" },
                React.createElement(
                    "button",
                    { className: "page-info-btn" },
                    React.createElement("img", { src: "/static/house.svg", alt: "" })
                ),
                React.createElement(
                    "div",
                    { className: "page-info" },
                    React.createElement(
                        "button",
                        { onClick: function onClick() {
                                return _this18.props.onclick("OverView");
                            }, className: "page-info-btn" },
                        "OverView"
                    )
                ),
                React.createElement(
                    "div",
                    { className: "page-info" },
                    React.createElement(
                        "button",
                        { onClick: function onClick() {
                                return _this18.props.onclick("Problem");
                            }, className: "page-info-btn" },
                        "Problems"
                    )
                ),
                React.createElement(
                    "div",
                    { className: indecater_class },
                    React.createElement(
                        "p",
                        null,
                        "<"
                    ),
                    React.createElement(
                        "p",
                        null,
                        ">"
                    )
                )
            ), React.createElement("hr", null)];
            return main;
        }
    }]);

    return Info_selecter;
}(React.Component);

var Main = function (_React$Component10) {
    _inherits(Main, _React$Component10);

    function Main(props) {
        _classCallCheck(this, Main);

        var _this19 = _possibleConstructorReturn(this, (Main.__proto__ || Object.getPrototypeOf(Main)).call(this, props));

        _this19.state = {
            changing: false,
            showing: "OverView",
            problem_number: 0
        };

        _this19.MainContent = _this19.MainContent.bind(_this19);
        return _this19;
    }

    _createClass(Main, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this20 = this;

            fetch("/problem_list_setting").then(function (res) {
                return res.json();
            }).then(function (data) {
                _this20.setState({
                    problem_number: data["count"]
                });
            });
            this.MainContent = this.MainContent.bind(this);
            this.change_Info = this.change_Info.bind(this);
        }
    }, {
        key: "MainContent",
        value: function MainContent() {
            if (this.state.showing == "OverView") {
                var html = [React.createElement(OverView_problem, { position: "", num_of_problem: this.state.problem_number })];
                return html;
            } else if (this.state.showing == "Problem") {
                var _html = React.createElement(Problem_List, null);
                return _html;
            }
        }
    }, {
        key: "change_Info",
        value: function change_Info(i) {
            this.setState({
                showing: i
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this21 = this;

            var translate_pos = {
                "OverView": "info-first",
                "Problem": "info-second"
            };

            var main = [React.createElement(Tool_bar, null)];
            var page = React.createElement(
                "div",
                { className: "p-40 main-page" },
                React.createElement(Introduce, { position: "" }),
                React.createElement(
                    "div",
                    { className: "main-content" },
                    React.createElement(Info_selecter, { onclick: function onclick(i) {
                            _this21.change_Info(i);
                        }, pos: translate_pos[this.state.showing] }),
                    React.createElement(
                        "div",
                        { className: "p-40 container flex flex-col" },
                        React.createElement(this.MainContent, null)
                    )
                )
            );
            main.push(page);
            return main;
        }
    }]);

    return Main;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("main"));
root.render(React.createElement(Main, null));